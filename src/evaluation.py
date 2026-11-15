import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.cluster.hierarchy import dendrogram

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

class ClusteringEvaluator:
    def __init__(self, output_plots_dir='results/plots', output_metrics_dir='results/metrics'):
        self.output_plots_dir = output_plots_dir
        self.output_metrics_dir = output_metrics_dir
        os.makedirs(output_plots_dir, exist_ok=True)
        os.makedirs(output_metrics_dir, exist_ok=True)

    def evaluate_models(self, X_scaled, models_dict):
        """
        Computes WCSS, Silhouette Score, Davies-Bouldin Index,
        and Calinski-Harabasz Index for all clustering models.
        """
        records = []
        for name, info in models_dict.items():
            labels = info['labels']
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            
            if n_clusters < 2:
                continue
                
            sil = silhouette_score(X_scaled, labels)
            db = davies_bouldin_score(X_scaled, labels)
            ch = calinski_harabasz_score(X_scaled, labels)
            inertia = info.get('inertia', np.nan)
            
            records.append({
                'Model': name,
                'K': n_clusters,
                'Metric_Type': info.get('metric', 'euclidean'),
                'Linkage': info.get('linkage', 'N/A'),
                'WCSS_Inertia': round(inertia, 2) if not np.isnan(inertia) else 'N/A',
                'Silhouette_Score': round(sil, 4),
                'Davies_Bouldin_Index': round(db, 4),
                'Calinski_Harabasz_Index': round(ch, 2)
            })
            
        metrics_df = pd.DataFrame(records)
        metrics_path = os.path.join(self.output_metrics_dir, 'evaluation_metrics.csv')
        metrics_df.to_csv(metrics_path, index=False)
        print(f"Saved evaluation metrics to {metrics_path}")
        return metrics_df

    def plot_elbow_and_silhouette_curve(self, X_scaled, k_range=range(2, 11)):
        """
        Plots WCSS Elbow curve and Silhouette Score curve for K=2 to 10.
        """
        from sklearn.cluster import KMeans
        inertias = []
        silhouettes = []
        
        for k in k_range:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X_scaled)
            inertias.append(km.inertia_)
            silhouettes.append(silhouette_score(X_scaled, labels))
            
        fig, ax1 = plt.subplots(figsize=(9, 5))
        
        color = '#1f77b4'
        ax1.set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Inertia / WCSS', color=color, fontsize=12, fontweight='bold')
        line1 = ax1.plot(list(k_range), inertias, marker='o', linewidth=2, color=color, label='WCSS (Elbow)')
        ax1.tick_params(axis='y', labelcolor=color)
        
        ax2 = ax1.twinx()
        color = '#2ca02c'
        ax2.set_ylabel('Silhouette Score', color=color, fontsize=12, fontweight='bold')
        line2 = ax2.plot(list(k_range), silhouettes, marker='s', linestyle='--', linewidth=2, color=color, label='Silhouette Score')
        ax2.tick_params(axis='y', labelcolor=color)
        
        # Highlight optimal K
        best_k = list(k_range)[np.argmax(silhouettes)]
        ax2.axvline(x=best_k, color='#d62728', linestyle=':', label=f'Peak Silhouette (K={best_k})')
        
        plt.title('K-Means Optimization: Elbow Method & Silhouette Scores', fontsize=14, fontweight='bold', pad=15)
        fig.tight_layout()
        
        save_path = os.path.join(self.output_plots_dir, 'kmeans_elbow_and_silhouette.png')
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"Saved elbow and silhouette plot to {save_path}")

    def plot_pca_clusters(self, X_pca, models_dict, var_ratio):
        """
        Generates 2D PCA cluster scatter plots for each model.
        """
        for name, info in models_dict.items():
            labels = info['labels']
            k = len(np.unique(labels))
            palette = sns.color_palette('tab10', k)
            
            plt.figure(figsize=(8, 6))
            for cluster_id in range(k):
                mask = labels == cluster_id
                plt.scatter(
                    X_pca[mask, 0],
                    X_pca[mask, 1],
                    label=f'Cluster {cluster_id}',
                    color=palette[cluster_id],
                    s=60,
                    alpha=0.8,
                    edgecolors='white',
                    linewidth=0.5
                )
                
            plt.title(f'{name} (K={k}) — PCA 2D Cluster Space', fontsize=13, fontweight='bold', pad=12)
            plt.xlabel(f'PCA Component 1 ({var_ratio[0]*100:.1f}% Variance)', fontsize=11)
            plt.ylabel(f'PCA Component 2 ({var_ratio[1]*100:.1f}% Variance)', fontsize=11)
            plt.legend(frameon=True, facecolor='white', framealpha=0.9)
            plt.tight_layout()
            
            save_name = f'pca_{name.lower()}.png'
            save_path = os.path.join(self.output_plots_dir, save_name)
            plt.savefig(save_path, dpi=300)
            plt.close()
            print(f"Saved PCA plot to {save_path}")

    def plot_dendrogram(self, Z, title='Hierarchical Clustering Dendrogram (Ward Linkage)'):
        """
        Plots and saves hierarchical clustering dendrogram.
        """
        plt.figure(figsize=(12, 6))
        dendrogram(
            Z,
            orientation='top',
            truncate_mode='lastp',
            p=30,
            show_leaf_counts=True,
            leaf_rotation=90,
            leaf_font_size=10
        )
        plt.title(title, fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Tourist Destinations / Cluster Size', fontsize=12)
        plt.ylabel('Ward Linkage Distance', fontsize=12)
        plt.tight_layout()
        
        save_path = os.path.join(self.output_plots_dir, 'hierarchical_dendrogram.png')
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"Saved dendrogram to {save_path}")

    def plot_distance_comparison(self, X_pca, hc_res, var_ratio):
        """
        Side-by-side comparison of Euclidean (Ward) vs Manhattan (Average).
        """
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        comparisons = [
            ('Hierarchical_Euclidean_Ward', axes[0], 'Euclidean Distance (Ward Linkage)'),
            ('Hierarchical_Manhattan_Average', axes[1], 'Manhattan Distance (Average Linkage)')
        ]
        
        for model_key, ax, title in comparisons:
            if model_key not in hc_res:
                continue
            labels = hc_res[model_key]['labels']
            k = len(np.unique(labels))
            palette = sns.color_palette('Set1', k)
            
            for cluster_id in range(k):
                mask = labels == cluster_id
                ax.scatter(
                    X_pca[mask, 0],
                    X_pca[mask, 1],
                    label=f'Cluster {cluster_id}',
                    color=palette[cluster_id],
                    s=60,
                    alpha=0.8,
                    edgecolors='white',
                    linewidth=0.5
                )
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xlabel(f'PCA Component 1 ({var_ratio[0]*100:.1f}%)')
            ax.set_ylabel(f'PCA Component 2 ({var_ratio[1]*100:.1f}%)')
            ax.legend(frameon=True, facecolor='white', framealpha=0.9)
            
        plt.suptitle('Hierarchical Clustering: Euclidean vs. Manhattan Distance Metric Comparison', fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        save_path = os.path.join(self.output_plots_dir, 'distance_metric_comparison.png')
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"Saved distance comparison plot to {save_path}")

    def profile_clusters(self, df: pd.DataFrame, labels, model_name='KMeans_K3'):
        """
        Calculates cluster profiles with mean, median, and categorical distributions.
        """
        df_copy = df.copy()
        df_copy['Cluster'] = labels
        
        numeric_cols = [
            'entry_fee', 'visit_duration', 'avg_rating',
            'review_count', 'positive_review_pct', 'negative_review_pct', 'sentiment_score'
        ]
        
        profile = df_copy.groupby('Cluster')[numeric_cols].agg(['mean', 'median', 'std'])
        counts = df_copy.groupby('Cluster')['place_name'].count()
        
        # Detailed profile summary
        summary_rows = []
        for c in sorted(df_copy['Cluster'].unique()):
            sub = df_copy[df_copy['Cluster'] == c]
            top_cats = ", ".join(sub['category'].value_counts().head(3).index.tolist())
            top_states = ", ".join(sub['state'].value_counts().head(3).index.tolist())
            
            summary_rows.append({
                'Cluster': c,
                'Place_Count': len(sub),
                'Percentage': round(len(sub) * 100 / len(df_copy), 1),
                'Avg_Entry_Fee_INR': round(sub['entry_fee'].mean(), 1),
                'Median_Entry_Fee_INR': round(sub['entry_fee'].median(), 1),
                'Avg_Visit_Duration_Hours': round(sub['visit_duration'].mean(), 2),
                'Avg_Rating': round(sub['avg_rating'].mean(), 2),
                'Avg_Review_Count': int(round(sub['review_count'].mean())),
                'Avg_Positive_Review_Pct': round(sub['positive_review_pct'].mean(), 1),
                'Avg_Negative_Review_Pct': round(sub['negative_review_pct'].mean(), 1),
                'Avg_Sentiment_Score': round(sub['sentiment_score'].mean(), 3),
                'Top_Categories': top_cats,
                'Top_States': top_states
            })
            
        summary_df = pd.DataFrame(summary_rows)
        csv_path = os.path.join(self.output_metrics_dir, f'cluster_profiles_{model_name.lower()}.csv')
        summary_df.to_csv(csv_path, index=False)
        print(f"Saved cluster profile to {csv_path}")
        
        # Save cluster assignments on data
        assigned_path = os.path.join(self.output_metrics_dir, f'assigned_clusters_{model_name.lower()}.csv')
        df_copy.to_csv(assigned_path, index=False)
        
        return summary_df
