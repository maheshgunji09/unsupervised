import os
import sys
import pandas as pd
import numpy as np

from data_cleaning import clean_tourism_data
from feature_engineering import FeatureEngineeringPipeline
from clustering import TourismClusteringEngine
from evaluation import ClusteringEvaluator

def run_complete_ml_pipeline():
    print("="*70)
    print("STARTING ML CLUSTERING & EVALUATION PIPELINE")
    print("="*70)
    
    # 1. Load integrated dataset
    data_path = os.path.join('data', 'processed', 'india_tourism_reviews.csv')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Missing {data_path}. Run dataset_integration.py first.")
        
    df_raw = pd.read_csv(data_path)
    print(f"Loaded integrated dataset: {df_raw.shape[0]} places, {df_raw.shape[1]} columns.")
    
    # 2. Data Cleaning
    df = clean_tourism_data(df_raw)
    
    # 3. Feature Engineering & Scaling
    fe = FeatureEngineeringPipeline()
    X_scaled, feature_names = fe.fit_transform_comprehensive(df)
    X_pca, var_ratio = fe.fit_transform_pca(X_scaled)
    
    print(f"Scaled feature matrix: {X_scaled.shape}")
    print(f"PCA Variance Explained: Component 1 = {var_ratio[0]*100:.2f}%, Component 2 = {var_ratio[1]*100:.2f}% (Total: {var_ratio.sum()*100:.2f}%)")
    
    # 4. Clustering Engine
    engine = TourismClusteringEngine(random_state=42)
    
    # Run K-Means for K=2, 3, 4
    km_results = engine.run_kmeans_experiments(X_scaled, k_values=[2, 3, 4])
    
    # Run Hierarchical for K=3 (Euclidean vs Manhattan)
    hc_results = engine.run_hierarchical_experiments(X_scaled, k=3)
    
    # Combine all models for evaluation
    all_models = {}
    all_models.update(km_results)
    all_models.update(hc_results)
    
    # 5. Evaluation & Metrics
    evaluator = ClusteringEvaluator()
    metrics_df = evaluator.evaluate_models(X_scaled, all_models)
    
    print("\n" + "="*70)
    print("CLUSTERING VALIDATION METRICS:")
    print(metrics_df.to_string(index=False))
    print("="*70)
    
    # 6. Visualizations
    # Elbow and Silhouette curves
    evaluator.plot_elbow_and_silhouette_curve(X_scaled, k_range=range(2, 11))
    
    # Dendrogram for Hierarchical clustering
    Z = engine.compute_dendrogram(X_scaled, method='ward')
    evaluator.plot_dendrogram(Z)
    
    # PCA 2D projections for all models
    evaluator.plot_pca_clusters(X_pca, all_models, var_ratio)
    
    # Distance metric comparison (Euclidean vs Manhattan)
    evaluator.plot_distance_comparison(X_pca, hc_results, var_ratio)
    
    # 7. Cluster Profiling & Interpretations
    # Profile K-Means K=3 (baseline optimal)
    kmeans_k3_labels = km_results['KMeans_K3']['labels']
    profile_kmeans = evaluator.profile_clusters(df, kmeans_k3_labels, model_name='KMeans_K3')
    
    # Profile Hierarchical Ward K=3
    ward_k3_labels = hc_results['Hierarchical_Euclidean_Ward']['labels']
    profile_ward = evaluator.profile_clusters(df, ward_k3_labels, model_name='Hierarchical_Ward_K3')
    
    print("\n" + "="*70)
    print("K-MEANS (K=3) CLUSTER PROFILES:")
    print(profile_kmeans.to_string(index=False))
    print("="*70)
    
    print("\nAll ML experiments, metrics, and visualization plots generated successfully!")

if __name__ == '__main__':
    run_complete_ml_pipeline()
