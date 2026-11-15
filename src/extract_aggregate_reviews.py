import gzip
import json
import re
import ast
import time
import os
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main():
    start_time = time.time()
    
    # 1. Load matched places
    matched_file = os.path.join('data', 'processed', 'matched_places.json')
    if not os.path.exists(matched_file):
        raise FileNotFoundError(f"Missing {matched_file}. Run match_places.py first.")
        
    with open(matched_file, 'r', encoding='utf-8') as f:
        matched_places = json.load(f)
        
    place_id_to_info = {}
    for item in matched_places:
        pid = item.get('gPlusPlaceId')
        if pid:
            place_id_to_info[str(pid)] = item

    tourism_place_ids = set(place_id_to_info.keys())
    print(f"Targeting reviews for {len(tourism_place_ids)} matched tourist destinations...")

    # Load all verified Indian place IDs as well
    india_places_file = os.path.join('data', 'raw', 'google_places_india.json')
    all_india_place_ids = set()
    if os.path.exists(india_places_file):
        with open(india_places_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line.strip())
                    pid = rec.get('gPlusPlaceId')
                    if pid:
                        all_india_place_ids.add(str(pid))
        print(f"Loaded {len(all_india_place_ids):,} total verified Indian place IDs.")

    # Initialize sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # PlaceId extraction regex handling optional unicode prefix u'...'
    re_place_id = re.compile(r"'gPlusPlaceId':\s*u?['\"](\d+)['\"]")

    reviews_path = os.path.join('data', 'raw', 'reviews.clean.json.gz')
    if not os.path.exists(reviews_path):
        raise FileNotFoundError(f"Missing {reviews_path}. Download reviews first.")

    # Storage for matched reviews per place ID
    tourism_reviews = {pid: {'ratings': [], 'sentiments': [], 'texts_count': 0} for pid in tourism_place_ids}

    print("Scanning reviews.clean.json.gz (11.45M reviews)...")
    total_reviews_scanned = 0
    all_india_reviews_count = 0
    tourism_reviews_count = 0
    
    with gzip.open(reviews_path, 'rt', encoding='utf-8', errors='ignore') as f:
        for line in f:
            total_reviews_scanned += 1
            
            # Fast check with regex
            m = re_place_id.search(line)
            if not m:
                continue
                
            pid = m.group(1)
            is_india = pid in all_india_place_ids
            is_tourism = pid in tourism_place_ids
            
            if not is_india and not is_tourism:
                continue
                
            if is_india:
                all_india_reviews_count += 1
                
            if not is_tourism:
                continue
                
            # Parse record for tourism destinations
            try:
                rec = ast.literal_eval(line.strip())
            except Exception:
                continue
                
            tourism_reviews_count += 1
            rating = float(rec.get('rating', 3.0))
            review_text = rec.get('reviewText', '') or ''
            
            # Sentiment calculation
            if review_text.strip():
                # VADER compound score is in [-1, 1]
                sentiment = sia.polarity_scores(review_text)['compound']
                tourism_reviews[pid]['texts_count'] += 1
            else:
                # Rating-based baseline fallback: 1-> -1.0, 3->0.0, 5->+1.0
                sentiment = (rating - 3.0) / 2.0
                
            tourism_reviews[pid]['ratings'].append(rating)
            tourism_reviews[pid]['sentiments'].append(sentiment)
            
            if total_reviews_scanned % 1000000 == 0:
                elapsed = time.time() - start_time
                print(f"Scanned {total_reviews_scanned:,} reviews in {elapsed:.1f}s | Indian reviews: {all_india_reviews_count:,} | Matched tourism reviews: {tourism_reviews_count:,}", flush=True)

    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print(f"REVIEW SCAN COMPLETED in {elapsed:.1f} seconds")
    print(f"Total reviews in dataset: {total_reviews_scanned:,}")
    print(f"Total reviews for verified Indian businesses: {all_india_reviews_count:,}")
    print(f"Total reviews matching tourist destinations: {tourism_reviews_count:,}")
    print("="*60)

    # Aggregate metrics per place
    aggregated_results = {}
    places_with_reviews = 0
    for pid, data in tourism_reviews.items():
        ratings = data['ratings']
        sentiments = data['sentiments']
        count = len(ratings)
        
        if count > 0:
            places_with_reviews += 1
            avg_rating = float(np.mean(ratings))
            pos_count = sum(1 for r in ratings if r >= 4.0)
            neg_count = sum(1 for r in ratings if r <= 2.0)
            pos_pct = round(pos_count * 100.0 / count, 2)
            neg_pct = round(neg_count * 100.0 / count, 2)
            avg_sentiment = float(np.mean(sentiments))
        else:
            avg_rating = None
            pos_pct = None
            neg_pct = None
            avg_sentiment = None
            
        aggregated_results[pid] = {
            'gPlusPlaceId': pid,
            'tourism_name': place_id_to_info[pid]['tourism_name'],
            'google_name': place_id_to_info[pid]['matched_google_name'],
            'review_count': count,
            'avg_rating': avg_rating,
            'positive_review_pct': pos_pct,
            'negative_review_pct': neg_pct,
            'sentiment_score': round(avg_sentiment, 4) if avg_sentiment is not None else None,
            'reviews_with_text': data['texts_count']
        }

    print(f"Distinct tourist destinations with active Google reviews: {places_with_reviews} / {len(tourism_place_ids)}")

    # Save aggregated reviews
    out_file = os.path.join('data', 'processed', 'aggregated_business_reviews.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(aggregated_results, f, indent=2)
    print(f"Saved aggregated reviews for {len(aggregated_results)} places to {out_file}.")

if __name__ == '__main__':
    main()
