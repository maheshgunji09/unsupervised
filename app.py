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
from liquid_glass_theme import get_liquid_glass_css, get_apple_plotly_layout, get_lucide_icon

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & APPLE TAHOE LIQUID GLASS INJECTION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Local Tourism Recommender | Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Central CSS Design Tokens & Lucide Icon System
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

# Functional Palette for Analytics & Clusters
PALETTE_FUNCTIONAL = ['#0A84FF', '#30D158', '#FF9F0A', '#BF5AF2', '#64D2FF', '#FF375F']

# -----------------------------------------------------------------------------
# 3. APPLE TRANSLUCENT FLOATING SIDEBAR (NO EMOJIS, MONOCHROME LUCIDE ICONS)
# -----------------------------------------------------------------------------
with st.sidebar:
    # macOS Window Controls & Subtle Branding
    st.markdown(f"""
    <div class="macos-header">
        <div class="macos-traffic-lights">
            <span class="traffic-light light-red"></span>
            <span class="traffic-light light-yellow"></span>
            <span class="traffic-light light-green"></span>
        </div>
        <div style="font-size: 0.70rem; color: var(--text-tertiary); font-weight: 600; letter-spacing: 0.6px;">
            MACOS TAHOE &bull; LIQUID GLASS
        </div>
    </div>
    <div style="padding: 0 0 16px 2px;">
        <div style="display: flex; align-items: center; gap: 9px; margin-bottom: 3px;">
            <div style="width: 24px; height: 24px; border-radius: 6px; background: rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center;">
                {get_lucide_icon('compass', size=14, color='var(--text-primary)')}
            </div>
            <div style="font-size: 1.05rem; font-weight: 600; color: var(--text-primary); letter-spacing: -0.2px;">
                Tourism Discovery
            </div>
        </div>
        <div style="font-size: 0.76rem; color: var(--text-tertiary); padding-left: 33px;">
            Unsupervised Analytics Suite
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clean Navigation Menu (Strictly No Emojis - SVGs are injected via CSS)
    NAV_ITEMS = [
        "Executive Overview",
        "Exploratory Data Analysis",
        "Interactive Clustering Studio",
        "Geospatial Tourism Map",
        "2D & 3D PCA Space",
        "Benchmark & Distance Comparison",
        "Personas & Cluster Profiles",
        "Smart Destination Recommender",
        "Data Catalog & Export"
    ]
    
    menu = st.radio(
        "Navigation",
        NAV_ITEMS,
        index=0,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Clean Status Footer
    st.markdown("""
    <div class="glass-card" style="padding: 12px 14px; margin-top: 8px; border-radius: 14px;">
        <div style="display: flex; align-items: center; gap: 7px; margin-bottom: 6px;">
            <span style="width: 7px; height: 7px; border-radius: 50%; background: var(--system-green); display: inline-block;"></span>
            <span style="font-size: 0.75rem; font-weight: 600; color: var(--text-primary);">System Online</span>
        </div>
        <div style="font-size: 0.70rem; color: var(--text-tertiary); line-height: 1.55;">
            &bull; 325 Verified Places<br>
            &bull; 645K Google Local Reviews<br>
            &bull; VADER NLP Sentiment<br>
            &bull; K-Means &amp; Hierarchical
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
if menu == "Executive Overview":
    # 1. Floating Hero Glass Slab
    st.markdown("""
    <div class="glass-panel" style="padding: 38px 40px; margin-bottom: 24px;">
        <div class="glass-pill" style="margin-bottom: 14px;">
            INTELLIGENT TOURISM DISCOVERY PLATFORM
        </div>
        <div style="font-size: 2.5rem; font-weight: 700; letter-spacing: -0.8px; color: var(--text-primary); line-height: 1.15; margin-bottom: 12px;">
            AI-Powered Local Tourism Recommender
        </div>
        <div style="font-size: 1.05rem; color: var(--text-secondary); line-height: 1.6; max-width: 960px;">
            An intelligent tourism discovery platform combining Indian destination information, Google Local reviews, 
            sentiment analysis and unsupervised machine learning.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Restrained Neutral Liquid Glass KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="apple-metric-card">
            <div class="metric-title">{get_lucide_icon('map-pin', size=13)} Destinations</div>
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-subtitle">Across 33 States</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="apple-metric-card">
            <div class="metric-title">{get_lucide_icon('message-square', size=13)} Google Reviews</div>
            <div class="metric-value">645K+</div>
            <div class="metric-subtitle">Verified Indian Corpus</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="apple-metric-card" style="border-top-color: rgba(10, 132, 255, 0.40);">
            <div class="metric-title" style="color: var(--system-blue);">{get_lucide_icon('star', size=13, color='var(--system-blue)')} Mean Rating</div>
            <div class="metric-value" style="color: var(--text-primary);">{df['avg_rating'].mean():.2f}</div>
            <div class="metric-subtitle">Scale 1.0 - 5.0</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="apple-metric-card">
            <div class="metric-title">{get_lucide_icon('thumbs-up', size=13)} Positive Feedback</div>
            <div class="metric-value">{df['positive_review_pct'].mean():.1f}%</div>
            <div class="metric-subtitle">Rating 4.0+ Proportion</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col5:
        st.markdown(f"""
        <div class="apple-metric-card">
            <div class="metric-title">{get_lucide_icon('trending-up', size=13)} Mean Sentiment</div>
            <div class="metric-value">+{df['sentiment_score'].mean():.3f}</div>
            <div class="metric-subtitle">VADER Polarity [-1, +1]</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # 3. Main Dashboard Panels: Integration Flow & Quick Lookahead
    col_left, col_right = st.columns([1.15, 0.85])
    
    with col_left:
        st.markdown(f"""
        <div class="glass-panel" style="padding: 26px 28px;">
            <div class="macos-header" style="margin-bottom: 16px; padding-bottom: 10px;">
                <div style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                    {get_lucide_icon('workflow', size=16, color='var(--text-secondary)')}
                    Dataset Integration Architecture
                </div>
                <div class="glass-pill" style="font-size: 0.70rem; padding: 3px 9px;">
                    180,686 Verified Places
                </div>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.86rem; line-height: 1.55; margin-bottom: 18px;">
                Data pipeline integrating Indian destinations with Google Local reviews:
            </p>
            <div style="display: grid; gap: 8px;">
                <div class="glass-card" style="padding: 10px 16px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.82rem; color: var(--text-primary); font-weight: 500;">1. Primary Tourism Dataset</span>
                    <span class="glass-pill" style="font-size: 0.70rem;">data.csv (325 Destinations)</span>
                </div>
                <div class="glass-card" style="padding: 10px 16px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.82rem; color: var(--text-primary); font-weight: 500;">2. UCSD Google Places Corpus</span>
                    <span class="glass-pill" style="font-size: 0.70rem;">3.11M Total &bull; 180,686 In-Bounds</span>
                </div>
                <div class="glass-card" style="padding: 10px 16px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.82rem; color: var(--text-primary); font-weight: 500;">3. Entity Matching &amp; Resolution</span>
                    <span class="glass-pill" style="font-size: 0.70rem;">281 Matched (86.5%) &bull; 44 Preserved</span>
                </div>
                <div class="glass-card" style="padding: 10px 16px; display: flex; align-items: center; justify-content: space-between;">
                    <span style="font-size: 0.82rem; color: var(--text-primary); font-weight: 500;">4. Review Sentiment Extraction</span>
                    <span class="glass-pill" style="font-size: 0.70rem;">645K Indian Reviews &bull; VADER Polarity</span>
                </div>
                <div class="glass-card" style="padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; border-color: rgba(10, 132, 255, 0.28); background: rgba(10, 132, 255, 0.05);">
                    <span style="font-size: 0.82rem; color: var(--text-primary); font-weight: 600;">5. Integrated ML Master Table</span>
                    <span class="glass-pill" style="font-size: 0.70rem; color: var(--system-blue); border-color: rgba(10, 132, 255, 0.35);">india_tourism_reviews.csv</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
        <div class="glass-panel" style="padding: 26px 28px;">
            <div class="macos-header" style="margin-bottom: 16px; padding-bottom: 10px;">
                <div style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); display: flex; align-items: center; gap: 8px;">
                    {get_lucide_icon('database', size=16, color='var(--text-secondary)')}
                    Quick Destination Lookahead
                </div>
                <div class="glass-pill" style="font-size: 0.70rem; padding: 3px 9px;">
                    Preview Sample
                </div>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.86rem; line-height: 1.55; margin-bottom: 14px;">
                Verified destinations with review counts and sentiment scores:
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
elif menu == "Exploratory Data Analysis":
    st.markdown(f"""
    <div class="glass-panel" style="padding: 28px 32px; margin-bottom: 22px;">
        <div class="glass-pill" style="margin-bottom: 10px;">DATASET INSIGHTS</div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.6px; margin-bottom: 6px;">
            Exploratory Data Analysis
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary);">
            Inspect geographic coverage across 33 states, economic distributions, and multi-attribute correlations.
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
                color_discrete_sequence=['#0A84FF']
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
                hole=0.60,
                color_discrete_sequence=PALETTE_FUNCTIONAL
            )
            fig_cats.update_layout(**APPLE_PLOTLY_THEME)
            st.plotly_chart(fig_cats, use_container_width=True)

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            fig_fee = px.histogram(
                df, x='entry_fee', nbins=30,
                title="Raw Entrance Fee (INR) — Positive Skewness",
                color_discrete_sequence=['#64D2FF']
            )
            fig_fee.update_layout(**APPLE_PLOTLY_THEME)
            st.plotly_chart(fig_fee, use_container_width=True)

        with col_d:
            df['log_fee'] = np.log1p(df['entry_fee'])
            fig_log_fee = px.histogram(
                df, x='log_fee', nbins=30,
                title="Log1p Transformed Entrance Fee (Normalized for ML)",
                color_discrete_sequence=['#30D158']
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
elif menu == "Interactive Clustering Studio":
    st.markdown(f"""
    <div class="glass-panel" style="padding: 28px 32px; margin-bottom: 22px;">
        <div class="glass-pill" style="margin-bottom: 10px;">MACHINE LEARNING LAB</div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.6px; margin-bottom: 6px;">
            Interactive Clustering Studio
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary);">
            Live parameter tuning for K-Means and Hierarchical Clustering with real-time validation feedback.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_view = st.columns([1, 2.3])

    with col_ctrl:
        st.markdown(f"""
        <div class="glass-panel" style="padding: 22px 24px;">
            <div style="font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; display: flex; align-items: center; gap: 7px;">
                {get_lucide_icon('sliders', size=15, color='var(--text-secondary)')}
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
                <div class="metric-subtitle">Cluster Compactness</div>
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
            color_discrete_sequence=PALETTE_FUNCTIONAL
        )
        fig_cluster.update_layout(**APPLE_PLOTLY_THEME)
        fig_cluster.update_traces(marker=dict(size=8, opacity=0.88, line=dict(width=0.8, color='rgba(255,255,255,0.6)')))
        st.plotly_chart(fig_cluster, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 4: GEOSPATIAL MAP
# -----------------------------------------------------------------------------
elif menu == "Geospatial Tourism Map":
    st.markdown(f"""
    <div class="glass-panel" style="padding: 28px 32px; margin-bottom: 22px;">
        <div class="glass-pill" style="margin-bottom: 10px;">GEOGRAPHIC VISUALIZATION</div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.6px; margin-bottom: 6px;">
            Geospatial Tourism Map
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary);">
            Destination distribution across India bounded by sovereign coordinates and cluster personas.
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
        color_continuous_scale="Blues"
    )
    fig_map.update_geos(
        fitbounds="locations",
        visible=False,
        showcountries=True,
        countrycolor="rgba(255,255,255,0.18)",
        showland=True,
        landcolor="#101014",
        showsubunits=True,
        subunitcolor="rgba(255,255,255,0.10)"
    )
    fig_map.update_layout(**APPLE_PLOTLY_THEME)
    fig_map.update_layout(height=650)
    st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 5: 2D & 3D PCA SPACE
# -----------------------------------------------------------------------------
elif menu == "2D & 3D PCA Space":
    st.markdown(f"""
    <div class="glass-panel" style="padding: 28px 32px; margin-bottom: 22px;">
        <div class="glass-pill" style="margin-bottom: 10px;">DIMENSIONALITY REDUCTION</div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.6px; margin-bottom: 6px;">
            Principal Component Analysis (PCA)
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary);">
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
            color_discrete_sequence=['#0A84FF', '#30D158', '#FF9F0A']
        )
        fig_3d.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='-apple-system, BlinkMacSystemFont, sans-serif', color='rgba(235,235,245,0.85)'),
            scene=dict(
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)"),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)"),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.06)")
            ),
            height=600
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
            color_continuous_scale="Blues"
        )
        fig_loadings.update_layout(**APPLE_PLOTLY_THEME)
        fig_loadings.update_layout(height=600)
        st.plotly_chart(fig_loadings, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 6: BENCHMARK & DISTANCE COMPARISON
# -----------------------------------------------------------------------------
elif menu == "Benchmark & Distance Comparison":
    st.markdown(f"""
    <div class="glass-panel" style="padding: 28px 32px; margin-bottom: 22px;">
        <div class="glass-pill" style="margin-bottom: 10px;">QUANTITATIVE BENCHMARKS</div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.6px; margin-bottom: 6px;">
            Model Benchmarks & Distance Comparison
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary);">
            Empirical comparison across WCSS, Silhouette, Davies-Bouldin, and Euclidean vs. Manhattan distance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not metrics_df.empty:
        st.markdown("<div class='glass-panel' style='padding: 22px 26px;'><div style='font-size: 1.05rem; font-weight: 600; color: var(--text-primary); margin-bottom: 12px;'>Clustering Validation Scoreboard</div>", unsafe_allow_html=True)
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
elif menu == "Personas & Cluster Profiles":
    st.markdown(f"""
    <div class="glass-panel" style="padding: 28px 32px; margin-bottom: 22px;">
        <div class="glass-pill" style="margin-bottom: 10px;">BEHAVIORAL SEGMENTATION</div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.6px; margin-bottom: 6px;">
            Tourist Personas & Behavioral Profiles
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary);">
            Interpreted destination archetypes derived from K-Means (K=3) profiling.
        </div>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown(f"""
        <div class="glass-panel" style="border-top: 1.5px solid var(--system-cyan); padding: 24px 22px;">
            <div style="font-size:0.74rem; color:var(--system-cyan); font-weight:600; text-transform:uppercase; letter-spacing:0.6px; display:flex; align-items:center; gap:6px;">
                {get_lucide_icon('landmark', size=13, color='var(--system-cyan)')}
                Cluster 0 (61.5%)
            </div>
            <div style="font-size:1.25rem; font-weight:700; color:var(--text-primary); margin:6px 0 8px 0;">Budget Sacred &amp; Scenic</div>
            <p style="color:var(--text-secondary); font-size:0.84rem; line-height:1.5; margin-bottom:14px;">
                High satisfaction, negligible entry fees, cultural and spiritual pilgrimage sites.
            </p>
            <div style="font-size:0.80rem; color:var(--text-secondary); line-height:1.75;">
                &bull; <b>Avg Entry Fee:</b> INR 5.9 (Median INR 0.0)<br>
                &bull; <b>Avg Duration:</b> 1.43 Hours<br>
                &bull; <b>Avg Rating:</b> 4.49 (87.7% Positive)<br>
                &bull; <b>Sentiment:</b> +0.573<br>
                &bull; <b>Sites:</b> Temples, Beaches, Lakes<br>
                &bull; <b>Target:</b> Pilgrims &amp; Backpackers
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p2:
        st.markdown(f"""
        <div class="glass-panel" style="border-top: 1.5px solid var(--system-pink); padding: 24px 22px;">
            <div style="font-size:0.74rem; color:var(--system-pink); font-weight:600; text-transform:uppercase; letter-spacing:0.6px; display:flex; align-items:center; gap:6px;">
                {get_lucide_icon('alert-circle', size=13, color='var(--system-pink)')}
                Cluster 1 (9.8%)
            </div>
            <div style="font-size:1.25rem; font-weight:700; color:var(--text-primary); margin:6px 0 8px 0;">Critical Feedback Sites</div>
            <p style="color:var(--text-secondary); font-size:0.84rem; line-height:1.5; margin-bottom:14px;">
                Destinations receiving polarizing reviews requiring maintenance and crowd intervention.
            </p>
            <div style="font-size:0.80rem; color:var(--text-secondary); line-height:1.75;">
                &bull; <b>Avg Entry Fee:</b> INR 91.2<br>
                &bull; <b>Avg Duration:</b> 1.70 Hours<br>
                &bull; <b>Avg Rating:</b> 2.91 (34.6% Negative)<br>
                &bull; <b>Sentiment:</b> +0.006 (Neutral/Low)<br>
                &bull; <b>Sites:</b> Crowded beaches, shrines<br>
                &bull; <b>Target:</b> Infrastructure Improvement
            </div>
        </div>
        """, unsafe_allow_html=True)

    with p3:
        st.markdown(f"""
        <div class="glass-panel" style="border-top: 1.5px solid var(--system-green); padding: 24px 22px;">
            <div style="font-size:0.74rem; color:var(--system-green); font-weight:600; text-transform:uppercase; letter-spacing:0.6px; display:flex; align-items:center; gap:6px;">
                {get_lucide_icon('trees', size=13, color='var(--system-green)')}
                Cluster 2 (28.6%)
            </div>
            <div style="font-size:1.25rem; font-weight:700; color:var(--text-primary); margin:6px 0 8px 0;">Premium Eco &amp; Heritage</div>
            <p style="color:var(--text-secondary); font-size:0.84rem; line-height:1.5; margin-bottom:14px;">
                Higher ticket prices, extended visits, premier national monuments &amp; safari parks.
            </p>
            <div style="font-size:0.80rem; color:var(--text-secondary); line-height:1.75;">
                &bull; <b>Avg Entry Fee:</b> INR 360.6 (Median INR 60)<br>
                &bull; <b>Avg Duration:</b> 2.65 Hours<br>
                &bull; <b>Avg Rating:</b> 4.27 (80.5% Positive)<br>
                &bull; <b>Sentiment:</b> +0.522<br>
                &bull; <b>Sites:</b> National Parks, Forts, Palaces<br>
                &bull; <b>Target:</b> Heritage Tourists &amp; Guided Tours
            </div>
        </div>
        """, unsafe_allow_html=True)

    if not profiles_df.empty:
        st.markdown("<div class='glass-panel' style='padding: 22px 26px;'><div style='font-size: 1.05rem; font-weight: 600; color: var(--text-primary); margin-bottom: 12px;'>Statistical Cluster Profile Summary</div>", unsafe_allow_html=True)
        st.dataframe(profiles_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 8: SMART DESTINATION RECOMMENDER
# -----------------------------------------------------------------------------
elif menu == "Smart Destination Recommender":
    st.markdown(f"""
    <div class="glass-panel" style="padding: 28px 32px; margin-bottom: 22px;">
        <div class="glass-pill" style="margin-bottom: 10px;">RECOMMENDATION ENGINE</div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.6px; margin-bottom: 6px;">
            Smart Destination Recommender
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary);">
            Discover personalized travel recommendations using cluster neighborhoods and multi-attribute similarity.
        </div>
    </div>
    """, unsafe_allow_html=True)

    rec_tab1, rec_tab2 = st.tabs(["Find Similar Destinations", "Preference-Based Search"])

    # Normalized feature matrix for similarity calculations
    num_features = ['latitude', 'longitude', 'entry_fee', 'visit_duration', 'avg_rating', 'review_count', 'sentiment_score']
    scaler = StandardScaler()
    X_norm = scaler.fit_transform(df[num_features].values)

    with rec_tab1:
        st.write("Pick a benchmark destination to discover closest neighbors in learned multi-attribute space:")
        dest_choice = st.selectbox("Benchmark Destination", options=sorted(df['place_name'].unique()))
        
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
                <div class="glass-card" style="padding: 16px 14px;">
                    <div style="font-size:0.72rem; color:var(--system-blue); font-weight:600; text-transform:uppercase;">{sim_score:.0f}% Similarity</div>
                    <div style="font-size:1rem; font-weight:600; color:var(--text-primary); margin:5px 0 3px 0;">{row['place_name']}</div>
                    <div style="color:var(--text-tertiary); font-size:0.76rem; margin-bottom:8px;">{row['state']} &bull; {row['category']}</div>
                    <div style="font-size:0.78rem; color:var(--text-secondary); line-height:1.6;">
                        Rating: {row['avg_rating']} / 5.0<br>
                        Fee: INR {row['entry_fee']:.0f}<br>
                        Duration: {row['visit_duration']} hrs<br>
                        Sentiment: +{row['sentiment_score']:.2f}
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
elif menu == "Data Catalog & Export":
    st.markdown(f"""
    <div class="glass-panel" style="padding: 28px 32px; margin-bottom: 22px;">
        <div class="glass-pill" style="margin-bottom: 10px;">CATALOG &amp; EXPORT</div>
        <div style="font-size: 2rem; font-weight: 700; color: var(--text-primary); letter-spacing: -0.6px; margin-bottom: 6px;">
            Integrated Master Data Catalog
        </div>
        <div style="font-size: 0.95rem; color: var(--text-secondary);">
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
        label="Download Filtered Dataset (CSV)",
        data=csv_data,
        file_name="india_tourism_reviews_filtered.csv",
        mime="text/csv"
    )
