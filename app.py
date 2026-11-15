import os
import json
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.metrics.pairwise import euclidean_distances

# Import Liquid Glass Design System
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from liquid_glass_theme import get_liquid_glass_svg_filters, get_liquid_glass_css, get_apple_plotly_layout

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & APPLE LIQUID GLASS INJECTION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI-Powered Local Tourism Recommender | Liquid Glass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject SVG optical refraction filters and Liquid Glass CSS
st.markdown(get_liquid_glass_svg_filters(), unsafe_allow_html=True)
st.markdown(get_liquid_glass_css(), unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_all_data():
    df_path = os.path.join('data', 'processed', 'india_tourism_reviews.csv')
    if not os.path.exists(df_path):
        st.error(f"Missing master dataset at {df_path}. Run ML pipeline first.")
        st.stop()
    df = pd.read_csv(df_path)
    
    # Load evaluation metrics
    metrics_path = os.path.join('results', 'metrics', 'evaluation_metrics.csv')
    metrics_df = pd.read_csv(metrics_path) if os.path.exists(metrics_path) else pd.DataFrame()
    
    # Load cluster profiles
    profiles_path = os.path.join('results', 'metrics', 'cluster_profiles_kmeans_k3.csv')
    profiles_df = pd.read_csv(profiles_path) if os.path.exists(profiles_path) else pd.DataFrame()
    
    # Load assigned clusters
    assigned_path = os.path.join('results', 'metrics', 'assigned_clusters_kmeans_k3.csv')
    if os.path.exists(assigned_path):
        df_assigned = pd.read_csv(assigned_path)
    else:
        df_assigned = df.copy()
        df_assigned['Cluster'] = 0
        
    return df, metrics_df, profiles_df, df_assigned

df, metrics_df, profiles_df, df_assigned = load_all_data()
APPLE_PLOTLY_THEME = get_apple_plotly_layout()

# -----------------------------------------------------------------------------
# 3. APPLE TRANSLUCENT FLOATING SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    # macOS Window Controls & Branding
    st.markdown("""
    <div class="macos-header">
        <div class="macos-traffic-lights">
            <span class="traffic-light light-red"></span>
            <span class="traffic-light light-yellow"></span>
            <span class="traffic-light light-green"></span>
        </div>
        <div style="font-size: 0.72rem; color: rgba(255,255,255,0.4); font-weight: 600; letter-spacing: 0.5px;">
            MACOS 15 • LIQUID GLASS
        </div>
    </div>
    <div style="padding: 0 0 18px 4px;">
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
            <div style="width: 28px; height: 28px; border-radius: 8px; background: linear-gradient(135deg, #0a84ff 0%, #5e5ce6 100%); display: flex; align-items: center; justify-content: center; font-size: 14px; box-shadow: 0 4px 10px rgba(10, 132, 255, 0.4);">
                🧭
            </div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; letter-spacing: -0.3px;">
                Tourism Discovery
            </div>
        </div>
        <div style="font-size: 0.8rem; color: rgba(255, 255, 255, 0.5); padding-left: 38px;">
            Unsupervised Suite
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Apple Navigation Menu
    menu = st.radio(
        "Navigation",
        [
            "🌟 Executive Overview",
            "📊 Exploratory Data Analysis",
            "🔬 Interactive Clustering Studio",
            "🗺️ Geospatial Tourism Map",
            "🌌 2D & 3D PCA Space",
            "📈 Benchmark & Distance Comparison",
            "👤 Personas & Cluster Profiles",
            "🎯 Smart Destination Recommender",
            "💾 Data Catalog & Export"
        ],
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # macOS Status Pill & Architecture Badges
    st.markdown("""
    <div class="glass-card" style="padding: 14px 16px; margin-top: 12px; border-radius: 16px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #30d158; box-shadow: 0 0 8px #30d158; display: inline-block;"></span>
            <span style="font-size: 0.78rem; font-weight: 600; color: #ffffff;">System Status: Online</span>
        </div>
        <div style="font-size: 0.72rem; color: rgba(255, 255, 255, 0.55); line-height: 1.6;">
            • <b>Dataset:</b> 325 Indian Destinations<br>
            • <b>Reviews:</b> 645K+ UCSD Google Corpus<br>
            • <b>NLP Model:</b> VADER Polarity Scoring<br>
            • <b>Clustering:</b> K-Means & Agglomerative
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW (APPLE LIQUID GLASS HERO & KPIS)
# -----------------------------------------------------------------------------
if menu == "🌟 Executive Overview":
    # 1. Floating Hero Glass Slab
    st.markdown("""
    <div class="glass-panel" style="padding: 40px 44px; margin-bottom: 28px;">
        <div class="glass-pill" style="margin-bottom: 16px;">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: #64d2ff; display: inline-block;"></span>
            INTELLIGENT TOURISM DISCOVERY PLATFORM
        </div>
        <div style="font-size: 2.75rem; font-weight: 800; letter-spacing: -1px; color: #ffffff; line-height: 1.15; margin-bottom: 14px;">
            AI-Powered Local Tourism Recommender
        </div>
        <div style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.72); line-height: 1.65; max-width: 980px; font-weight: 400;">
            An intelligent tourism discovery platform combining Indian destination information, Google Local reviews, 
            sentiment analysis and unsupervised machine learning to uncover geographic hotspots, behavioral spending patterns, 
            and traveler satisfaction.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Apple Liquid Glass KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="apple-metric-card">
            <div class="metric-accent-line" style="background: linear-gradient(90deg, #0a84ff, transparent);"></div>
            <div class="metric-title">Destinations</div>
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-subtitle">
                <span style="color: #64d2ff;">33 States Covered</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="apple-metric-card">
            <div class="metric-accent-line" style="background: linear-gradient(90deg, #64d2ff, transparent);"></div>
            <div class="metric-title">Google Reviews</div>
            <div class="metric-value">645K+</div>
            <div class="metric-subtitle">
                <span style="color: #30d158;">Verified Indian Corpus</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="apple-metric-card">
            <div class="metric-accent-line" style="background: linear-gradient(90deg, #ffd60a, transparent);"></div>
            <div class="metric-title">Mean Rating</div>
            <div class="metric-value">{df['avg_rating'].mean():.2f} ★</div>
            <div class="metric-subtitle">
                <span style="color: #ffd60a;">Scale: 1.0 – 5.0</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="apple-metric-card">
            <div class="metric-accent-line" style="background: linear-gradient(90deg, #30d158, transparent);"></div>
            <div class="metric-title">Positive Feedback</div>
            <div class="metric-value">{df['positive_review_pct'].mean():.1f}%</div>
            <div class="metric-subtitle">
                <span style="color: #30d158;">4.0+ Star Ratings</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown(f"""
        <div class="apple-metric-card">
            <div class="metric-accent-line" style="background: linear-gradient(90deg, #bf5af2, transparent);"></div>
            <div class="metric-title">Mean Sentiment</div>
            <div class="metric-value">+{df['sentiment_score'].mean():.3f}</div>
            <div class="metric-subtitle">
                <span style="color: #bf5af2;">VADER Polarity [-1, +1]</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # 3. Main Dashboard Panels: Integration Flow & Quick Lookahead
    col_left, col_right = st.columns([1.15, 0.85])
    
    with col_left:
        st.markdown("""
        <div class="glass-panel" style="padding: 28px 30px;">
            <div class="macos-header" style="margin-bottom: 18px; padding-bottom: 12px;">
                <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">
                    Dataset Integration Architecture
                </div>
                <div class="glass-pill" style="font-size: 0.72rem; padding: 4px 10px;">
                    180,686 Verified Places
                </div>
            </div>
            <p style="color: rgba(255, 255, 255, 0.68); font-size: 0.88rem; line-height: 1.6; margin-bottom: 20px;">
                End-to-end data pipeline harmonizing Indian destinations with Google Local reviews:
            </p>
            <div style="display: grid; gap: 10px;">
                <div class="glass-card" style="padding: 12px 18px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.85rem; color: #ffffff; font-weight: 600;">1. Primary Tourism Dataset</span>
                    <span class="glass-pill" style="font-size: 0.72rem;">data.csv (325 Destinations)</span>
                </div>
                <div class="glass-card" style="padding: 12px 18px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.85rem; color: #ffffff; font-weight: 600;">2. UCSD Google Places Corpus</span>
                    <span class="glass-pill" style="font-size: 0.72rem;">3.11M Total → 180,686 In-Bounds</span>
                </div>
                <div class="glass-card" style="padding: 12px 18px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.85rem; color: #ffffff; font-weight: 600;">3. Entity Matching & Resolution</span>
                    <span class="glass-pill" style="font-size: 0.72rem;">281 Matched (86.5%) • 44 Preserved</span>
                </div>
                <div class="glass-card" style="padding: 12px 18px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.85rem; color: #ffffff; font-weight: 600;">4. Review Sentiment Extraction</span>
                    <span class="glass-pill" style="font-size: 0.72rem;">645K Indian Reviews • VADER Polarity</span>
                </div>
                <div class="glass-card" style="padding: 12px 18px; display: flex; align-items: center; justify-content: space-between; border-color: rgba(10, 132, 255, 0.35); background: rgba(10, 132, 255, 0.08);">
                    <span style="font-size: 0.85rem; color: #64d2ff; font-weight: 600;">5. Integrated ML Master Table</span>
                    <span class="glass-pill" style="font-size: 0.72rem; border-color: #64d2ff; color: #64d2ff;">india_tourism_reviews.csv</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="glass-panel" style="padding: 28px 30px;">
            <div class="macos-header" style="margin-bottom: 18px; padding-bottom: 12px;">
                <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff;">
                    Quick Destination Lookahead
                </div>
                <div class="glass-pill" style="font-size: 0.72rem; padding: 4px 10px;">
                    Preview Sample
                </div>
            </div>
            <p style="color: rgba(255, 255, 255, 0.68); font-size: 0.88rem; line-height: 1.6; margin-bottom: 16px;">
                Verified destinations with enriched reviews and sentiment scores:
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.dataframe(
            df[['place_name', 'state', 'category', 'avg_rating', 'sentiment_score']].head(8),
            use_container_width=True
        )

# -----------------------------------------------------------------------------
# PAGE 2: EXPLORATORY DATA ANALYSIS (EDA)
# -----------------------------------------------------------------------------
elif menu == "📊 Exploratory Data Analysis":
    st.markdown("""
    <div class="glass-panel" style="padding: 32px 36px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 12px;">DATASET INSIGHTS</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; margin-bottom: 8px;">
            Exploratory Data Analysis
        </div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.7);">
            Inspect spatial coverage across 33 states, economic distributions, and multi-attribute correlation patterns.
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["State & Category Coverage", "Economic Distributions & Skewness", "Multi-Attribute Correlations"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            top_states = df['state'].value_counts().head(12).reset_index()
            top_states.columns = ['State', 'Destinations']
            fig_states = px.bar(
                top_states, x='Destinations', y='State', orientation='h',
                title="Top 12 Indian States by Featured Destinations",
                color='Destinations', color_continuous_scale=['#0a84ff', '#5e5ce6', '#bf5af2']
            )
            fig_states.update_layout(**APPLE_PLOTLY_THEME)
            fig_states.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_states, use_container_width=True)

        with col_b:
            top_cats = df['category'].value_counts().head(8).reset_index()
            top_cats.columns = ['Category', 'Count']
            fig_cats = px.pie(
                top_cats, names='Category', values='Count',
                title="Top Destination Categories",
                hole=0.55,
                color_discrete_sequence=['#0a84ff', '#30d158', '#ffd60a', '#ff9f0a', '#bf5af2', '#ff375f', '#64d2ff', '#5e5ce6']
            )
            fig_cats.update_layout(**APPLE_PLOTLY_THEME)
            st.plotly_chart(fig_cats, use_container_width=True)

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            fig_fee = px.histogram(
                df, x='entry_fee', nbins=30,
                title="Raw Entrance Fee (INR) — High Positive Skewness",
                color_discrete_sequence=['#64d2ff']
            )
            fig_fee.update_layout(**APPLE_PLOTLY_THEME)
            st.plotly_chart(fig_fee, use_container_width=True)

        with col_d:
            df['log_fee'] = np.log1p(df['entry_fee'])
            fig_log_fee = px.histogram(
                df, x='log_fee', nbins=30,
                title="Log1p Transformed Entrance Fee (Normal Distribution for ML)",
                color_discrete_sequence=['#30d158']
            )
            fig_log_fee.update_layout(**APPLE_PLOTLY_THEME)
            st.plotly_chart(fig_log_fee, use_container_width=True)

    with tab3:
        corr_cols = ['entry_fee', 'visit_duration', 'avg_rating', 'review_count', 'positive_review_pct', 'negative_review_pct', 'sentiment_score']
        corr_matrix = df[corr_cols].corr()
        fig_corr = px.imshow(
            corr_matrix, text_auto=".2f", aspect="auto",
            title="Correlation Matrix of Numerical Tourism Features",
            color_continuous_scale="RdBu_r"
        )
        fig_corr.update_layout(**APPLE_PLOTLY_THEME)
        st.plotly_chart(fig_corr, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 3: INTERACTIVE CLUSTERING STUDIO
# -----------------------------------------------------------------------------
elif menu == "🔬 Interactive Clustering Studio":
    st.markdown("""
    <div class="glass-panel" style="padding: 32px 36px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 12px;">MACHINE LEARNING LAB</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; margin-bottom: 8px;">
            Interactive Clustering Studio
        </div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.7);">
            Live parameter tuning for K-Means and Hierarchical Clustering with real-time validation feedback.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_view = st.columns([1, 2.3])

    with col_ctrl:
        st.markdown("""
        <div class="glass-panel" style="padding: 24px 26px;">
            <div style="font-size: 1rem; font-weight: 700; color: #ffffff; margin-bottom: 14px;">
                Hyperparameter Tuning
            </div>
        """, unsafe_allow_html=True)
        
        algorithm = st.selectbox("Clustering Algorithm", ["K-Means", "Agglomerative (Hierarchical)"])
        k_val = st.slider("Number of Clusters (K)", min_value=2, max_value=8, value=3)
        
        if algorithm == "Agglomerative (Hierarchical)":
            metric_choice = st.selectbox("Distance Metric", ["euclidean", "manhattan"])
            if metric_choice == "euclidean":
                linkage_choice = st.selectbox("Linkage Method", ["ward", "average", "complete"])
            else:
                linkage_choice = st.selectbox("Linkage Method", ["average", "complete"])
        else:
            metric_choice = "euclidean"
            linkage_choice = "N/A"

        feature_set = st.radio(
            "Feature Engineering Focus",
            [
                "Comprehensive (Spatial + Cost + Sentiment)",
                "Spatial Only (Latitude + Longitude)",
                "Economic & Duration (Fee + Duration)",
                "Experience & Reputation (Rating + Sentiment + Reviews)"
            ]
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Prepare features based on user selection
    df_studio = df.copy()
    df_studio['entry_fee_log'] = np.log1p(df_studio['entry_fee'])
    df_studio['review_count_log'] = np.log1p(df_studio['review_count'])

    if feature_set.startswith("Comprehensive"):
        features_used = ['latitude', 'longitude', 'entry_fee_log', 'visit_duration', 'avg_rating', 'review_count_log', 'positive_review_pct', 'negative_review_pct', 'sentiment_score']
    elif feature_set.startswith("Spatial"):
        features_used = ['latitude', 'longitude', 'review_count_log']
    elif feature_set.startswith("Economic"):
        features_used = ['entry_fee_log', 'visit_duration']
    else:
        features_used = ['avg_rating', 'review_count_log', 'positive_review_pct', 'negative_review_pct', 'sentiment_score']

    scaler = StandardScaler()
    X_studio = scaler.fit_transform(df_studio[features_used].values)

    # Run clustering live
    if algorithm == "K-Means":
        model = KMeans(n_clusters=k_val, random_state=42, n_init=10)
        labels = model.fit_predict(X_studio)
        inertia_val = f"{model.inertia_:.1f}"
    else:
        model = AgglomerativeClustering(n_clusters=k_val, metric=metric_choice, linkage=linkage_choice)
        labels = model.fit_predict(X_studio)
        inertia_val = "N/A"

    df_studio['Cluster'] = [f"Cluster {l}" for l in labels]

    # Metrics calculation
    sil = silhouette_score(X_studio, labels)
    db = davies_bouldin_score(X_studio, labels)
    ch = calinski_harabasz_score(X_studio, labels)

    with col_view:
        # Live score metrics cards
        sc1, sc2, sc3, sc4 = st.columns(4)
        with sc1:
            st.markdown(f"""
            <div class="apple-metric-card">
                <div class="metric-title">Silhouette</div>
                <div class="metric-value">{sil:.4f}</div>
                <div class="metric-subtitle">Range: [-1, +1]</div>
            </div>
            """, unsafe_allow_html=True)
        with sc2:
            st.markdown(f"""
            <div class="apple-metric-card">
                <div class="metric-title">Davies-Bouldin</div>
                <div class="metric-value">{db:.4f}</div>
                <div class="metric-subtitle">Lower is Better</div>
            </div>
            """, unsafe_allow_html=True)
        with sc3:
            st.markdown(f"""
            <div class="apple-metric-card">
                <div class="metric-title">Calinski-Harabasz</div>
                <div class="metric-value">{ch:.1f}</div>
                <div class="metric-subtitle">Higher is Better</div>
            </div>
            """, unsafe_allow_html=True)
        with sc4:
            st.markdown(f"""
            <div class="apple-metric-card">
                <div class="metric-title">WCSS Inertia</div>
                <div class="metric-value">{inertia_val}</div>
                <div class="metric-subtitle">Compactness</div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        
        # 2D PCA representation
        pca = PCA(n_components=2, random_state=42)
        X_pca_studio = pca.fit_transform(X_studio)
        df_studio['PCA1'] = X_pca_studio[:, 0]
        df_studio['PCA2'] = X_pca_studio[:, 1]

        fig_cluster = px.scatter(
            df_studio, x='PCA1', y='PCA2', color='Cluster',
            hover_name='place_name',
            hover_data=['state', 'category', 'entry_fee', 'avg_rating', 'sentiment_score'],
            title=f"2D PCA Projection: {algorithm} (K={k_val}, Metric={metric_choice})",
            color_discrete_sequence=['#0a84ff', '#30d158', '#ff9f0a', '#bf5af2', '#ff375f', '#64d2ff', '#ffd60a', '#5e5ce6']
        )
        fig_cluster.update_layout(**APPLE_PLOTLY_THEME)
        fig_cluster.update_traces(marker=dict(size=9, opacity=0.88, line=dict(width=0.8, color='rgba(255,255,255,0.7)')))
        st.plotly_chart(fig_cluster, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 4: GEOSPATIAL MAP
# -----------------------------------------------------------------------------
elif menu == "🗺️ Geospatial Tourism Map":
    st.markdown("""
    <div class="glass-panel" style="padding: 32px 36px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 12px;">GEOGRAPHIC VISUALIZATION</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; margin-bottom: 8px;">
            Interactive Geospatial Tourism Map
        </div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.7);">
            Explore tourist hotspots across India bounded by sovereign coordinates and cluster personas.
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig_map = px.scatter_geo(
        df_assigned,
        lat='latitude',
        lon='longitude',
        color='Cluster',
        hover_name='place_name',
        hover_data=['state', 'category', 'entry_fee', 'avg_rating', 'sentiment_score'],
        size='avg_rating',
        projection="natural earth",
        title="Destination Hotspots across India",
        color_continuous_scale="Viridis"
    )
    fig_map.update_geos(
        fitbounds="locations",
        visible=False,
        showcountries=True,
        countrycolor="rgba(255,255,255,0.2)",
        showland=True,
        landcolor="#070d1a",
        showsubunits=True,
        subunitcolor="rgba(255,255,255,0.12)"
    )
    fig_map.update_layout(**APPLE_PLOTLY_THEME)
    fig_map.update_layout(height=650)
    st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 5: 2D & 3D PCA SPACE
# -----------------------------------------------------------------------------
elif menu == "🌌 2D & 3D PCA Space":
    st.markdown("""
    <div class="glass-panel" style="padding: 32px 36px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 12px;">LATENT MANIFOLD</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; margin-bottom: 8px;">
            Principal Component Analysis (PCA)
        </div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.7);">
            Rotatable 3D coordinate projection and component eigenvector loadings matrix.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Compute 3D PCA
    fe_cols = ['latitude', 'longitude', 'entry_fee', 'visit_duration', 'avg_rating', 'review_count', 'positive_review_pct', 'negative_review_pct', 'sentiment_score']
    X_all = StandardScaler().fit_transform(df[fe_cols].values)
    pca_3d = PCA(n_components=3, random_state=42)
    X_pca3 = pca_3d.fit_transform(X_all)
    
    df_assigned['PC1'] = X_pca3[:, 0]
    df_assigned['PC2'] = X_pca3[:, 1]
    df_assigned['PC3'] = X_pca3[:, 2]

    col_3d, col_loadings = st.columns([1.5, 1])

    with col_3d:
        fig_3d = px.scatter_3d(
            df_assigned, x='PC1', y='PC2', z='PC3',
            color='Cluster', hover_name='place_name',
            title=f"3D PCA Projection ({pca_3d.explained_variance_ratio_.sum()*100:.1f}% Variance Explained)",
            color_discrete_sequence=['#0a84ff', '#30d158', '#ff9f0a']
        )
        fig_3d.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='-apple-system, BlinkMacSystemFont, sans-serif', color='rgba(255,255,255,0.85)'),
            scene=dict(
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.08)"),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.08)"),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.08)")
            ),
            height=620
        )
        st.plotly_chart(fig_3d, use_container_width=True)

    with col_loadings:
        loadings = pd.DataFrame(
            pca_3d.components_.T,
            index=fe_cols,
            columns=['PC1', 'PC2', 'PC3']
        )
        fig_loadings = px.imshow(
            loadings, text_auto=".2f", aspect="auto",
            title="Eigenvector Feature Loadings",
            color_continuous_scale="Purples"
        )
        fig_loadings.update_layout(**APPLE_PLOTLY_THEME)
        fig_loadings.update_layout(height=620)
        st.plotly_chart(fig_loadings, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 6: BENCHMARK & DISTANCE COMPARISON
# -----------------------------------------------------------------------------
elif menu == "📈 Benchmark & Distance Comparison":
    st.markdown("""
    <div class="glass-panel" style="padding: 32px 36px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 12px;">QUANTITATIVE BENCHMARKS</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; margin-bottom: 8px;">
            Model Benchmarks & Distance Comparison
        </div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.7);">
            Empirical comparison across WCSS, Silhouette, Davies-Bouldin, and Euclidean vs. Manhattan distance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not metrics_df.empty:
        st.markdown("<div class='glass-panel' style='padding: 24px 28px;'><h4 style='color:#fff; margin-top:0;'>Clustering Validation Scoreboard</h4>", unsafe_allow_html=True)
        st.dataframe(metrics_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    col_plot1, col_plot2 = st.columns(2)
    with col_plot1:
        elbow_img = os.path.join('results', 'plots', 'kmeans_elbow_and_silhouette.png')
        if os.path.exists(elbow_img):
            st.image(elbow_img, caption="K-Means Elbow & Silhouette Curve (K=2 to 10)", use_container_width=True)

    with col_plot2:
        dist_img = os.path.join('results', 'plots', 'distance_metric_comparison.png')
        if os.path.exists(dist_img):
            st.image(dist_img, caption="Euclidean (Ward) vs. Manhattan (Average) Linkage", use_container_width=True)

    dendro_img = os.path.join('results', 'plots', 'hierarchical_dendrogram.png')
    if os.path.exists(dendro_img):
        st.image(dendro_img, caption="Hierarchical Clustering Dendrogram (Ward Linkage)", use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 7: CLUSTER PERSONAS & PROFILES
# -----------------------------------------------------------------------------
elif menu == "👤 Personas & Cluster Profiles":
    st.markdown("""
    <div class="glass-panel" style="padding: 32px 36px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 12px;">BEHAVIORAL SEGMENTATION</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; margin-bottom: 8px;">
            Tourist Personas & Behavioral Profiles
        </div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.7);">
            Interpreted destination archetypes derived from K-Means (K=3) profiling.
        </div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div class="glass-panel" style="border-top: 2px solid #64d2ff; padding: 26px 24px;">
            <div style="font-size:0.75rem; color:#64d2ff; font-weight:700; text-transform:uppercase; letter-spacing:0.6px;">CLUSTER 0 (61.5%)</div>
            <div style="font-size:1.35rem; font-weight:700; color:#fff; margin:6px 0 10px 0;">Budget Sacred & Scenic</div>
            <p style="color:rgba(255,255,255,0.65); font-size:0.85rem; line-height:1.5; margin-bottom:16px;">
                High satisfaction, negligible entry fees, cultural and spiritual pilgrimage sites.
            </p>
            <div style="font-size:0.82rem; color:rgba(255,255,255,0.85); line-height:1.8;">
                • <b>Avg Entry Fee:</b> ₹5.9 (Median ₹0.0)<br>
                • <b>Avg Duration:</b> 1.43 Hours<br>
                • <b>Avg Rating:</b> 4.49 ★ (87.7% Positive)<br>
                • <b>Sentiment:</b> +0.573<br>
                • <b>Sites:</b> Temples, Beaches, Lakes<br>
                • <b>Target:</b> Pilgrims & Backpackers
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown("""
        <div class="glass-panel" style="border-top: 2px solid #ff375f; padding: 26px 24px;">
            <div style="font-size:0.75rem; color:#ff375f; font-weight:700; text-transform:uppercase; letter-spacing:0.6px;">CLUSTER 1 (9.8%)</div>
            <div style="font-size:1.35rem; font-weight:700; color:#fff; margin:6px 0 10px 0;">Critical Feedback Sites</div>
            <p style="color:rgba(255,255,255,0.65); font-size:0.85rem; line-height:1.5; margin-bottom:16px;">
                Destinations receiving polarizing reviews requiring maintenance and crowd intervention.
            </p>
            <div style="font-size:0.82rem; color:rgba(255,255,255,0.85); line-height:1.8;">
                • <b>Avg Entry Fee:</b> ₹91.2<br>
                • <b>Avg Duration:</b> 1.70 Hours<br>
                • <b>Avg Rating:</b> 2.91 ★ (34.6% Negative)<br>
                • <b>Sentiment:</b> +0.006 (Neutral/Low)<br>
                • <b>Sites:</b> Crowded beaches, shrines<br>
                • <b>Target:</b> Infrastructure Improvement
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown("""
        <div class="glass-panel" style="border-top: 2px solid #30d158; padding: 26px 24px;">
            <div style="font-size:0.75rem; color:#30d158; font-weight:700; text-transform:uppercase; letter-spacing:0.6px;">CLUSTER 2 (28.6%)</div>
            <div style="font-size:1.35rem; font-weight:700; color:#fff; margin:6px 0 10px 0;">Premium Eco & Heritage</div>
            <p style="color:rgba(255,255,255,0.65); font-size:0.85rem; line-height:1.5; margin-bottom:16px;">
                Higher ticket prices, extended visits, premier national monuments & safari parks.
            </p>
            <div style="font-size:0.82rem; color:rgba(255,255,255,0.85); line-height:1.8;">
                • <b>Avg Entry Fee:</b> ₹360.6 (Median ₹60)<br>
                • <b>Avg Duration:</b> 2.65 Hours<br>
                • <b>Avg Rating:</b> 4.27 ★ (80.5% Positive)<br>
                • <b>Sentiment:</b> +0.522<br>
                • <b>Sites:</b> National Parks, Forts, Palaces<br>
                • <b>Target:</b> Heritage Tourists & Guided Tours
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not profiles_df.empty:
        st.markdown("<div class='glass-panel' style='padding: 24px 28px;'><h4 style='color:#fff; margin-top:0;'>Statistical Cluster Profile Summary</h4>", unsafe_allow_html=True)
        st.dataframe(profiles_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 8: SMART DESTINATION RECOMMENDER
# -----------------------------------------------------------------------------
elif menu == "🎯 Smart Destination Recommender":
    st.markdown("""
    <div class="glass-panel" style="padding: 32px 36px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 12px;">AI RECOMMENDATION ENGINE</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; margin-bottom: 8px;">
            Smart Destination Recommender
        </div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.7);">
            Discover personalized travel recommendations using cluster neighborhoods and multi-attribute similarity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    rec_tab1, rec_tab2 = st.tabs(["Find Similar to a Destination", "Preference-Based Search"])

    # Normalized feature matrix for similarity calculations
    num_features = ['latitude', 'longitude', 'entry_fee', 'visit_duration', 'avg_rating', 'review_count', 'sentiment_score']
    scaler = StandardScaler()
    X_norm = scaler.fit_transform(df[num_features].values)

    with rec_tab1:
        st.write("Pick a place you enjoyed, and the system finds the closest destinations in learned latent space:")
        dest_choice = st.selectbox("Select Benchmark Destination", options=sorted(df['place_name'].unique()))
        
        idx = df[df['place_name'] == dest_choice].index[0]
        target_vec = X_norm[idx:idx+1]
        distances = euclidean_distances(target_vec, X_norm).flatten()
        
        # Get top 5 closest (excluding self)
        nearest_indices = np.argsort(distances)[1:6]
        
        st.markdown(f"#### Top 5 Matches for '{dest_choice}':")
        cols_rec = st.columns(5)
        for i, match_idx in enumerate(nearest_indices):
            row = df.iloc[match_idx]
            sim_score = max(0, 100 - (distances[match_idx] * 12))
            with cols_rec[i]:
                st.markdown(f"""
                <div class="glass-card" style="padding: 18px 16px;">
                    <div style="font-size:0.75rem; color:#64d2ff; font-weight:700;">{sim_score:.0f}% SIMILAR</div>
                    <div style="font-size:1.05rem; font-weight:700; color:#fff; margin:6px 0 4px 0;">{row['place_name']}</div>
                    <div style="color:rgba(255,255,255,0.55); font-size:0.78rem; margin-bottom:8px;">{row['state']} • {row['category']}</div>
                    <div style="font-size:0.8rem; color:rgba(255,255,255,0.85); line-height:1.6;">
                        ⭐ {row['avg_rating']} / 5.0<br>
                        🎟️ ₹{row['entry_fee']:.0f}<br>
                        ⏱️ {row['visit_duration']} hrs<br>
                        💬 Sentiment: +{row['sentiment_score']:.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with rec_tab2:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            max_budget = st.slider("Maximum Entry Fee (INR)", min_value=0, max_value=1000, value=200, step=20)
        with col_f2:
            max_duration = st.slider("Max Visit Duration (Hours)", min_value=0.5, max_value=6.0, value=3.0, step=0.5)
        with col_f3:
            min_rating = st.slider("Minimum Rating", min_value=3.0, max_value=5.0, value=4.2, step=0.1)

        filtered = df[
            (df['entry_fee'] <= max_budget) &
            (df['visit_duration'] <= max_duration) &
            (df['avg_rating'] >= min_rating)
        ].sort_values(by='sentiment_score', ascending=False)

        st.markdown(f"Found **{len(filtered)}** tailored destinations matching criteria:")
        st.dataframe(
            filtered[['place_name', 'state', 'category', 'entry_fee', 'visit_duration', 'avg_rating', 'sentiment_score']].head(15),
            use_container_width=True
        )

# -----------------------------------------------------------------------------
# PAGE 9: DATA CATALOG & EXPORT
# -----------------------------------------------------------------------------
elif menu == "💾 Data Catalog & Export":
    st.markdown("""
    <div class="glass-panel" style="padding: 32px 36px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 12px;">CATALOG & EXPORT</div>
        <div style="font-size: 2.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.8px; margin-bottom: 8px;">
            Integrated Master Data Catalog
        </div>
        <div style="font-size: 1rem; color: rgba(255, 255, 255, 0.7);">
            Filter, inspect, and export the enriched Indian tourism dataset with verified reviews and coordinates.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_flt1, col_flt2 = st.columns(2)
    with col_flt1:
        states_selected = st.multiselect("Filter by State", options=sorted(df['state'].unique()), default=[])
    with col_flt2:
        categories_selected = st.multiselect("Filter by Category", options=sorted(df['category'].unique()), default=[])

    df_filtered = df.copy()
    if states_selected:
        df_filtered = df_filtered[df_filtered['state'].isin(states_selected)]
    if categories_selected:
        df_filtered = df_filtered[df_filtered['category'].isin(categories_selected)]

    st.dataframe(df_filtered, use_container_width=True)

    csv_data = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name="india_tourism_reviews_filtered.csv",
        mime="text/csv"
    )
