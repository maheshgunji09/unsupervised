import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import seaborn as sns
import os

class TourismClusteringEngine:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.cluster_labels = {}
        
    def run_kmeans_experiments(self, X_scaled, k_values=[2, 3, 4]):
        """
        Runs K-Means clustering for specified K values.
        Returns dictionary of fitted models and cluster labels.
        """
        results = {}
        for k in k_values:
            km = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            labels = km.fit_predict(X_scaled)
            results[f'KMeans_K{k}'] = {
                'model': km,
                'k': k,
                'labels': labels,
                'inertia': km.inertia_,
                'cluster_centers': km.cluster_centers_
            }
            self.cluster_labels[f'KMeans_K{k}'] = labels
            self.models[f'KMeans_K{k}'] = km
        return results

    def run_hierarchical_experiments(self, X_scaled, k=3):
        """
        Runs Hierarchical (Agglomerative) Clustering comparing:
        1. Euclidean distance (Ward linkage)
        2. Euclidean distance (Average linkage)
        3. Manhattan / Cityblock distance (Average linkage)
        4. Manhattan / Cityblock distance (Complete linkage)
        """
        configs = [
            ('Hierarchical_Euclidean_Ward', 'euclidean', 'ward'),
            ('Hierarchical_Euclidean_Average', 'euclidean', 'average'),
            ('Hierarchical_Manhattan_Average', 'manhattan', 'average'),
            ('Hierarchical_Manhattan_Complete', 'manhattan', 'complete')
        ]
        results = {}
        for name, metric, linkage_type in configs:
            model = AgglomerativeClustering(
                n_clusters=k,
                metric=metric,
                linkage=linkage_type
            )
            labels = model.fit_predict(X_scaled)
            results[name] = {
                'model': model,
                'k': k,
                'metric': metric,
                'linkage': linkage_type,
                'labels': labels
            }
            self.cluster_labels[name] = labels
            self.models[name] = model
        return results

    def compute_dendrogram(self, X_scaled, method='ward', metric='euclidean'):
        """
        Computes hierarchical linkage matrix using SciPy.
        """
        if method == 'ward':
            Z = linkage(X_scaled, method='ward')
        else:
            Z = linkage(X_scaled, method=method, metric=metric)
        return Z

if __name__ == '__main__':
    from feature_engineering import FeatureEngineeringPipeline
    df = pd.read_csv('data/processed/india_tourism_reviews.csv')
    fe = FeatureEngineeringPipeline()
    X_scaled, features = fe.fit_transform_comprehensive(df)
    
    engine = TourismClusteringEngine()
    km_res = engine.run_kmeans_experiments(X_scaled, k_values=[2, 3, 4])
    hc_res = engine.run_hierarchical_experiments(X_scaled, k=3)
    
    print("K-Means experiments completed:")
    for k_name, res in km_res.items():
        print(f" - {k_name}: Inertia (WCSS) = {res['inertia']:.2f}")
        
    print("\nHierarchical experiments completed:")
    for h_name, res in hc_res.items():
        counts = pd.Series(res['labels']).value_counts().to_dict()
        print(f" - {h_name}: cluster distribution = {counts}")
