import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from i18n import t
from utils.data_loader import load_master, load_trends

def render(lang):
    df     = load_master()
    trends = load_trends()

    # ── Header ───────────────────────────────────────────
    st.markdown(f"""
    <div style='margin-bottom:8px;'>
        <span style='font-size:36px;font-weight:900;color:#022C22;'>⚡ TechPulse</span>
    </div>
    <div style='font-size:14px;color:#059669;font-weight:700;
                letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;'>
        {'Product Intelligence Platform' if lang == 'en'
        else 'Plataforma de Inteligencia de Productos'}
    </div>
    <div style='font-size:14px;color:#065F46;max-width:700px;line-height:1.6;'>
        {'TechPulse analyzes <b style="color:#10B981">152,556 digital products</b> launched on Product Hunt between 2014 and 2024. The platform combines trend forecasting, semantic clustering, and a hybrid recommendation engine.' if lang == 'en'
        else 'TechPulse analiza <b style="color:#10B981">152,556 productos digitales</b> lanzados en Product Hunt entre 2014 y 2024. La plataforma combina forecasting de tendencias, clustering semántico y un motor de recomendación híbrido.'}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── KPIs ─────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric(t('total_products',   lang), "152,556")
    c2.metric(t('total_votes',      lang), "20.3M")
    c3.metric(t('total_categories', lang), "470")
    c4.metric(t('total_segments',   lang), "10")
    c5.metric(t('years_covered',    lang), "10")
    c6.metric(t('indexed_products', lang), "125,579")

    st.divider()

    # ── Highlight cards ──────────────────────────────────
    best = trends.loc[trends['growth_pct'].idxmax()]
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#10B981,#059669);
                    padding:28px 24px;border-radius:14px;color:white;
                    box-shadow:0 4px 20px rgba(16,185,129,0.35);'>
            <div style='font-size:11px;opacity:0.85;letter-spacing:1.5px;
                        text-transform:uppercase;margin-bottom:10px;font-weight:700;'>
                🤖 {'AI Signal in 2024' if lang == 'en' else 'Señal de IA en 2024'}
            </div>
            <div style='font-size:42px;font-weight:900;line-height:1;'>55.5%</div>
            <div style='font-size:13px;opacity:0.85;margin-top:10px;'>
                {'of 2024 launches are AI-related' if lang == 'en'
                 else 'de los lanzamientos 2024 son AI-related'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#06B6D4,#0891B2);
                    padding:28px 24px;border-radius:14px;color:white;
                    box-shadow:0 4px 20px rgba(6,182,212,0.35);'>
            <div style='font-size:11px;opacity:0.85;letter-spacing:1.5px;
                        text-transform:uppercase;margin-bottom:10px;font-weight:700;'>
                📈 {'Fastest Growing' if lang == 'en' else 'Mayor Crecimiento'}
            </div>
            <div style='font-size:24px;font-weight:900;line-height:1.2;'>
                {best['category']}
            </div>
            <div style='font-size:22px;font-weight:700;opacity:0.9;margin-top:8px;'>
                +{best['growth_pct']:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#6366F1,#4F46E5);
                    padding:28px 24px;border-radius:14px;color:white;
                    box-shadow:0 4px 20px rgba(99,102,241,0.35);'>
            <div style='font-size:11px;opacity:0.85;letter-spacing:1.5px;
                        text-transform:uppercase;margin-bottom:10px;font-weight:700;'>
                ⭐ {'Most Engaging' if lang == 'en' else 'Más Engaging'}
            </div>
            <div style='font-size:20px;font-weight:900;line-height:1.2;'>
                Design & Open Source
            </div>
            <div style='font-size:14px;opacity:0.85;margin-top:8px;'>
                175 {'avg votes/product' if lang == 'en' else 'votos promedio/producto'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Pipeline ─────────────────────────────────────────
    st.markdown(
        f"<div style='font-size:16px;font-weight:700;color:#022C22;margin-bottom:16px;'>"
        f"🔧 {'Technical Pipeline' if lang == 'en' else 'Pipeline Técnico'}</div>",
        unsafe_allow_html=True)

    pipeline = [
        ("01", "Data Collection" if lang == 'en' else "Recolección",
         "152,556 products" if lang == 'en' else "152,556 productos"),
        ("02", "EDA",
         "470 categories · 10 years" if lang == 'en' else "470 categorías · 10 años"),
        ("03", "Forecasting", "Holt-Winters + STL"),
        ("04", "Clustering",  "K-Means + UMAP"),
        ("05", "Recommender" if lang == 'en' else "Recomendador",
         "Sentence Transformers"),
        ("06", "Insights",
         "Bilingual reports" if lang == 'en' else "Informes bilingüe"),
    ]

    bg_colors = ['#10B981','#06B6D4','#6366F1','#F59E0B','#EF4444','#8B5CF6']
    cols = st.columns(6)

    for col, (num, title, desc), bg in zip(cols, pipeline, bg_colors):
        col.markdown(f"""
        <div style='background:{bg};padding:18px 10px;border-radius:12px;
                    text-align:center;color:white;min-height:115px;
                    box-shadow:0 4px 12px rgba(0,0,0,0.12);'>
            <div style='font-size:26px;font-weight:900;opacity:0.9;'>{num}</div>
            <div style='font-size:12px;font-weight:700;margin:6px 0 4px 0;'>{title}</div>
            <div style='font-size:10px;opacity:0.80;line-height:1.4;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Stats rápidas ────────────────────────────────────
    st.markdown(f"<div style='font-size:16px;font-weight:700;color:#CBD5E1;margin-bottom:16px;'>"
                f"📊 {'Quick Stats' if lang == 'en' else 'Estadísticas Rápidas'}</div>",
                unsafe_allow_html=True)

    launches = df.groupby('year').size()
    record_year = int(launches.idxmax())
    record_val  = int(launches.max())

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Record Year" if lang == 'en' else "Año Récord",
              str(record_year), f"+{record_val:,} launches")
    s2.metric("Most Voted Product" if lang == 'en' else "Producto Más Votado",
              "Startup Stash", "21,798 votes")
    s3.metric("Top Category" if lang == 'en' else "Top Categoría",
              "Tech", "52,012 products")
    s4.metric("Data Gap" if lang == 'en' else "Gap de Datos",
              "2022", "No public dataset")