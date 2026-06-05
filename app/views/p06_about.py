import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from i18n import t

def render(lang):
    PDF_DIR = Path(__file__).parent.parent.parent / 'reports' / 'pdf'

    st.title(f"👤 {t('about_title', lang)}")
    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("## Bryan Anthony López Guerrero")
        st.markdown(f"**{t('about_role', lang)}**")
        st.markdown(t('about_bio', lang))
        st.markdown("""
- 🎓 Ing. en TI | Máster Visual Analytics & Big Data
- 🏆 Especialización en Big Data & IA
- 📍 Ambato, Ecuador
- 🌐 Open to remote opportunities
        """)
        st.divider()
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/anthonylpz)  [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/anthonylopez-dev)")

    with col2:
        st.markdown(f"### {t('stack_title', lang)}")
        stack = {
            "Languages"   : "Python",
            "ML/DS"       : "Scikit-learn · XGBoost · SHAP",
            "NLP"         : "Sentence Transformers",
            "Clustering"  : "K-Means · UMAP",
            "Forecasting" : "Holt-Winters · STL",
            "Apps"        : "Streamlit · FastAPI",
            "Viz"         : "Plotly · Seaborn · Matplotlib",
            "Data"        : "Pandas · Parquet",
            "Reports"     : "ReportLab",
            "DevOps"      : "Git · GitHub · Render",
        }
        for category, tools in stack.items():
            st.markdown(f"**{category}:** {tools}")

    st.divider()
    st.subheader("📄 Reports / Informes")
    c1, c2 = st.columns(2)

    pdf_en = PDF_DIR / 'techpulse_report_en.pdf'
    pdf_es = PDF_DIR / 'techpulse_report_es.pdf'

    with c1:
        if pdf_en.exists():
            with open(pdf_en, 'rb') as f:
                st.download_button(t('download_en', lang), f,
                                   file_name='techpulse_report_en.pdf',
                                   mime='application/pdf',
                                   use_container_width=True)
    with c2:
        if pdf_es.exists():
            with open(pdf_es, 'rb') as f:
                st.download_button(t('download_es', lang), f,
                                   file_name='techpulse_report_es.pdf',
                                   mime='application/pdf',
                                   use_container_width=True)

    st.divider()
    st.subheader("🗂️ Portfolio Projects" if lang == 'en' else "🗂️ Proyectos del Portafolio")
    projects = [
        ("TechPulse", "Product Intelligence Platform · Forecasting + Clustering + Recommender", "2026"),
        ("Diabetes Risk Prediction", "XGBoost + SHAP + Streamlit · ROC-AUC 0.89", "2026"),
        ("Ecuador Tourism Sentiment", "BERT/TextBlob + Looker Studio · NLP pipeline", "2026"),
        ("Labor Market & Poverty Ecuador", "Power BI + XGBoost · 2007–2024", "2026"),
    ]
    for name, desc, year in projects:
        st.markdown(f"**{name}** ({year}) — {desc}")