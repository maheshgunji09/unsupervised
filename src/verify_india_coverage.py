import gzip
import ast
import json
import time
import re
import pandas as pd
from collections import Counter

# Load tourism data
tourism_df = pd.read_csv('data.csv')
tourism_places = tourism_df['Name'].dropna().str.strip().tolist()
tourism_places_lower = {name.lower(): name for name in tourism_places}
tourism_cities = set(tourism_df['City'].dropna().str.strip().str.lower())
tourism_states = set(tourism_df['State'].dropna().str.strip().str.lower())

print(f"Loaded {len(tourism_places)} tourist destinations from data.csv.")
print(f"Covering {len(tourism_cities)} unique cities and {len(tourism_states)} unique states.")

# Bounding box for India
# Latitude: 6.5 to 37.5, Longitude: 68.0 to 97.5
LAT_MIN, LAT_MAX = 6.5, 37.5
LON_MIN, LON_MAX = 68.0, 97.5

# Indian state keywords and synonyms
indian_states_keywords = [
    'india', 'delhi', 'maharashtra', 'maharastra', 'mumbai', 'karnataka', 'bengaluru', 'bangalore',
    'tamil nadu', 'chennai', 'uttar pradesh', 'rajasthan', 'jaipur', 'gujarat', 'ahmedabad',
    'kerala', 'kochi', 'west bengal', 'kolkata', 'telangana', 'hyderabad', 'andhra pradesh',
    'madhya pradesh', 'punjab', 'amritsar', 'haryana', 'bihar', 'odisha', 'orissa', 'goa',
    'assam', 'himachal pradesh', 'uttarakhand', 'jammu', 'kashmir', 'chandigarh', 'puducherry',
    'pondicherry', 'jharkhand', 'chhattisgarh', 'sikkim', 'meghalaya', 'agra', 'varanasi'
]
state_pattern = re.compile(r'\b(?:' + '|'.join(indian_states_keywords) + r')\b', re.IGNORECASE)

start_time = time.time()
total_records = 0
india_gps_count = 0
india_address_count = 0
verified_india_records = []
matched_places = {}

print("Scanning places.clean.json.gz...")
with gzip.open('data/raw/places.clean.json.gz', 'rt', encoding='utf-8', errors='ignore') as f:
    for idx, line in enumerate(f):
        total_records += 1
        
        # Fast filter before expensive parsing:
        # Check if line contains coordinates that could be in India or keywords
        has_kw = bool(state_pattern.search(line))
        
        # If no keyword, check if there's gps pattern
        # E.g. 'gps': [lat, lon]
        if not has_kw and "'gps': [" not in line:
            continue
            
        try:
            place = ast.literal_eval(line.strip())
        except Exception:
            continue
            
        gps = place.get('gps')
        address = place.get('address') or []
        address_str = ' '.join(address) if isinstance(address, list) else str(address)
        name = place.get('name', '') or ''
        
        is_india_gps = False
        if gps and len(gps) == 2 and gps[0] is not None and gps[1] is not None:
            lat, lon = gps[0], gps[1]
            if LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX:
                is_india_gps = True
                india_gps_count += 1
                
        is_india_addr = bool(state_pattern.search(address_str)) or bool(state_pattern.search(name))
        if is_india_addr:
            india_address_count += 1
            
        if is_india_gps or is_india_addr:
            verified_india_records.append({
                'gPlusPlaceId': place.get('gPlusPlaceId'),
                'name': name,
                'address': address_str,
                'gps': gps,
                'price': place.get('price'),
                'closed': place.get('closed')
            })
            
            # Check match against data.csv places
            name_clean = name.strip().lower()
            for tp_lower, original_tp in tourism_places_lower.items():
                if tp_lower == name_clean or tp_lower in name_clean or name_clean in tp_lower:
                    if original_tp not in matched_places:
                        matched_places[original_tp] = []
                    matched_places[original_tp].append({
                        'gPlusPlaceId': place.get('gPlusPlaceId'),
                        'google_name': name,
                        'address': address_str,
                        'gps': gps
                    })

        if total_records % 500000 == 0:
            elapsed = time.time() - start_time
            print(f"Processed {total_records:,} records in {elapsed:.1f}s | Verified India so far: {len(verified_india_records):,} | Matched tourism destinations: {len(matched_places)}")

elapsed = time.time() - start_time
print("\n" + "="*60)
print(f"SCAN COMPLETED in {elapsed:.2f} seconds")
print(f"Total Places in dataset: {total_records:,}")
print(f"Places with GPS inside India: {india_gps_count:,}")
print(f"Places with Indian Address/Keywords: {india_address_count:,}")
print(f"Total Verified Indian Businesses/Places: {len(verified_india_records):,}")
print(f"Distinct Tourism Destinations matched from data.csv: {len(matched_places)} / {len(tourism_places)} ({len(matched_places)*100/len(tourism_places):.1f}%)")
print("="*60)

# Save sample matches for inspection
with open('data/raw/sample_matches.json', 'w', encoding='utf-8') as f:
    sample_out = {k: matched_places[k][:3] for k in list(matched_places.keys())[:20]}
    json.dump(sample_out, f, indent=2)

# Save verified Indian places metadata
import pickle
print(f"Saving verified Indian places ({len(verified_india_records):,}) to data/raw/google_places_india.json...")
with open('data/raw/google_places_india.json', 'w', encoding='utf-8') as f:
    for item in verified_india_records:
        f.write(json.dumps(item) + '\n')

print("Saved data/raw/google_places_india.json successfully.")
