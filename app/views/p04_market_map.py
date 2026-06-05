import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from i18n import t
from utils.data_loader import load_clustered, load_profiles, FIGURES, plotly_theme

def render(lang):
    df       = load_clustered()
    profiles = load_profiles()
    theme    = plotly_theme()

    st.title(f"🗺️ {t('market_map_title', lang)}")
    st.caption(t('market_map_subtitle', lang))
    st.divider()

    # ── UMAP estático ────────────────────────────────────
    st.subheader("🗺️ Product Ecosystem Map" if lang == 'en'
                 else "🗺️ Mapa del Ecosistema de Productos")
    st.markdown(
        "Each dot represents a product. Colors indicate market segments identified by K-Means clustering."
        if lang == 'en' else
        "Cada punto representa un producto. Los colores indican segmentos de mercado identificados por clustering K-Means."
    )

    umap_path = FIGURES / '13_umap_named_clusters.png'
    if umap_path.exists():
        from PIL import Image as PILImage
        img = PILImage.open(umap_path)
        orig_w, orig_h = img.size
        # Mostrar a resolución nativa máxima sin estirar
        max_w = 900
        if orig_w > max_w:
            display_w = max_w
        else:
            display_w = orig_w
        st.image(str(umap_path), width=display_w)
    else:
        st.warning("UMAP figure not found. Run notebook 04 first.")

    st.divider()

    # ── Burbujas interactivas ────────────────────────────
    st.subheader("Segment Size vs. Engagement" if lang == 'en'
                 else "Tamaño vs. Engagement por Segmento")
    st.markdown(
        "Bubble size represents total votes in the segment."
        if lang == 'en' else
        "El tamaño de la burbuja representa los votos totales del segmento."
    )

    cluster_col = 'cluster_name' if 'cluster_name' in df.columns else 'cluster'
    seg_stats = (df.groupby(cluster_col)
                 .agg(n_products=('votes','count'),
                      avg_votes=('votes','mean'),
                      total_votes=('votes','sum'))
                 .reset_index())

    fig = px.scatter(seg_stats,
        x='n_products', y='avg_votes',
        size='total_votes', color=cluster_col,
        hover_name=cluster_col,
        text=cluster_col,
        labels={
            'n_products': 'Number of Products' if lang == 'en' else 'Número de Productos',
            'avg_votes' : 'Average Votes' if lang == 'en' else 'Votos Promedio',
            cluster_col : 'Segment' if lang == 'en' else 'Segmento',
        },
        size_max=60)
    fig.update_traces(textposition='top center', textfont=dict(color='#94A3B8', size=9))
    fig.update_layout(
        showlegend=False,
        xaxis=theme['xaxis'],
        yaxis=theme['yaxis'],
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=theme['font'],
        margin=theme['margin'],
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Perfil de segmento ───────────────────────────────
    st.subheader(t('segment_profile', lang))
    segments = sorted(df[cluster_col].dropna().unique().tolist())
    selected = st.selectbox(t('select_segment', lang), segments)

    segment = df[df[cluster_col] == selected]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Products"    if lang == 'en' else "Productos",
              f"{len(segment):,}")
    c2.metric("Avg Votes"   if lang == 'en' else "Votos Promedio",
              f"{segment['votes'].mean():.0f}")
    c3.metric("Median Votes" if lang == 'en' else "Votos Mediana",
              f"{segment['votes'].median():.0f}")
    c4.metric("Max Votes"   if lang == 'en' else "Votos Máximos",
              f"{segment['votes'].max():,}")

    st.markdown(f"**{'Top 10 products in this segment' if lang == 'en' else 'Top 10 productos en este segmento'}:**")
    top10 = (segment.nlargest(10, 'votes')
             [['name', 'tagline', 'votes', 'year']]
             .reset_index(drop=True))
    top10.index += 1
    top10.columns = ['Product', 'Tagline', 'Votes', 'Year']
    st.dataframe(top10, use_container_width=True)

    st.divider()

    # ── Distribución de votos del segmento ───────────────
    st.subheader("Vote Distribution in Segment" if lang == 'en'
                 else "Distribución de Votos en el Segmento")

    votes_filtered = segment[segment['votes'] > 0]['votes']
    p99 = votes_filtered.quantile(0.99)
    votes_plot = votes_filtered[votes_filtered <= p99]

    fig2 = px.histogram(
        votes_plot, nbins=40,
        labels={'value': 'Votes', 'count': 'Products'},
        color_discrete_sequence=['#2563EB'])
    fig2.update_layout(
        showlegend=False,
        xaxis=theme['xaxis'],
        yaxis=theme['yaxis'],
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=theme['font'],
        margin=theme['margin'],
        height=300,
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ── Tabla de todos los segmentos ─────────────────────
    st.subheader("All Segments Overview" if lang == 'en'
                 else "Resumen de Todos los Segmentos")

    all_segs = (df.groupby(cluster_col)
                .agg(products=('votes','count'),
                     avg_votes=('votes','mean'),
                     median_votes=('votes','median'),
                     max_votes=('votes','max'))
                .reset_index()
                .sort_values('avg_votes', ascending=False))
    all_segs.columns = (
        ['Segment', 'Products', 'Avg Votes', 'Median Votes', 'Max Votes']
        if lang == 'en' else
        ['Segmento', 'Productos', 'Votos Prom.', 'Votos Mediana', 'Votos Máx.']
    )
    all_segs = all_segs.round(1).reset_index(drop=True)
    all_segs.index += 1
    st.dataframe(all_segs, use_container_width=True)