import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA

class FeatureEngineeringPipeline:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2, random_state=42)
        self.feature_names = []
        
    def fit_transform_comprehensive(self, df: pd.DataFrame):
        """
        Creates standardized feature matrix including spatial, economic,
        and review/sentiment metrics with skewness correction.
        """
        df = df.copy()
        
        # Log transformations for heavily right-skewed features
        df['entry_fee_log'] = np.log1p(df['entry_fee'])
        df['review_count_log'] = np.log1p(df['review_count'])
        
        self.feature_names = [
            'latitude',
            'longitude',
            'entry_fee_log',
            'visit_duration',
            'avg_rating',
            'review_count_log',
            'positive_review_pct',
            'negative_review_pct',
            'sentiment_score'
        ]
        
        X_raw = df[self.feature_names].values
        X_scaled = self.scaler.fit_transform(X_raw)
        return X_scaled, self.feature_names

    def fit_transform_subset(self, df: pd.DataFrame, subset_name='geographic'):
        """
        Creates specific feature subsets for targeted segmentation:
        - 'geographic': latitude, longitude, review_count_log
        - 'significance': entry_fee_log, visit_duration
        - 'sentiment': avg_rating, review_count_log, positive_review_pct, negative_review_pct, sentiment_score
        """
        df = df.copy()
        df['entry_fee_log'] = np.log1p(df['entry_fee'])
        df['review_count_log'] = np.log1p(df['review_count'])
        
        subsets = {
            'geographic': ['latitude', 'longitude', 'review_count_log'],
            'significance': ['entry_fee_log', 'visit_duration'],
            'sentiment': ['avg_rating', 'review_count_log', 'positive_review_pct', 'negative_review_pct', 'sentiment_score']
        }
        
        cols = subsets.get(subset_name, self.feature_names)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[cols].values)
        return X_scaled, cols

    def fit_transform_pca(self, X_scaled):
        """
        Fits 2D PCA on scaled features for visualization.
        """
        X_pca = self.pca.fit_transform(X_scaled)
        explained_variance = self.pca.explained_variance_ratio_
        return X_pca, explained_variance

if __name__ == '__main__':
    df = pd.read_csv('data/processed/india_tourism_reviews.csv')
    fe = FeatureEngineeringPipeline()
    X_scaled, features = fe.fit_transform_comprehensive(df)
    X_pca, var_ratio = fe.fit_transform_pca(X_scaled)
    print(f"X_scaled shape: {X_scaled.shape}")
    print(f"Features: {features}")
    print(f"PCA explained variance: {var_ratio} (Total: {var_ratio.sum():.4f})")
