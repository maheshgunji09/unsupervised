import pandas as pd
import numpy as np

def clean_tourism_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw tourism data by standardizing column names, state names,
    handling missing values, and formatting data types.
    """
    df = df.copy()
    
    # Standardize state names
    state_mapping = {
        'Maharastra': 'Maharashtra',
        'Orissa': 'Odisha',
        'Pondicherry': 'Puducherry'
    }
    if 'state' in df.columns:
        df['state'] = df['state'].replace(state_mapping)
    elif 'State' in df.columns:
        df['State'] = df['State'].replace(state_mapping)
        
    # Standardize string fields
    str_cols = ['place_name', 'state', 'category', 'City', 'Name', 'Type', 'Significance']
    for col in str_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    # Numeric conversions with safe defaults
    numeric_defaults = {
        'entry_fee': 0.0,
        'Entrance Fee in INR': 0.0,
        'visit_duration': 1.5,
        'time needed to visit in hrs': 1.5,
        'avg_rating': 4.0,
        'Google review rating': 4.0,
        'review_count': 1000,
        'Number of google review in lakhs': 0.1,
        'positive_review_pct': 85.0,
        'negative_review_pct': 5.0,
        'sentiment_score': 0.5
    }
    
    for col, default_val in numeric_defaults.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(default_val)
            
    return df

if __name__ == '__main__':
    df = pd.read_csv('data/processed/india_tourism_reviews.csv')
    cleaned = clean_tourism_data(df)
    print(f"Cleaned dataset: {cleaned.shape[0]} rows, {cleaned.shape[1]} columns.")
    print("Null count:", cleaned.isnull().sum().to_dict())
