import os
import json
import pandas as pd
import numpy as np
from city_coordinates import CITY_COORDINATES

def integrate_datasets():
    print("Integrating Indian Tourism Dataset with Google Local Reviews...")

    # 1. Load original tourism data
    tourism_df = pd.read_csv('data.csv')
    
    # Clean state names
    state_map = {
        'Maharastra': 'Maharashtra',
        'Orissa': 'Odisha',
        'Pondicherry': 'Puducherry'
    }
    tourism_df['State'] = tourism_df['State'].replace(state_map)
    
    # 2. Load matched places mapping
    matched_file = os.path.join('data', 'processed', 'matched_places.json')
    if os.path.exists(matched_file):
        with open(matched_file, 'r', encoding='utf-8') as f:
            matched_list = json.load(f)
    else:
        matched_list = []
        
    matched_by_idx = {m['place_idx']: m for m in matched_list}
    matched_by_name = {m['tourism_name']: m for m in matched_list}
    
    # 3. Load aggregated Google Local reviews
    reviews_file = os.path.join('data', 'processed', 'aggregated_business_reviews.json')
    if os.path.exists(reviews_file):
        with open(reviews_file, 'r', encoding='utf-8') as f:
            agg_reviews = json.load(f)
    else:
        agg_reviews = {}
        
    # Map aggregated review by gPlusPlaceId
    # Also index by tourism_name
    reviews_by_place_id = agg_reviews
    reviews_by_name = {v['tourism_name']: v for v in agg_reviews.values() if 'tourism_name' in v}
    
    integrated_rows = []
    unmatched_rows = []
    
    for idx, row in tourism_df.iterrows():
        p_name = row['Name']
        state = row['State']
        city = str(row['City']).strip().lower() if pd.notna(row['City']) else ""
        category = row['Type'] if pd.notna(row['Type']) and str(row['Type']).strip() != "" else row.get('Significance', 'General')
        
        # Clean numerical fields from data.csv
        try:
            entry_fee = float(row['Entrance Fee in INR']) if pd.notna(row['Entrance Fee in INR']) else 0.0
        except (ValueError, TypeError):
            entry_fee = 0.0
            
        try:
            visit_duration = float(row['time needed to visit in hrs']) if pd.notna(row['time needed to visit in hrs']) else 1.5
        except (ValueError, TypeError):
            visit_duration = 1.5
            
        # Baseline values from original dataset
        orig_rating = float(row['Google review rating']) if pd.notna(row['Google review rating']) else 4.0
        orig_review_count = float(row['Number of google review in lakhs']) * 100000 if pd.notna(row['Number of google review in lakhs']) else 1000
        
        # Check match
        matched_info = matched_by_idx.get(idx) or matched_by_name.get(p_name)
        is_matched = matched_info is not None
        
        # Determine coordinates
        lat, lon = None, None
        if is_matched and matched_info.get('gps'):
            gps = matched_info['gps']
            if len(gps) == 2 and gps[0] is not None and gps[1] is not None:
                lat, lon = float(gps[0]), float(gps[1])
                # Normalize microdegrees if present (e.g. 30123364 -> 30.123364)
                if abs(lat) > 90.0:
                    lat = lat / 1e6
                if abs(lon) > 180.0:
                    lon = lon / 1e6
                
        # Fallback coordinates from city/landmark lookup
        if lat is None or lon is None or lat == 0 or lon == 0:
            if city in CITY_COORDINATES:
                lat, lon = CITY_COORDINATES[city]
            else:
                # Default approximate central coordinates of India
                lat, lon = 20.5937, 78.9629

        # Review features
        rev_info = None
        if is_matched and matched_info.get('gPlusPlaceId'):
            pid = str(matched_info['gPlusPlaceId'])
            rev_info = reviews_by_place_id.get(pid)
        if not rev_info and p_name in reviews_by_name:
            rev_info = reviews_by_name[p_name]
            
        if rev_info and rev_info.get('review_count', 0) > 0:
            # We have enriched Google Local reviews!
            avg_rating = rev_info['avg_rating'] if rev_info.get('avg_rating') is not None else orig_rating
            review_count = rev_info['review_count']
            positive_review_pct = rev_info['positive_review_pct'] if rev_info.get('positive_review_pct') is not None else 85.0
            negative_review_pct = rev_info['negative_review_pct'] if rev_info.get('negative_review_pct') is not None else 5.0
            sentiment_score = rev_info['sentiment_score'] if rev_info.get('sentiment_score') is not None else round((avg_rating - 3.0)/2.0, 4)
            match_status = "enriched_google_reviews"
        elif is_matched:
            # Matched to place metadata, but 0 reviews in 2018 crawl: use verified metadata and rating baseline
            avg_rating = orig_rating
            review_count = int(orig_review_count)
            # Baseline sentiment from rating
            # Rating 4.5 -> pos ~85%, neg ~5%, sentiment ~0.75
            sentiment_score = round((avg_rating - 3.0) / 2.0, 4)
            positive_review_pct = round(max(0.0, min(100.0, (avg_rating / 5.0) * 100 - 5)), 2)
            negative_review_pct = round(max(0.0, min(100.0, 100.0 - positive_review_pct - 10.0)), 2)
            match_status = "matched_metadata_only"
        else:
            # Unmatched tourism place
            avg_rating = orig_rating
            review_count = int(orig_review_count)
            sentiment_score = round((avg_rating - 3.0) / 2.0, 4)
            positive_review_pct = round(max(0.0, min(100.0, (avg_rating / 5.0) * 100 - 5)), 2)
            negative_review_pct = round(max(0.0, min(100.0, 100.0 - positive_review_pct - 10.0)), 2)
            match_status = "unmatched_preserved"
            
            unmatched_rows.append({
                'place_name': p_name,
                'state': state,
                'city': row['City'],
                'category': category,
                'entry_fee': entry_fee,
                'visit_duration': visit_duration,
                'orig_rating': orig_rating,
                'orig_reviews_lakhs': row['Number of google review in lakhs']
            })

        integrated_rows.append({
            'place_name': p_name,
            'state': state,
            'latitude': round(lat, 6),
            'longitude': round(lon, 6),
            'category': category,
            'entry_fee': entry_fee,
            'visit_duration': visit_duration,
            'avg_rating': round(avg_rating, 2),
            'review_count': int(review_count),
            'positive_review_pct': round(positive_review_pct, 2),
            'negative_review_pct': round(negative_review_pct, 2),
            'sentiment_score': round(sentiment_score, 4),
            'match_status': match_status
        })

    # Create DataFrames
    df_integrated = pd.DataFrame(integrated_rows)
    df_unmatched = pd.DataFrame(unmatched_rows)
    
    # Save datasets
    out_integrated = os.path.join('data', 'processed', 'india_tourism_reviews.csv')
    out_unmatched = os.path.join('data', 'processed', 'unmatched_tourism_places.csv')
    
    df_integrated.to_csv(out_integrated, index=False)
    df_unmatched.to_csv(out_unmatched, index=False)
    
    print("\n" + "="*60)
    print("DATASET INTEGRATION COMPLETED")
    print(f"Total tourist destinations processed: {len(df_integrated)}")
    print(f"Places enriched with Google Reviews: {(df_integrated['match_status'] == 'enriched_google_reviews').sum()}")
    print(f"Places matched with metadata: {(df_integrated['match_status'] == 'matched_metadata_only').sum()}")
    print(f"Unmatched places preserved: {len(df_unmatched)}")
    print(f"Output saved to: {out_integrated}")
    print(f"Unmatched saved to: {out_unmatched}")
    print("="*60)
    print("\nSample rows of integrated dataset:")
    print(df_integrated.head(10)[['place_name', 'state', 'latitude', 'longitude', 'category', 'avg_rating', 'sentiment_score', 'match_status']])

if __name__ == '__main__':
    integrate_datasets()
