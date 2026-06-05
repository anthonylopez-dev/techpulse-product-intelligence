import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import ast, re
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from i18n import t
from utils.data_loader import load_forecasts, load_trends, load_master, plotly_theme

def render(lang):
    forecasts = load_forecasts()
    trends    = load_trends()
    df        = load_master()
    theme     = plotly_theme()

    st.title(f"📈 {t('forecasting_title', lang)}")
    st.caption(t('forecasting_subtitle', lang))
    st.divider()

    # ── Selector ─────────────────────────────────────────
    categories = sorted(forecasts['category'].unique().tolist())
    selected   = st.selectbox(t('select_category', lang), categories)

    fc = forecasts[forecasts['category'] == selected].copy()
    fc['ds'] = pd.to_datetime(fc['ds'])
    hist = fc[fc['type'] == 'historical']
    fut  = fc[fc['type'] == 'forecast']

    # Serie real
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

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
    ts_real   = (df_topics[df_topics['topics_list'] == selected]
                 .groupby(pd.Grouper(key='created_at', freq='MS'))
                 .size().reset_index(name='y'))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ts_real['created_at'], y=ts_real['y'],
        mode='lines', name='Historical (actual)',
        line=dict(color='#94A3B8', width=1.5)))
    fig.add_trace(go.Scatter(
        x=hist['ds'], y=hist['yhat'],
        mode='lines', name='Model fit',
        line=dict(color='#2563EB', width=1.5, dash='dot')))
    fig.add_trace(go.Scatter(
        x=fut['ds'], y=fut['yhat'],
        mode='lines', name='Forecast 2025–2026',
        line=dict(color='#2563EB', width=2.5)))
    fig.add_trace(go.Scatter(
        x=list(fut['ds']) + list(fut['ds'][::-1]),
        y=list(fut['yhat_upper']) + list(fut['yhat_lower'][::-1]),
        fill='toself', fillcolor='rgba(37,99,235,0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        name='90% CI'))

    forecast_start = pd.Timestamp('2025-01-01').timestamp() * 1000
    fig.add_vline(x=forecast_start, line_dash='dash', line_color='#DC2626',
                  annotation_text='Forecast start',
                  annotation_font_color='#DC2626')

    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Products/month',
        hovermode='x unified',
        legend=dict(
            orientation='h', yanchor='bottom', y=-0.3,
            font=dict(color='#94A3B8')
        ),
        xaxis=theme['xaxis'],
        yaxis=theme['yaxis'],
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=theme['font'],
        margin=dict(t=40, b=80, l=10, r=10),
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Ranking ──────────────────────────────────────────
    st.subheader(t('growth_ranking', lang))
    trends_sorted = trends.sort_values('growth_pct', ascending=True)
    colors_bar = ['#059669' if not r['is_dominant'] else '#2563EB'
                  for _, r in trends_sorted.iterrows()]

    fig2 = go.Figure(go.Bar(
        x=trends_sorted['growth_pct'],
        y=trends_sorted['category'],
        orientation='h',
        marker_color=colors_bar,
        text=[f"{v:+.1f}%" for v in trends_sorted['growth_pct']],
        textposition='outside',
        textfont=dict(color='#94A3B8'),
    ))
    fig2.add_vline(x=0, line_color='#94A3B8', line_width=1)
    fig2.update_layout(
        xaxis_title='Projected Growth (%)' if lang == 'en' else 'Crecimiento Proyectado (%)',
        xaxis=theme['xaxis'],
        yaxis=theme['yaxis'],
        plot_bgcolor=theme['plot_bgcolor'],
        paper_bgcolor=theme['paper_bgcolor'],
        font=theme['font'],
        margin=dict(t=20, b=20, l=10, r=80),
        height=350,
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ── Tabla ────────────────────────────────────────────
    st.subheader("Trend Summary" if lang == 'en' else "Resumen de Tendencias")
    display = trends.sort_values('growth_pct', ascending=False).copy()
    display['Type']          = display['is_dominant'].map(
        {True: 'Dominant' if lang == 'en' else 'Dominante',
         False: '🚀 Emerging' if lang == 'en' else '🚀 Emergente'})
    display['Growth']        = display['growth_pct'].apply(lambda x: f"{x:+.1f}%")
    display['Current']       = display['last_observed'].apply(lambda x: f"{x:.0f}/mo")
    display['2026 Forecast'] = display['forecast_2026'].apply(lambda x: f"{x:.0f}/mo")
    st.dataframe(
        display[['category', 'Current', '2026 Forecast', 'Growth', 'Type']],
        use_container_width=True, hide_index=True)