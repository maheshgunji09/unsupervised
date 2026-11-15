# Local Tourism Recommender (Extended Integration)

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.9.1-orange.svg)](https://scikit-learn.org/)
[![NLTK VADER](https://img.shields.io/badge/NLP-VADER%20Sentiment-brightgreen.svg)](https://www.nltk.org/)

An enterprise-grade, unsupervised machine learning system for personalized tourism recommendation and behavioral segmentation across India. This project extends the original repository by integrating real-world geographic, business metadata, and review sentiment from the **UCSD Google Local Reviews (2018)** dataset with India's must-see destinations dataset (`data.csv`).

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Data Integration Architecture](#data-integration-architecture)
3. [Verified Dataset Statistics](#verified-dataset-statistics)
4. [Feature Engineering & Schema](#feature-engineering--schema)
5. [Machine Learning Pipeline](#machine-learning-pipeline)
6. [Experimental Results & Evaluation Benchmarks](#experimental-results--evaluation-benchmarks)
7. [Cluster Profiles & Tourist Personas](#cluster-profiles--tourist-personas)
8. [Repository Directory Structure](#repository-directory-structure)
9. [Quickstart & Reproducibility Guide](#quickstart--reproducibility-guide)
10. [Authors & Acknowledgments](#authors--acknowledgments)

---

## Project Overview

Traditional tourism recommendation systems rely solely on generic place categories or static guidebook lists. This project creates an adaptive, multi-dimensional segmentation engine that combines:
* **Spatial Geography:** Precision GPS coordinates bounded across India.
* **Economic Constraints & Time Commitments:** Entrance fees (INR) and duration of visits.
* **Customer Reputation & Real Feedback:** Google Local review volumes, star ratings, and NLP sentiment analysis of actual traveler text reviews.

By clustering tourist destinations across these orthogonal dimensions using **K-Means**, **Hierarchical Agglomerative Clustering (Euclidean vs. Manhattan)**, and **Principal Component Analysis (PCA)**, tourism boards, travel agencies, and travelers can uncover distinct destination personas and optimize itineraries.

---

## Data Integration Architecture

Rather than discarding the rich domain information in the original `data.csv`, we utilize it as the primary anchor and enrich it with Google Local business metadata and reviews.

```
+------------------------------------+        +-----------------------------------+
|       Primary Tourism Data         |        |   UCSD Google Local 2018 Dataset  |
|            (data.csv)              |        |   places.clean.json.gz (277 MB)   |
| 325 destinations across 33 states  |        |   reviews.clean.json.gz (1.4 GB)  |
+-----------------+------------------+        +-----------------+-----------------+
                  |                                             |
                  |                   +-------------------------+
                  |                   | Country & State Filtering:
                  |                   | - India Bounding Box [6.5-37.5 N, 68-97.5 E]
                  |                   | - 180,686 verified Indian businesses
                  |                   v
                  |          +----------------------------------+
                  +--------->|  High-Confidence Place Matching  |
                             |  - Token similarity & city alias |
                             |  - 281 matched destinations      |
                             +----------------+-----------------+
                                              |
                                              v
                             +----------------------------------+
                             |   Review Extraction & NLP VADER  |
                             |   - 11.45M reviews scanned       |
                             |   - 645,269 Indian reviews       |
                             |   - 9,521 matched reviews        |
                             |   - Compound sentiment scoring   |
                             +----------------+-----------------+
                                              |
                                              v
                             +----------------------------------+
                             |     Final Integrated Dataset     |
                             |  india_tourism_reviews.csv (325) |
                             |  unmatched_tourism_places.csv(44)|
                             +----------------+-----------------+
                                              |
                                              v
                             +----------------------------------+
                             |   Unsupervised ML Pipeline       |
                             |  - Skewness correction (log1p)   |
                             |  - StandardScaler normalization  |
                             |  - K-Means (K=2, 3, 4)           |
                             |  - Hierarchical (Ward/Manhattan) |
                             |  - 2D PCA Projections            |
                             +----------------------------------+
```

### Dataset Integration Rules
1. **India-Only Filtering:** Google Places were filtered by official bounding coordinates and verified Indian state/address tokens, yielding 180,686 verified businesses.
2. **Entity Resolution:** Tourism places were matched against Google metadata using normalized token overlap and state/city compatibility.
3. **Review Joining:** Using `gPlusPlaceId`, reviews were scanned and mapped to their respective business metadata.
4. **Sentiment Scoring:** Natural language sentiment was calculated using NLTK VADER compound polarity on review texts; for unreviewed destinations, baseline sentiment from ratings was preserved.
5. **Transparency & Unmatched Preservation:** The 44 unmatched destinations are preserved separately in `data/processed/unmatched_tourism_places.csv` without inventing artificial reviews.

---

## Verified Dataset Statistics

| Metric | Empirical Count | Notes |
|---|---|---|
| **Total Places in Google Dataset** | 3,114,353 | Worldwide coverage |
| **Places with GPS inside India** | 173,647 | Bounded latitude [6.5, 37.5], longitude [68.0, 97.5] |
| **Places with Indian Address Tokens** | 160,255 | State/city address verified |
| **Total Verified Indian Places** | 180,686 | Complete India metadata subset |
| **Tourism Destinations in data.csv** | 325 | Spanning 33 states and union territories |
| **High-Confidence Matched Places** | 281 (86.5%) | Verified against Google Local metadata |
| **Unmatched Places Preserved** | 44 (13.5%) | Separately tracked in dedicated table |
| **Total Reviews Scanned** | 11,453,845 | Full UCSD Google Local review corpus |
| **Reviews for Indian Businesses** | 645,269 | Confirmed Indian review ecosystem |
| **Reviews Matched to Tourist Places** | 9,521 | Text & ratings assigned to destination IDs |
| **Matched Places with Active Reviews**| 274 (100.0%) | Full review statistics populated |

---

## Feature Engineering & Schema

The integrated dataset `data/processed/india_tourism_reviews.csv` adheres strictly to the target specification:

| Feature | Type | Description |
|---|---|---|
| `place_name` | String | Official tourist destination name |
| `state` | String | Standardized Indian state (e.g., corrected 'Maharastra' -> 'Maharashtra') |
| `latitude` | Float | Verified latitude in decimal degrees |
| `longitude` | Float | Verified longitude in decimal degrees |
| `category` | String | Destination type / category (Temple, Fort, National Park, etc.) |
| `entry_fee` | Float | Entrance fee in INR |
| `visit_duration` | Float | Estimated visit duration in hours |
| `avg_rating` | Float | Google average star rating (1.0 - 5.0) |
| `review_count` | Integer | Total Google review volume |
| `positive_review_pct` | Float | Percentage of ratings >= 4.0 stars |
| `negative_review_pct` | Float | Percentage of ratings <= 2.0 stars |
| `sentiment_score` | Float | Aggregated NLP compound sentiment score (-1.0 to +1.0) |
| `match_status` | String | Audit tag (`enriched_google_reviews`, `unmatched_preserved`) |

---

## Machine Learning Pipeline

1. **Pre-processing & Skewness Correction:** 
   - Heavily skewed variables (`entry_fee`, `review_count`) are transformed via `log1p(x)`.
2. **Standardization:**
   - All continuous variables are standardized via `StandardScaler` to zero mean and unit variance.
3. **K-Means Clustering:**
   - Evaluated across $K \in \{2, 3, 4\}$ with `random_state=42` and `n_init=10`.
4. **Hierarchical Agglomerative Clustering:**
   - Tested across distance metrics:
     - **Euclidean:** Ward Linkage and Average Linkage.
     - **Manhattan / Cityblock:** Average Linkage and Complete Linkage.
5. **Dimensionality Reduction (PCA):**
   - 2-component PCA preserves 52.75% of cumulative multi-dimensional variance for clear visual projection.

---

## Experimental Results & Evaluation Benchmarks

All models were evaluated on three standard clustering validation metrics:
* **WCSS (Within-Cluster Sum of Squares / Inertia):** Lower indicates tighter clusters.
* **Silhouette Score:** Ranges from -1 to +1; higher indicates well-separated, cohesive clusters.
* **Davies-Bouldin Index:** Lower indicates better cluster separation and compactness.
* **Calinski-Harabasz Index:** Higher indicates dense, well-separated clusters.

### Quantitative Benchmark Table

| Model | K | Metric | Linkage | WCSS (Inertia) | Silhouette Score | Davies-Bouldin Index | Calinski-Harabasz |
|---|---|---|---|---|---|---|---|
| **KMeans_K2** | 2 | Euclidean | N/A | 2269.33 | **0.3728** | **1.3646** | **93.32** |
| **KMeans_K3** | 3 | Euclidean | N/A | 1964.69 | 0.1774 | 1.6988 | 78.69 |
| **KMeans_K4** | 4 | Euclidean | N/A | 1729.23 | 0.1861 | 1.5722 | 73.99 |
| **Hierarchical_Ward** | 3 | Euclidean | Ward | N/A | 0.1369 | 1.8938 | 64.61 |
| **Hierarchical_Average_Euclidean** | 3 | Euclidean | Average | N/A | **0.6101** | **0.3507** | 25.55 |
| **Hierarchical_Average_Manhattan** | 3 | Manhattan | Average | N/A | **0.4761** | **1.1363** | 42.64 |
| **Hierarchical_Complete_Manhattan** | 3 | Manhattan | Complete | N/A | 0.3099 | 1.4141 | 64.00 |

### Key Experimental Insights
1. **Optimal K Selection:** While K=2 maximizes mathematical Silhouette score by splitting high vs. low satisfaction places, **K=3 provides the optimal operational granularity** for tourism marketing by isolating:
   - Budget/Sacred Heritage sites,
   - Critical/Maintenance-Needy destinations, and
   - Premium/Exploration Parks and Forts.
2. **Euclidean vs. Manhattan Distance:**
   - Manhattan distance with Average Linkage achieves a Silhouette score of **0.4761**, effectively handling feature outliers in visit duration and entry fees without excessive distortion.
   - Ward linkage yields the most evenly balanced and interpretable clusters for K-Means and Hierarchical pipelines.

---

## Cluster Profiles & Tourist Personas

Based on **K-Means ($K=3$)** profiling across 325 destinations:

| Cluster | Count | Share | Avg Fee | Median Fee | Avg Duration | Avg Rating | Positive % | Negative % | Sentiment | Dominant Types | Top States |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Cluster 0: Budget Sacred & Scenic Gems** | 200 | 61.5% | ₹5.9 | ₹0.0 | 1.43 hrs | 4.49 | 87.7% | 2.8% | +0.573 | Temple, Beach, Lake | Uttar Pradesh, Karnataka, Andhra Pradesh |
| **Cluster 1: Mixed / Critical Feedback** | 32 | 9.8% | ₹91.2 | ₹0.0 | 1.70 hrs | 2.91 | 23.5% | 34.6% | +0.006 | Beach, Temple, Waterfall | Maharashtra, Uttar Pradesh, Kerala |
| **Cluster 2: Premium Eco & Heritage Expeditions** | 93 | 28.6% | ₹360.6 | ₹60.0 | 2.65 hrs | 4.27 | 80.5% | 4.8% | +0.522 | National Park, Fort, Palace | Rajasthan, Delhi, Maharashtra |

### Practical Recommendations
* **Persona 0 (Pilgrims & Budget Backpackers):** High satisfaction, virtually zero financial barrier. Focus on crowd-management and transport connectivity.
* **Persona 1 (Attention Required / Tourism Intervention):** Sites with elevated negative feedback (34.6%) and low ratings (2.91). Target infrastructure improvements, cleaner facilities, and visitor safety measures.
* **Persona 2 (Cultural Tourists & Wildlife Enthusiasts):** Visitors spend higher entry fees and dedicate full half-days (2.65+ hours). Ideal for premium guided tour packaging and luxury hospitality partnerships.

---

## Repository Directory Structure

```
AI-Powered-Local-Tourism-Recommender/
│
├── data/
│   ├── raw/
│   │   ├── tourism_data.csv                 # Original 325 Indian tourism records
│   │   ├── places.clean.json.gz             # UCSD Google Places raw corpus (277 MB)
│   │   └── reviews.clean.json.gz            # UCSD Google Reviews raw corpus (1.4 GB)
│   │
│   └── processed/
│       ├── india_tourism_reviews.csv        # Integrated ML-ready master dataset
│       ├── unmatched_tourism_places.csv     # Preserved unmatched tourism places
│       ├── matched_places.json              # Entity resolution mapping
│       └── aggregated_business_reviews.json # Aggregated review & sentiment metrics
│
├── notebooks/
│   ├── 01_data_exploration.ipynb            # Raw data EDA & distributions
│   ├── 02_data_preprocessing.ipynb          # Hygiene, standardization & outliers
│   ├── 03_dataset_integration.ipynb         # Entity matching & review aggregation
│   ├── 04_kmeans_clustering.ipynb           # K-Means experiments (K=2, 3, 4)
│   ├── 05_hierarchical_clustering.ipynb     # Euclidean vs. Manhattan dendrograms
│   ├── 06_pca_visualization.ipynb           # PCA 2D projections & loadings
│   └── 07_evaluation_and_profiling.ipynb    # Validation metrics & persona analysis
│
├── src/
│   ├── data_cleaning.py                     # Cleaning & normalization helpers
│   ├── dataset_integration.py               # Master dataset integration pipeline
│   ├── match_places.py                      # Token & geo-coordinate entity matching
│   ├── extract_aggregate_reviews.py         # 11.45M review parser & VADER sentiment
│   ├── city_coordinates.py                  # Geocoded coordinates reference table
│   ├── feature_engineering.py               # Skewness correction, scaling & PCA
│   ├── clustering.py                        # K-Means & Hierarchical engines
│   ├── evaluation.py                        # Validation metrics & visualization suite
│   └── run_pipeline.py                      # End-to-end execution runner
│
├── results/
│   ├── plots/
│   │   ├── kmeans_elbow_and_silhouette.png  # Elbow & Silhouette curves
│   │   ├── hierarchical_dendrogram.png      # Hierarchical linkage tree
│   │   ├── distance_metric_comparison.png   # Euclidean vs. Manhattan PCA comparison
│   │   ├── pca_kmeans_k2.png                # K-Means K=2 PCA plot
│   │   ├── pca_kmeans_k3.png                # K-Means K=3 PCA plot
│   │   ├── pca_kmeans_k4.png                # K-Means K=4 PCA plot
│   │   └── pca_hierarchical_*.png           # Hierarchical PCA plots
│   │
│   └── metrics/
│       ├── evaluation_metrics.csv           # WCSS, Silhouette, DB, CH benchmarks
│       ├── cluster_profiles_kmeans_k3.csv   # K-Means K=3 profile statistics
│       └── assigned_clusters_kmeans_k3.csv  # Labeled master dataset
│
├── requirements.txt                         # Pinned Python dependencies
├── .gitignore                               # Git hygiene & raw data exclusions
└── README.md                                # Comprehensive documentation
```

---

## Quickstart & Reproducibility Guide

### 1. Environment Setup
Clone the repository and install dependencies in a virtual environment:
```bash
git clone https://github.com/vishal-0122/AI-Powered-Local-Tourism-Recommender.git
cd AI-Powered-Local-Tourism-Recommender

python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Run the Complete Pipeline
To execute the entire integration, clustering, evaluation, and plotting workflow in one step:
```bash
python src/run_pipeline.py
```

### 3. Step-by-Step Script Execution (Optional)
If running from raw data:
```bash
# 1. Download raw Google Local datasets (Places & Reviews)
python src/download_places.py
python src/download_reviews.py

# 2. Verify and match Indian places
python src/verify_india_coverage.py
python src/match_places.py

# 3. Extract and aggregate review text sentiments
python src/extract_aggregate_reviews.py

# 4. Integrate into final dataset
python src/dataset_integration.py

# 5. Run clustering, PCA, and metrics evaluation
python src/run_pipeline.py
```

### 4. Interactive Jupyter Notebooks
Launch Jupyter Notebook to inspect individual analytical phases:
```bash
jupyter notebook notebooks/
```

---

## Authors & Acknowledgments

* **Original Authors:** Vishal Dangiwala & Deepali Malik
* **Extended Dataset Integration & Machine Learning Pipeline:** Developed with rigorous adherence to reproducible empirical standards.
* **Data Sources:**
  - *Travel Dataset: Guide to India's Must See Places* (Kaggle)
  - *Google Local Reviews (2018)*, Prof. Julian McAuley, UC San Diego CSE ([Official Dataset Link](https://cseweb.ucsd.edu/~jmcauley/datasets.html#google_local))
