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

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & LIQUID GLASS THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Local Tourism Recommender | Dashboard",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injected CSS for Liquid Glass UI/UX
LIQUID_GLASS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0e17;
    --glass-bg: rgba(255, 255, 255, 0.04);
    --glass-border: rgba(255, 255, 255, 0.12);
    --glass-highlight: rgba(255, 255, 255, 0.22);
    --accent-cyan: #00f2fe;
    --accent-blue: #4facfe;
    --accent-violet: #8a2be2;
    --accent-pink: #ff007f;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
}

/* Global Background */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(79, 172, 254, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(255, 0, 127, 0.08) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(138, 43, 226, 0.09) 0%, transparent 60%),
                #070b12 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Liquid Glass Cards */
.liquid-card {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.06) 0%, rgba(255, 255, 255, 0.02) 100%);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--glass-border);
    border-top: 1px solid var(--glass-highlight);
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.liquid-card:hover {
    border-color: rgba(0, 242, 254, 0.4);
    box-shadow: 0 16px 45px rgba(0, 242, 254, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

/* Hero Badge */
.liquid-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: linear-gradient(135deg, rgba(0, 242, 254, 0.15) 0%, rgba(79, 172, 254, 0.05) 100%);
    border: 1px solid rgba(0, 242, 254, 0.3);
    padding: 6px 16px;
    border-radius: 100px;
    color: #38bdf8;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

/* Glowing Typography */
h1, h2, h3 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.5px;
}

.glow-title {
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.6rem;
    font-weight: 700;
    margin-bottom: 8px;
}

/* Metric Pill */
.metric-pill {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 18px 20px;
    text-align: left;
    position: relative;
    overflow: hidden;
}

.metric-pill::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--accent-cyan);
    border-radius: 4px;
}

.metric-val {
    font-family: 'Outfit', sans-serif;
    font-size: 1.85rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
}

.metric-label {
    font-size: 0.82rem;
    font-weight: 500;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

.metric-sub {
    font-size: 0.8rem;
    color: #38bdf8;
    margin-top: 4px;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: rgba(10, 15, 26, 0.85) !important;
    backdrop-filter: blur(25px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Streamlit Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.03);
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #94a3b8 !important;
    padding: 8px 18px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    background: transparent !important;
    border: none !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(0, 242, 254, 0.2) 0%, rgba(79, 172, 254, 0.1) 100%) !important;
    color: #ffffff !important;
    border: 1px solid rgba(0, 242, 254, 0.4) !important;
}

/* Dataframe Styling */
[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>
"""
st.markdown(LIQUID_GLASS_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA LOADING & CACHING
# -----------------------------------------------------------------------------
@st.cache_data
def load_all_data():
    df_path = os.path.join('data', 'processed', 'india_tourism_reviews.csv')
    if not os.path.exists(df_path):
        st.error(f"Missing master dataset at {df_path}. Run pipeline first.")
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

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0;">
        <div style="font-family: 'Outfit'; font-size: 1.4rem; font-weight: 700; color: #fff;">
            Tourism Discovery
        </div>
        <div style="font-size: 0.82rem; color: #94a3b8;">
            Unsupervised Suite
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Navigation Hub",
        [
            "🌟 Executive Overview",
            "📊 Exploratory Data Analysis",
            "🔬 Interactive Clustering Studio",
            "🗺️ Geospatial Tourism Map",
            "🌌 2D & 3D PCA Space",
            "📈 Benchmark & Distance Comparison",
            "👤 Personas & Cluster Profiles",
            "🎯 Destination Recommender",
            "💾 Data Catalog & Export"
        ],
        index=0
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 0.75rem; color: #64748b; line-height: 1.5;">
        <b>Engine:</b> K-Means & Hierarchical<br>
        <b>Data:</b> India Guide + UCSD Google Local<br>
        <b>NLP:</b> VADER Polarity Scoring
    </div>
    """, unsafe_allow_html=True)

# Common Plotly Theme configuration
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Plus Jakarta Sans', color='#cbd5e1'),
    margin=dict(l=30, r=30, t=50, b=30),
    xaxis=dict(gridcolor='rgba(255,255,255,0.06)', zerolinecolor='rgba(255,255,255,0.1)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.06)', zerolinecolor='rgba(255,255,255,0.1)'),
    legend=dict(bgcolor='rgba(15,23,42,0.6)', bordercolor='rgba(255,255,255,0.1)', borderwidth=1)
)

# -----------------------------------------------------------------------------
# PAGE 1: EXECUTIVE OVERVIEW
# -----------------------------------------------------------------------------
if menu == "🌟 Executive Overview":
    st.markdown("""
    <div class="liquid-card">
        <div class="liquid-badge">INTEGRATED TOURISM INTELLIGENCE</div>
        <div class="glow-title">Local Tourism Recommender</div>
        <p style="color: #94a3b8; font-size: 1.05rem; max-width: 900px; margin-bottom: 24px;">
            A multi-dimensional unsupervised learning system harmonizing India's premier tourist destinations 
            with <b>11.45 million reviews</b> from the UCSD Google Local dataset, precision GPS bounds, 
            and VADER NLP sentiment analytics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Top KPI Metrics Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""
        <div class="metric-pill">
            <div class="metric-label">Destinations</div>
            <div class="metric-val">{len(df):,}</div>
            <div class="metric-sub">Across 33 States</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-pill" style="border-left-color: #38bdf8;">
            <div class="metric-label">Google Reviews</div>
            <div class="metric-val">645K+</div>
            <div class="metric-sub">Verified Indian Corpus</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-pill" style="border-left-color: #10b981;">
            <div class="metric-label">Mean Rating</div>
            <div class="metric-val">{df['avg_rating'].mean():.2f} ★</div>
            <div class="metric-sub">Scale: 1.0 - 5.0</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-pill" style="border-left-color: #f59e0b;">
            <div class="metric-label">Positive Feedback</div>
            <div class="metric-val">{df['positive_review_pct'].mean():.1f}%</div>
            <div class="metric-sub">4.0+ Star Proportion</div>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown(f"""
        <div class="metric-pill" style="border-left-color: #ec4899;">
            <div class="metric-label">Mean Sentiment</div>
            <div class="metric-val">+{df['sentiment_score'].mean():.3f}</div>
            <div class="metric-sub">VADER Polarity [-1, +1]</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    
    # Two Columns: Integration Flow & Quick Sample Explorer
    col_left, col_right = st.columns([1.1, 0.9])
    
    with col_left:
        st.markdown("""
        <div class="liquid-card">
            <h3 style="margin-top:0; color:#fff;">Dataset Integration Architecture</h3>
            <p style="color:#94a3b8; font-size:0.9rem;">
                Enriching primary tourism records with verified Google Local entities and NLP reviews:
            </p>
            <div style="background: rgba(0,0,0,0.3); padding: 16px; border-radius: 12px; font-family: monospace; font-size: 0.85rem; color: #38bdf8; line-height: 1.8;">
                [Primary Tourism Data (data.csv)] -> 325 Places<br>
                &nbsp;&nbsp;&nbsp;&nbsp;+ [UCSD Google Local 2018 (3.11M Places)]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--> Filtered India Bounding Box: 180,686 Verified Places<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--> High-Confidence Match: 281 Places (86.5%)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--> Preserved Unmatched: 44 Places (13.5%)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;+ [UCSD Google Reviews (11.45M Reviews)]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--> 645,269 Indian Reviews / 9,521 Matched Reviews<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;--> VADER NLP Compound Sentiment Extraction<br>
                ==> [Master Integrated Dataset: india_tourism_reviews.csv]
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="liquid-card">
            <h3 style="margin-top:0; color:#fff;">Quick Destination Lookahead</h3>
            <p style="color:#94a3b8; font-size:0.9rem;">Preview enriched destination records:</p>
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
    <div class="liquid-card">
        <div class="liquid-badge">DESCRIPTIVE ANALYTICS</div>
        <div class="glow-title">Exploratory Data Analysis</div>
        <p style="color: #94a3b8;">Discover distributions, skewness, fees, and review sentiment correlations across India.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["State & Category Distributions", "Skewness & Economic Profiles", "Feature Correlations"])

    with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
            top_states = df['state'].value_counts().head(12).reset_index()
            top_states.columns = ['State', 'Count']
            fig_states = px.bar(
                top_states, x='Count', y='State', orientation='h',
                title="Top 12 Indian States by Featured Destinations",
                color='Count', color_continuous_scale='Viridis'
            )
            fig_states.update_layout(**PLOTLY_LAYOUT)
            fig_states.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_states, use_container_width=True)

        with col_b:
            top_cats = df['category'].value_counts().head(10).reset_index()
            top_cats.columns = ['Category', 'Count']
            fig_cats = px.pie(
                top_cats, names='Category', values='Count',
                title="Top Destination Categories Breakdown",
                hole=0.45, color_discrete_sequence=px.colors.sequential.Tealgrn
            )
            fig_cats.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig_cats, use_container_width=True)

    with tab2:
        col_c, col_d = st.columns(2)
        with col_c:
            fig_fee = px.histogram(
                df, x='entry_fee', nbins=30,
                title="Entrance Fee Distribution (INR) — Raw Skewness",
                color_discrete_sequence=['#38bdf8']
            )
            fig_fee.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig_fee, use_container_width=True)

        with col_d:
            df['log_fee'] = np.log1p(df['entry_fee'])
            fig_log_fee = px.histogram(
                df, x='log_fee', nbins=30,
                title="Log1p Transformed Entrance Fee (Normalizing for ML)",
                color_discrete_sequence=['#10b981']
            )
            fig_log_fee.update_layout(**PLOTLY_LAYOUT)
            st.plotly_chart(fig_log_fee, use_container_width=True)

    with tab3:
        corr_cols = ['entry_fee', 'visit_duration', 'avg_rating', 'review_count', 'positive_review_pct', 'negative_review_pct', 'sentiment_score']
        corr_matrix = df[corr_cols].corr()
        fig_corr = px.imshow(
            corr_matrix, text_auto=".2f", aspect="auto",
            title="Correlation Matrix of Numerical Tourism Attributes",
            color_continuous_scale="RdBu_r"
        )
        fig_corr.update_layout(**PLOTLY_LAYOUT)
        st.plotly_chart(fig_corr, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 3: INTERACTIVE CLUSTERING STUDIO
# -----------------------------------------------------------------------------
elif menu == "🔬 Interactive Clustering Studio":
    st.markdown("""
    <div class="liquid-card">
        <div class="liquid-badge">REAL-TIME EXPERIMENTATION</div>
        <div class="glow-title">Interactive Clustering Studio</div>
        <p style="color: #94a3b8;">Experiment live with algorithms, distance metrics, cluster counts (K), and feature subsets.</p>
    </div>
    """, unsafe_allow_html=True)

    col_ctrl, col_view = st.columns([1, 2.2])

    with col_ctrl:
        st.markdown("<div class='liquid-card'><b>Hyperparameters</b>", unsafe_allow_html=True)
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
        # Score metrics bar
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Silhouette Score", f"{sil:.4f}", help="Higher is better ([-1, 1])")
        m2.metric("Davies-Bouldin", f"{db:.4f}", help="Lower is better")
        m3.metric("Calinski-Harabasz", f"{ch:.1f}", help="Higher is better")
        m4.metric("WCSS (Inertia)", inertia_val)

        # 2D PCA representation
        pca = PCA(n_components=2, random_state=42)
        X_pca_studio = pca.fit_transform(X_studio)
        df_studio['PCA1'] = X_pca_studio[:, 0]
        df_studio['PCA2'] = X_pca_studio[:, 1]

        fig_cluster = px.scatter(
            df_studio, x='PCA1', y='PCA2', color='Cluster',
            hover_name='place_name',
            hover_data=['state', 'category', 'entry_fee', 'avg_rating', 'sentiment_score'],
            title=f"Live 2D PCA Projection: {algorithm} (K={k_val}, {metric_choice})",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_cluster.update_layout(**PLOTLY_LAYOUT)
        fig_cluster.update_traces(marker=dict(size=9, opacity=0.85, line=dict(width=0.8, color='white')))
        st.plotly_chart(fig_cluster, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 4: GEOSPATIAL MAP
# -----------------------------------------------------------------------------
elif menu == "🗺️ Geospatial Tourism Map":
    st.markdown("""
    <div class="liquid-card">
        <div class="liquid-badge">SPATIAL DISTRIBUTION</div>
        <div class="glow-title">Interactive Geospatial Tourism Map</div>
        <p style="color: #94a3b8;">Explore tourist destinations across Indian states, clustered by behavior and popularity.</p>
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
        color_continuous_scale="Turbo"
    )
    fig_map.update_geos(
        fitbounds="locations",
        visible=False,
        showcountries=True,
        countrycolor="rgba(255,255,255,0.2)",
        showland=True,
        landcolor="#0e1626",
        showsubunits=True,
        subunitcolor="rgba(255,255,255,0.15)"
    )
    fig_map.update_layout(**PLOTLY_LAYOUT)
    fig_map.update_layout(height=650)
    st.plotly_chart(fig_map, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 5: 2D & 3D PCA SPACE
# -----------------------------------------------------------------------------
elif menu == "🌌 2D & 3D PCA Space":
    st.markdown("""
    <div class="liquid-card">
        <div class="liquid-badge">DIMENSIONALITY REDUCTION</div>
        <div class="glow-title">Principal Component Analysis (PCA)</div>
        <p style="color: #94a3b8;">Visualizing high-dimensional clustering geometry in 2D and 3D coordinate space.</p>
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
            title=f"3D PCA Projection (Explained Variance: {pca_3d.explained_variance_ratio_.sum()*100:.1f}%)",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_3d.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1'),
            scene=dict(
                xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
                yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)"),
                zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)")
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
            title="PCA Component Loadings",
            color_continuous_scale="Purples"
        )
        fig_loadings.update_layout(**PLOTLY_LAYOUT)
        fig_loadings.update_layout(height=600)
        st.plotly_chart(fig_loadings, use_container_width=True)

# -----------------------------------------------------------------------------
# PAGE 6: BENCHMARK & DISTANCE COMPARISON
# -----------------------------------------------------------------------------
elif menu == "📈 Benchmark & Distance Comparison":
    st.markdown("""
    <div class="liquid-card">
        <div class="liquid-badge">QUANTITATIVE VALIDATION</div>
        <div class="glow-title">Model Benchmarks & Distance Comparison</div>
        <p style="color: #94a3b8;">Evaluation across WCSS, Silhouette, Davies-Bouldin, and Euclidean vs. Manhattan distance.</p>
    </div>
    """, unsafe_allow_html=True)

    if not metrics_df.empty:
        st.markdown("<div class='liquid-card'><h4>Clustering Validation Scoreboard</h4>", unsafe_allow_html=True)
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
    <div class="liquid-card">
        <div class="liquid-badge">SEGMENTATION INTERPRETATION</div>
        <div class="glow-title">Tourist Personas & Behavioral Profiles</div>
        <p style="color: #94a3b8;">Actionable behavioral insights into destination archetypes derived from K-Means (K=3).</p>
    </div>
    """, unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)

    with p1:
        st.markdown("""
        <div class="liquid-card" style="border-top-color: #38bdf8;">
            <div style="font-size:0.8rem; color:#38bdf8; font-weight:700;">CLUSTER 0 (61.5%)</div>
            <h3 style="color:#fff; margin:6px 0;">Budget Sacred & Scenic Gems</h3>
            <p style="color:#94a3b8; font-size:0.85rem;">High satisfaction, negligible entry fees, cultural and spiritual pilgrimage sites.</p>
            <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.8;">
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
        <div class="liquid-card" style="border-top-color: #f43f5e;">
            <div style="font-size:0.8rem; color:#f43f5e; font-weight:700;">CLUSTER 1 (9.8%)</div>
            <h3 style="color:#fff; margin:6px 0;">Mixed / Critical Destinations</h3>
            <p style="color:#94a3b8; font-size:0.85rem;">Destinations receiving polarizing or critical traveler reviews; requires management attention.</p>
            <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.8;">
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
        <div class="liquid-card" style="border-top-color: #10b981;">
            <div style="font-size:0.8rem; color:#10b981; font-weight:700;">CLUSTER 2 (28.6%)</div>
            <h3 style="color:#fff; margin:6px 0;">Premium Eco & Heritage</h3>
            <p style="color:#94a3b8; font-size:0.85rem;">Higher ticket prices, extended visit durations, premier national monuments & parks.</p>
            <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.8;">
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
        st.markdown("<div class='liquid-card'><h4>Statistical Cluster Profile Summary</h4>", unsafe_allow_html=True)
        st.dataframe(profiles_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PAGE 8: DESTINATION RECOMMENDER
# -----------------------------------------------------------------------------
elif menu == "🎯 Destination Recommender":
    st.markdown("""
    <div class="liquid-card">
        <div class="liquid-badge">RECOMMENDATION ENGINE</div>
        <div class="glow-title">Destination Recommender</div>
        <p style="color: #94a3b8;">Discover personalized travel recommendations using cluster neighborhoods and multi-attribute similarity.</p>
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
                <div class="liquid-card" style="padding: 16px;">
                    <div style="font-size:0.75rem; color:#38bdf8; font-weight:700;">{sim_score:.0f}% SIMILAR</div>
                    <h4 style="color:#fff; margin:6px 0; font-size:1.05rem;">{row['place_name']}</h4>
                    <p style="color:#94a3b8; font-size:0.8rem; margin-bottom:8px;">{row['state']} • {row['category']}</p>
                    <div style="font-size:0.8rem; color:#cbd5e1;">
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
    <div class="liquid-card">
        <div class="liquid-badge">CATALOG & EXPORT</div>
        <div class="glow-title">Integrated Master Data Catalog</div>
        <p style="color: #94a3b8;">Filter, inspect, and export the enriched Indian tourism dataset.</p>
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
