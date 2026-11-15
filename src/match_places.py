import json
import re
import difflib
import pandas as pd
import numpy as np

# Load tourism dataset
tourism_df = pd.read_csv('data.csv')

# Clean State names in tourism_df
state_corrections = {
    'Maharastra': 'Maharashtra',
    'Orissa': 'Odisha',
    'Pondicherry': 'Puducherry'
}
tourism_df['State_Clean'] = tourism_df['State'].replace(state_corrections)

# Canonical City aliases
city_aliases = {
    'bengaluru': ['bangalore', 'bengaluru'],
    'mumbai': ['mumbai', 'bombay'],
    'kolkata': ['kolkata', 'calcutta'],
    'chennai': ['chennai', 'madras'],
    'delhi': ['delhi', 'new delhi'],
    'varanasi': ['varanasi', 'banaras', 'kashi'],
    'kochi': ['kochi', 'cochin'],
    'prayagraj': ['prayagraj', 'allahabad'],
    'visakhapatnam': ['visakhapatnam', 'vizag'],
    'puducherry': ['puducherry', 'pondicherry']
}

def normalize_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = [t for t in text.split() if t]
    return " ".join(tokens)

# Load verified Indian places from Google Local
print("Loading verified Indian Google Places...")
google_places = []
with open('data/raw/google_places_india.json', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            google_places.append(json.loads(line.strip()))
print(f"Loaded {len(google_places):,} Indian Google Places.")

# Stopwords for place names
GENERIC_WORDS = {
    'the', 'of', 'and', 'in', 'at', 'temple', 'park', 'fort', 'palace',
    'museum', 'garden', 'gardens', 'beach', 'lake', 'waterfall', 'waterfalls',
    'wildlife', 'sanctuary', 'national', 'memorial', 'monument', 'view', 'point',
    'caves', 'cave', 'tomb', 'stepwell', 'zoo', 'centre', 'center', 'hill', 'hills'
}

def extract_significant_tokens(name):
    norm = normalize_text(name)
    tokens = [w for w in norm.split() if len(w) > 2 and w not in GENERIC_WORDS]
    return set(tokens)

# Index Google places by significant keywords and states
print("Indexing Google Places by keywords...")
from collections import defaultdict
keyword_index = defaultdict(list)
for idx, gp in enumerate(google_places):
    gname = gp.get('name', '')
    tokens = extract_significant_tokens(gname)
    for tok in tokens:
        keyword_index[tok].append(idx)

print(f"Index built with {len(keyword_index):,} unique keywords.")

# Matching function
matches = []
unmatched = []

for idx, row in tourism_df.iterrows():
    p_name = row['Name']
    p_state = row['State_Clean'].lower()
    p_city = str(row['City']).lower() if pd.notna(row['City']) else ""
    
    # Significant tokens for this tourist place
    p_tokens = extract_significant_tokens(p_name)
    p_norm = normalize_text(p_name)
    
    candidate_indices = set()
    for tok in p_tokens:
        if tok in keyword_index:
            candidate_indices.update(keyword_index[tok])
            
    best_match = None
    best_score = 0.0
    
    for c_idx in candidate_indices:
        cand = google_places[c_idx]
        c_name = cand.get('name', '')
        c_norm = normalize_text(c_name)
        c_addr = normalize_text(cand.get('address', ''))
        
        # State/City validation
        state_match = p_state in c_addr
        city_match = False
        if p_city:
            city_variants = city_aliases.get(p_city, [p_city])
            city_match = any(v in c_addr for v in city_variants)
            
        # Geographic / text compatibility bonus
        location_weight = 1.0
        if state_match or city_match:
            location_weight = 1.4
        elif any(s in c_addr for s in ['delhi', 'maharashtra', 'karnataka', 'tamil nadu', 'rajasthan', 'kerala'] if s != p_state):
            # Penalty if explicitly in a different major state
            location_weight = 0.5
            
        # String similarities
        seq_ratio = difflib.SequenceMatcher(None, p_norm, c_norm).ratio()
        
        c_tokens = extract_significant_tokens(c_name)
        if p_tokens and c_tokens:
            jaccard = len(p_tokens & c_tokens) / len(p_tokens | c_tokens)
            overlap = len(p_tokens & c_tokens) / len(p_tokens)
        else:
            jaccard = 0.0
            overlap = 0.0
            
        # Combined score
        score = (seq_ratio * 0.4 + jaccard * 0.3 + overlap * 0.3) * location_weight
        
        # Exact match boost
        if p_norm == c_norm and (state_match or city_match):
            score = 2.0
            
        if score > best_score:
            best_score = score
            best_match = {
                'place_idx': idx,
                'tourism_name': p_name,
                'matched_google_name': c_name,
                'score': score,
                'gPlusPlaceId': cand.get('gPlusPlaceId'),
                'address': cand.get('address'),
                'gps': cand.get('gps'),
                'price': cand.get('price'),
                'closed': cand.get('closed')
            }
            
    # Acceptance threshold
    if best_match and best_score >= 0.65:
        matches.append(best_match)
    else:
        unmatched.append({
            'place_idx': idx,
            'tourism_name': p_name,
            'state': row['State'],
            'city': row['City'],
            'best_candidate': best_match['matched_google_name'] if best_match else None,
            'best_score': best_score
        })

print("\n" + "="*60)
print(f"MATCHING RESULTS:")
print(f"Total tourist places in data.csv: {len(tourism_df)}")
print(f"High-confidence matched places: {len(matches)} ({len(matches)*100/len(tourism_df):.1f}%)")
print(f"Unmatched places: {len(unmatched)} ({len(unmatched)*100/len(tourism_df):.1f}%)")
print("="*60)

# Save matched mapping and unmatched list
with open('data/processed/matched_places.json', 'w', encoding='utf-8') as f:
    json.dump(matches, f, indent=2)

with open('data/processed/unmatched_places.json', 'w', encoding='utf-8') as f:
    json.dump(unmatched, f, indent=2)

print("Saved data/processed/matched_places.json and data/processed/unmatched_places.json.")

# Print 10 samples of matched places
print("\nSample High-Confidence Matches:")
for m in matches[:10]:
    print(f" - [{m['tourism_name']}] -> [{m['matched_google_name']}] (Score: {m['score']:.2f}, ID: {m['gPlusPlaceId']}, GPS: {m['gps']})")
