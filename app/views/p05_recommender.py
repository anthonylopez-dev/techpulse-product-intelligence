import streamlit as st
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from i18n import t
from utils.data_loader import load_recommendation_index, load_embeddings, load_sentence_transformer

def render(lang):
    st.title(f"🤖 {t('recommender_title', lang)}")
    st.divider()

    df_idx     = load_recommendation_index()
    embeddings = load_embeddings()
    model      = load_sentence_transformer()

    if embeddings is None:
        st.error("Embeddings not found. Please run notebook 05 first." if lang == 'en'
                 else "Embeddings no encontrados. Ejecuta el notebook 05 primero.")
        st.stop()

    from utils.recommender import recommend_by_query, recommend_similar

    cluster_col = 'cluster_name' if 'cluster_name' in df_idx.columns else 'cluster'

    mode = st.radio("", [t('mode_a', lang), t('mode_b', lang)], horizontal=True)
    st.divider()

    if mode == t('mode_a', lang):
        col1, col2 = st.columns([3, 1])
        with col1:
            query = st.text_input(t('mode_a_label', lang),
                                  placeholder=t('mode_a_placeholder', lang))
        with col2:
            min_votes = st.number_input(t('min_votes', lang),
                                        min_value=0, value=0, step=10)

        segments = ['All'] + sorted(df_idx[cluster_col].dropna().unique().tolist())
        cluster_filter = st.selectbox(t('filter_segment', lang), segments)

        if st.button(t('search_button', lang), type='primary'):
            if query.strip():
                with st.spinner('Searching...' if lang == 'en' else 'Buscando...'):
                    results = recommend_by_query(
                        query, df_idx, embeddings, model,
                        top_n=10, min_votes=min_votes,
                        cluster_filter=None if cluster_filter == 'All' else cluster_filter
                    )
                st.subheader(t('results_title', lang))
                if len(results) == 0:
                    st.info(t('no_results', lang))
                else:
                    for _, row in results.iterrows():
                        c1, c2 = st.columns([5, 1])
                        with c1:
                            st.markdown(f"**{row['rank']}. {row['name']}**")
                            tagline = str(row.get('tagline', ''))
                            if tagline not in ('', 'nan', 'None'):
                                st.caption(tagline)
                            st.caption(f"📂 {row['cluster_name']} · 👍 {int(row['votes']):,} votes · 📅 {int(row['year'])}")
                        with c2:
                            score = row['similarity_score']
                            if score > 0.75:
                                color, bg = '#FFFFFF', '#10B981'
                            elif score > 0.60:
                                color, bg = '#FFFFFF', '#06B6D4'
                            else:
                                color, bg = '#FFFFFF', '#94A3B8'
                            st.markdown(
                                f"<div style='text-align:center;padding:10px 8px;"
                                f"background:{bg};border-radius:8px;"
                                f"color:{color};font-weight:800;font-size:15px;"
                                f"box-shadow:0 2px 8px rgba(0,0,0,0.15);'>"
                                f"{score:.3f}</div>",
                                unsafe_allow_html=True)
                        st.divider()
            else:
                st.warning("Please enter a search query." if lang == 'en'
                           else "Por favor ingresa una consulta.")

    else:
        product_name = st.text_input(t('mode_b_label', lang),
                                     placeholder=t('mode_b_placeholder', lang))

        if st.button(t('find_button', lang), type='primary'):
            if product_name.strip():
                with st.spinner('Finding similar products...' if lang == 'en'
                                else 'Buscando productos similares...'):
                    ref, results = recommend_similar(
                        product_name, df_idx, embeddings, top_n=10)

                if results is None:
                    st.warning(f"Product '{product_name}' not found." if lang == 'en'
                               else f"Producto '{product_name}' no encontrado.")
                else:
                    st.info(
                        f"**{t('ref_product', lang)}:** {ref['name']} · "
                        f"📂 {ref.get('cluster_name', '')} · "
                        f"👍 {int(ref['votes']):,} votes")
                    st.subheader(t('results_title', lang))
                    for _, row in results.iterrows():
                        c1, c2 = st.columns([5, 1])
                        with c1:
                            st.markdown(f"**{row['rank']}. {row['name']}**")
                            tagline = str(row.get('tagline', ''))
                            if tagline not in ('', 'nan', 'None'):
                                st.caption(tagline)
                            st.caption(f"📂 {row['cluster_name']} · 👍 {int(row['votes']):,} votes · 📅 {int(row['year'])}")
                        with c2:
                            score = row['similarity_score']
                            if score > 0.75:
                                color, bg = '#FFFFFF', '#10B981'
                            elif score > 0.60:
                                color, bg = '#FFFFFF', '#06B6D4'
                            else:
                                color, bg = '#FFFFFF', '#94A3B8'
                            st.markdown(
                                f"<div style='text-align:center;padding:10px 8px;"
                                f"background:{bg};border-radius:8px;"
                                f"color:{color};font-weight:800;font-size:15px;"
                                f"box-shadow:0 2px 8px rgba(0,0,0,0.15);'>"
                                f"{score:.3f}</div>",
                                unsafe_allow_html=True)
                        st.divider()
            else:
                st.warning("Please enter a product name." if lang == 'en'
                           else "Por favor ingresa un nombre de producto.")