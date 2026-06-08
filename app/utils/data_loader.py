import pandas as pd
import numpy as np
from pathlib import Path
import streamlit as st

ROOT      = Path(__file__).parent.parent.parent
PROCESSED = ROOT / 'data' / 'processed'
MODELS    = ROOT / 'models'
FIGURES   = ROOT / 'reports' / 'figures'

@st.cache_data
def load_master():
    df = pd.read_parquet(PROCESSED / 'master_dataset.parquet')
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['year'] = df['created_at'].dt.year.astype(int)
    return df

@st.cache_data
def load_clustered():
    df = pd.read_parquet(PROCESSED / 'clustered_products.parquet')
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['year'] = df['created_at'].dt.year.astype(int)
    return df

@st.cache_data
def load_forecasts():
    return pd.read_parquet(PROCESSED / 'forecasts.parquet')

@st.cache_data
def load_trends():
    return pd.read_parquet(PROCESSED / 'category_trends.parquet')

@st.cache_data
def load_profiles():
    return pd.read_parquet(PROCESSED / 'cluster_profiles.parquet')

@st.cache_data
def load_recommendation_index():
    return pd.read_parquet(MODELS / 'recommendation_index.parquet')

@st.cache_resource
def load_embeddings():
    path = MODELS / 'sentence_transformer_embeddings.npy'
    if path.exists():
        return np.load(str(path))

    # No existe — generamos en runtime
    placeholder = st.empty()
    placeholder.info("⚙️ Generating embeddings for the first time. This takes ~10 minutes...")

    df = load_recommendation_index()

    def build_text(row):
        parts = []
        for col in ['name', 'tagline', 'description']:
            val = str(row.get(col, ''))
            if val not in ('', 'nan', 'None'):
                parts.append(val.strip())
        return ' | '.join(parts)

    texts = df.apply(build_text, axis=1).tolist()

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(
        texts,
        batch_size=256,
        show_progress_bar=False,
        normalize_embeddings=True
    )

    try:
        MODELS.mkdir(parents=True, exist_ok=True)
        np.save(str(path), embeddings)
    except Exception:
        pass

    placeholder.empty()  # ← limpia el mensaje al terminar
    return embeddings

@st.cache_resource
def load_sentence_transformer():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

def plotly_theme(include_axes=True):
    """Tema Plotly esmeralda vibrante — colores sólidos visibles sobre fondo claro."""
    base = dict(
        plot_bgcolor  = 'rgba(255,255,255,0.7)',
        paper_bgcolor = 'rgba(255,255,255,0)',
        font          = dict(color='#065F46', family='sans-serif', size=12),
        legend        = dict(
            font=dict(color='#065F46', size=11),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#BBF7D0',
            borderwidth=1,
        ),
        margin  = dict(t=40, b=40, l=10, r=10),
        colorway= [
            '#059669',
            '#0284C7',
            '#7C3AED',
            '#D97706',
            '#DC2626',
            '#0891B2',
            '#9333EA',
            '#EA580C',
        ],
    )
    if include_axes:
        axis_style = dict(
            gridcolor     = 'rgba(187,247,208,0.9)',
            linecolor     = '#86EFAC',
            tickfont      = dict(color='#059669', size=11),
            title_font    = dict(color='#065F46', size=12),
            zerolinecolor = '#86EFAC',
        )
        base['xaxis'] = axis_style
        base['yaxis'] = axis_style.copy()
    return base