import json
import os

def create_notebook(cells, filename):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.11.9"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    path = os.path.join("notebooks", filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print(f"Generated {path}")

def md_cell(source):
    if isinstance(source, str):
        source = [line + "\n" for line in source.split("\n")]
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    }

def code_cell(source):
    if isinstance(source, str):
        source = [line + "\n" for line in source.split("\n")]
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }

def generate_all_notebooks():
    os.makedirs("notebooks", exist_ok=True)
    
    # 01_data_exploration.ipynb
    nb1_cells = [
        md_cell("""# 01 - Exploratory Data Analysis (EDA)
## AI-Powered Local Tourism Recommender
This notebook explores the original Indian tourism dataset (`data.csv`) and analyzes key patterns in tourist destinations, geographical distribution, visitor fees, durations, and original ratings."""),
        code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load raw tourism data
df = pd.read_csv('../data/raw/tourism_data.csv')
print(f"Total destinations: {len(df)}")
df.head()"""),
        code_cell("""# Summary statistics of numerical columns
df.describe()"""),
        code_cell("""# Distribution of Tourist Destinations across Indian States
plt.figure(figsize=(12, 6))
top_states = df['State'].value_counts().head(15)
sns.barplot(x=top_states.values, y=top_states.index, palette='viridis')
plt.title('Top 15 Indian States by Number of Featured Tourist Places', fontsize=14, fontweight='bold')
plt.xlabel('Number of Places')
plt.ylabel('State')
plt.show()"""),
        code_cell("""# Distribution of Tourist Site Categories / Types
plt.figure(figsize=(10, 5))
top_types = df['Type'].value_counts().head(10)
sns.barplot(x=top_types.values, y=top_types.index, palette='mako')
plt.title('Top 10 Tourist Site Types in India', fontsize=14, fontweight='bold')
plt.xlabel('Count')
plt.show()"""),
        code_cell("""# Correlation between Visit Duration, Entrance Fee, and Review Rating
corr_cols = ['time needed to visit in hrs', 'Google review rating', 'Entrance Fee in INR', 'Number of google review in lakhs']
corr = df[corr_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix of Tourism Attributes', fontsize=14, fontweight='bold')
plt.show()""")
    ]
    create_notebook(nb1_cells, "01_data_exploration.ipynb")

    # 02_data_preprocessing.ipynb
    nb2_cells = [
        md_cell("""# 02 - Data Cleaning & Preprocessing
This notebook handles data hygiene: standardizing state nomenclature (e.g. correcting `Maharastra` to `Maharashtra`), formatting missing values, string sanitization, and outlier detection."""),
        code_cell("""import pandas as pd
import numpy as np
import sys
sys.path.append('../src')
from data_cleaning import clean_tourism_data

# Load dataset
df_raw = pd.read_csv('../data/raw/tourism_data.csv')
print(f"Original shape: {df_raw.shape}")
print(f"Missing values before cleaning:\n{df_raw.isnull().sum()}")"""),
        code_cell("""# Clean dataset using standardized pipeline
df_cleaned = clean_tourism_data(df_raw)
print(f"Cleaned shape: {df_cleaned.shape}")
print(f"Unique states after cleaning ({len(df_cleaned['State'].unique())}):\n{sorted(df_cleaned['State'].unique())}")"""),
        code_cell("""# Outlier analysis: Skewness in Entrance Fee and Review Count
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.boxplot(y=df_cleaned['Entrance Fee in INR'], ax=axes[0], color='skyblue')
axes[0].set_title('Entrance Fee (INR) - Raw Outliers')

sns.boxplot(y=df_cleaned['Number of google review in lakhs'], ax=axes[1], color='salmon')
axes[1].set_title('Review Count (Lakhs) - Raw Outliers')
plt.show()""")
    ]
    create_notebook(nb2_cells, "02_data_preprocessing.ipynb")

    # 03_dataset_integration.ipynb
    nb3_cells = [
        md_cell("""# 03 - Dataset Integration Pipeline
## Enriched Indian Tourism with UCSD Google Local 2018
This notebook demonstrates the end-to-end integration:
1. Spatial coordinate bounding and keyword extraction on 180,686 verified Indian businesses.
2. High-confidence entity resolution between `data.csv` and Google Places.
3. Review aggregation of ratings and VADER NLP sentiment on review texts.
4. Outputting the enriched `india_tourism_reviews.csv` and preserving unmatched destinations."""),
        code_cell("""import pandas as pd
import json

# Inspect matched places
with open('../data/processed/matched_places.json', 'r', encoding='utf-8') as f:
    matched = json.load(f)
print(f"Total matched destinations: {len(matched)}")
pd.DataFrame(matched).head()"""),
        code_cell("""# Load the final integrated dataset
df_integrated = pd.read_csv('../data/processed/india_tourism_reviews.csv')
print(f"Integrated dataset shape: {df_integrated.shape}")
df_integrated.head(10)"""),
        code_cell("""# Verification of Feature Columns
print("Feature columns verified:")
for col in df_integrated.columns:
    print(f" - {col}: {df_integrated[col].dtype}")"""),
        code_cell("""# Match Status Breakdown
print(df_integrated['match_status'].value_counts())""")
    ]
    create_notebook(nb3_cells, "03_dataset_integration.ipynb")

    # 04_kmeans_clustering.ipynb
    nb4_cells = [
        md_cell("""# 04 - K-Means Clustering Experiments (K=2, 3, 4)
This notebook trains K-Means models on the scaled multi-dimensional feature space, conducts Elbow and Silhouette analysis to evaluate cluster compactness and separation, and profiles the clusters."""),
        code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('../src')

from feature_engineering import FeatureEngineeringPipeline
from clustering import TourismClusteringEngine
from evaluation import ClusteringEvaluator

# Load integrated data
df = pd.read_csv('../data/processed/india_tourism_reviews.csv')
fe = FeatureEngineeringPipeline()
X_scaled, feature_names = fe.fit_transform_comprehensive(df)
X_pca, var_ratio = fe.fit_transform_pca(X_scaled)

print(f"Features: {feature_names}")"""),
        code_cell("""# Run K-Means for K=2, 3, 4
engine = TourismClusteringEngine(random_state=42)
km_res = engine.run_kmeans_experiments(X_scaled, k_values=[2, 3, 4])

for k_name, res in km_res.items():
    print(f"{k_name}: Inertia (WCSS) = {res['inertia']:.2f}")"""),
        code_cell("""# Evaluate WCSS, Silhouette, and Davies-Bouldin
evaluator = ClusteringEvaluator(output_plots_dir='../results/plots', output_metrics_dir='../results/metrics')
metrics = evaluator.evaluate_models(X_scaled, km_res)
metrics"""),
        code_cell("""# Plot Elbow Curve and Silhouette Scores
evaluator.plot_elbow_and_silhouette_curve(X_scaled)
plt.figure(figsize=(9, 5))
img = plt.imread('../results/plots/kmeans_elbow_and_silhouette.png')
plt.imshow(img)
plt.axis('off')
plt.show()"""),
        code_cell("""# Visualize 2D PCA Projections for K=2, 3, 4
evaluator.plot_pca_clusters(X_pca, km_res, var_ratio)
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for idx, k in enumerate([2, 3, 4]):
    img = plt.imread(f'../results/plots/pca_kmeans_k{k}.png')
    axes[idx].imshow(img)
    axes[idx].axis('off')
    axes[idx].set_title(f'K-Means K={k}', fontweight='bold')
plt.tight_layout()
plt.show()""")
    ]
    create_notebook(nb4_cells, "04_kmeans_clustering.ipynb")

    # 05_hierarchical_clustering.ipynb
    nb5_cells = [
        md_cell("""# 05 - Hierarchical Agglomerative Clustering
## Distance Metric Comparison: Euclidean vs. Manhattan
This notebook investigates hierarchical clustering:
1. Ward Linkage (Euclidean metric)
2. Average Linkage (Euclidean metric)
3. Average Linkage (Manhattan / Cityblock metric)
4. Complete Linkage (Manhattan metric)
Includes full dendrogram construction and quantitative metric comparison."""),
        code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../src')

from feature_engineering import FeatureEngineeringPipeline
from clustering import TourismClusteringEngine
from evaluation import ClusteringEvaluator

df = pd.read_csv('../data/processed/india_tourism_reviews.csv')
fe = FeatureEngineeringPipeline()
X_scaled, feature_names = fe.fit_transform_comprehensive(df)
X_pca, var_ratio = fe.fit_transform_pca(X_scaled)

engine = TourismClusteringEngine(random_state=42)
hc_res = engine.run_hierarchical_experiments(X_scaled, k=3)"""),
        code_cell("""# Hierarchical Validation Metrics Comparison
evaluator = ClusteringEvaluator(output_plots_dir='../results/plots', output_metrics_dir='../results/metrics')
hc_metrics = evaluator.evaluate_models(X_scaled, hc_res)
hc_metrics"""),
        code_cell("""# Plot Dendrogram (Ward Linkage)
Z = engine.compute_dendrogram(X_scaled, method='ward')
evaluator.plot_dendrogram(Z)

plt.figure(figsize=(12, 6))
img = plt.imread('../results/plots/hierarchical_dendrogram.png')
plt.imshow(img)
plt.axis('off')
plt.show()"""),
        code_cell("""# Side-by-side Distance Metric Comparison: Euclidean vs. Manhattan
evaluator.plot_distance_comparison(X_pca, hc_res, var_ratio)
plt.figure(figsize=(16, 6))
img = plt.imread('../results/plots/distance_metric_comparison.png')
plt.imshow(img)
plt.axis('off')
plt.show()""")
    ]
    create_notebook(nb5_cells, "05_hierarchical_clustering.ipynb")

    # 06_pca_visualization.ipynb
    nb6_cells = [
        md_cell("""# 06 - Principal Component Analysis (PCA) & Visualization
This notebook examines the dimensionality reduction space:
- Variance explained by principal components
- Feature loadings / eigenvectors
- 2D cluster projections across models"""),
        code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append('../src')

from feature_engineering import FeatureEngineeringPipeline

df = pd.read_csv('../data/processed/india_tourism_reviews.csv')
fe = FeatureEngineeringPipeline()
X_scaled, feature_names = fe.fit_transform_comprehensive(df)
X_pca, var_ratio = fe.fit_transform_pca(X_scaled)

print(f"Component 1 Variance: {var_ratio[0]*100:.2f}%")
print(f"Component 2 Variance: {var_ratio[1]*100:.2f}%")
print(f"Cumulative Variance Explained: {var_ratio.sum()*100:.2f}%")"""),
        code_cell("""# Feature Loadings (Weights) on Principal Components
pca_loadings = pd.DataFrame(
    fe.pca.components_.T,
    index=feature_names,
    columns=['PC1', 'PC2']
)

plt.figure(figsize=(10, 6))
sns.heatmap(pca_loadings, annot=True, cmap='RdBu_r', center=0, fmt='.3f', linewidths=0.5)
plt.title('PCA Feature Loadings (Eigenvectors)', fontsize=14, fontweight='bold')
plt.show()""")
    ]
    create_notebook(nb6_cells, "06_pca_visualization.ipynb")

    # 07_evaluation_and_profiling.ipynb
    nb7_cells = [
        md_cell("""# 07 - Model Evaluation, Cluster Profiling & Recommendations
This notebook summarizes all validation metrics (WCSS, Silhouette, Davies-Bouldin, Calinski-Harabasz) and analyzes the actionable tourist personas identified by the clusters."""),
        code_cell("""import pandas as pd

# Load comprehensive metrics table
metrics_df = pd.read_csv('../results/metrics/evaluation_metrics.csv')
metrics_df.sort_values(by='Silhouette_Score', ascending=False)"""),
        code_cell("""# Load K-Means (K=3) Cluster Profiles
profile_km = pd.read_csv('../results/metrics/cluster_profiles_kmeans_k3.csv')
profile_km"""),
        code_cell("""# Cluster Interpretation & Persona Summary
personas = {
    0: "Budget Cultural & Sacred Heritage (Temples, Lakes, Free/Low Fee, High Satisfaction)",
    1: "Mixed/Critical Feedback Destinations (Low Avg Rating, Moderate Fee, High Negative Sentiment)",
    2: "Premium Heritage & Eco-Exploration (Forts, National Parks, Higher Entry Fee, Longer Visits)"
}

for c, desc in personas.items():
    print(f"Cluster {c}: {desc}")""")
    ]
    create_notebook(nb7_cells, "07_evaluation_and_profiling.ipynb")

if __name__ == '__main__':
    generate_all_notebooks()
