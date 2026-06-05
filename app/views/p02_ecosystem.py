import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import ast, re
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from i18n import t
from utils.data_loader import load_master, load_clustered, FIGURES, plotly_theme

COLORS = ['#059669','#0284C7','#7C3AED','#D97706','#DC2626','#0891B2','#9333EA','#EA580C']

def render(lang):
    df    = load_master()
    theme = plotly_theme()

    st.title(f"🌍 {t('ecosystem_title', lang)}")
    st.caption(t('ecosystem_subtitle', lang))
    st.divider()

    # ── Lanzamientos por año ─────────────────────────────
    st.subheader(t('launches_title', lang))
    launches = df.groupby('year').size().reset_index(name='count')

    fig = go.Figure()
    for i, row in launches.iterrows():
        fig.add_trace(go.Bar(
            x=[row['year']], y=[row['count']],
            marker_color='#059669',
            showlegend=False,
        ))
    fig.add_vline(x=2020, line_dash='dash', line_color='#D97706',
                  annotation_text='COVID-19',
                  annotation_font_color='#D97706',
                  annotation_position='top right')
    fig.add_vline(x=2023, line_dash='dash', line_color='#0284C7',
                  annotation_text='AI Boom',
                  annotation_font_color='#0284C7',
                  annotation_position='top right')
    fig.update_layout(
        xaxis_title='Year' if lang == 'en' else 'Año',
        yaxis_title='Products Launched' if lang == 'en' else 'Productos Lanzados',
        xaxis=dict(**theme['xaxis'], tickmode='linear'),
        yaxis=theme['yaxis'],
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=theme['font'],
        margin=theme['margin'],
        bargap=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Topics ───────────────────────────────────────────
    st.subheader(t('categories_title', lang))

    def extract_topics(value):
        if pd.isna(value) or str(value) in ('', 'None', 'nan'):
            return []
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list):
                return [str(x).strip().title() for x in parsed if x]
        except:
            pass
        cleaned = re.sub(r"[\[\]'\"{}]", '', str(value))
        return [p.strip().title() for p in cleaned.split(',') if p.strip()]

    df['topics_list'] = df['topics'].apply(extract_topics)
    df_topics = df.explode('topics_list').dropna(subset=['topics_list'])
    df_topics  = df_topics[df_topics['topics_list'].str.len() > 1]

    col1, col2 = st.columns(2)

    with col1:
        top15 = df_topics['topics_list'].value_counts().head(15).reset_index()
        top15.columns = ['topic', 'count']
        # Asignar colores sólidos por categoría
        bar_colors = [COLORS[i % len(COLORS)] for i in range(len(top15))]
        fig2 = go.Figure(go.Bar(
            x=top15['count'],
            y=top15['topic'],
            orientation='h',
            marker_color=bar_colors,
        ))
        fig2.update_layout(
            yaxis=dict(**theme['yaxis'], autorange='reversed'),
            xaxis=theme['xaxis'],
            plot_bgcolor=theme['plot_bgcolor'],
            paper_bgcolor=theme['paper_bgcolor'],
            font=theme['font'],
            margin=theme['margin'],
            xaxis_title='Products' if lang == 'en' else 'Productos',
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        top6  = df_topics['topics_list'].value_counts().head(6).index.tolist()
        cat_year = (df_topics[df_topics['topics_list'].isin(top6)]
                    .groupby(['year', 'topics_list']).size().reset_index(name='count'))

        fig3 = go.Figure()
        for i, cat in enumerate(top6):
            data = cat_year[cat_year['topics_list'] == cat]
            fig3.add_trace(go.Scatter(
                x=data['year'], y=data['count'],
                mode='lines+markers',
                name=cat,
                line=dict(color=COLORS[i % len(COLORS)], width=2.5),
                marker=dict(color=COLORS[i % len(COLORS)], size=6),
            ))
        fig3.update_layout(
            xaxis=theme['xaxis'],
            yaxis=theme['yaxis'],
            plot_bgcolor=theme['plot_bgcolor'],
            paper_bgcolor=theme['paper_bgcolor'],
            font=theme['font'],
            legend=dict(
                font=dict(color='#065F46', size=10),
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor='#BBF7D0',
                borderwidth=1,
                orientation='h',
                yanchor='bottom', y=-0.45,
            ),
            margin=dict(t=40, b=80, l=10, r=10),
            xaxis_title='Year' if lang == 'en' else 'Año',
            yaxis_title='Products' if lang == 'en' else 'Productos',
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # ── Top productos ────────────────────────────────────
    st.subheader("🏆 All-Time Top Products" if lang == 'en'
                 else "🏆 Top Productos de Todos los Tiempos")
    top15_prod = df.nlargest(15, 'votes')[['name', 'votes', 'year']].reset_index(drop=True)
    top15_prod.index += 1
    top15_prod.columns = ['Product', 'Votes', 'Year']
    st.dataframe(top15_prod, use_container_width=True)

    st.divider()

    # ── Engagement por segmento ──────────────────────────
    st.subheader(t('engagement_title', lang))
    df_c = load_clustered()
    cluster_col = 'cluster_name' if 'cluster_name' in df_c.columns else 'cluster'

    seg = (df_c.groupby(cluster_col)
           .agg(avg_votes=('votes','mean'),
                n_products=('votes','count'),
                total_votes=('votes','sum'))
           .reset_index()
           .sort_values('avg_votes'))

    col_a, col_b = st.columns(2)

    with col_a:
        seg_colors = [COLORS[i % len(COLORS)] for i in range(len(seg))]
        fig_e1 = go.Figure(go.Bar(
            x=seg['avg_votes'],
            y=seg[cluster_col],
            orientation='h',
            marker_color=seg_colors,
            text=[f"{v:.0f}" for v in seg['avg_votes']],
            textposition='outside',
            textfont=dict(color='#065F46', size=11),
        ))
        fig_e1.update_layout(
            xaxis=theme['xaxis'],
            yaxis=dict(**theme['yaxis']),
            plot_bgcolor=theme['plot_bgcolor'],
            paper_bgcolor=theme['paper_bgcolor'],
            font=theme['font'],
            margin=theme['margin'],
            xaxis_title='Average Votes' if lang == 'en' else 'Votos Promedio',
        )
        st.plotly_chart(fig_e1, use_container_width=True)

    with col_b:
        fig_e2 = go.Figure()
        for i, (_, row) in enumerate(seg.iterrows()):
            fig_e2.add_trace(go.Scatter(
                x=[row['n_products']],
                y=[row['avg_votes']],
                mode='markers+text',
                name=row[cluster_col],
                text=[row[cluster_col]],
                textposition='top center',
                textfont=dict(color='#065F46', size=9),
                marker=dict(
                    color=COLORS[i % len(COLORS)],
                    size=max(10, min(row['total_votes'] / 20000, 50)),
                    opacity=0.85,
                ),
                showlegend=False,
            ))
        fig_e2.update_layout(
            xaxis=theme['xaxis'],
            yaxis=theme['yaxis'],
            plot_bgcolor=theme['plot_bgcolor'],
            paper_bgcolor=theme['paper_bgcolor'],
            font=theme['font'],
            margin=theme['margin'],
            xaxis_title='Number of Products' if lang == 'en' else 'Número de Productos',
            yaxis_title='Average Votes' if lang == 'en' else 'Votos Promedio',
        )
        st.plotly_chart(fig_e2, use_container_width=True)