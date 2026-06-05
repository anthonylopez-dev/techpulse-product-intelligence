import streamlit as st
from pathlib import Path
import sys
import importlib.util

APP_DIR = Path(__file__).parent
sys.path.insert(0, str(APP_DIR))

from i18n import t

st.set_page_config(
    page_title="TechPulse — Product Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos globales ────────────────────────────────────
st.markdown("""
<style>
    /* ── Fondo principal ── */
    .stApp { background-color: #F0FDF4; }
    [data-testid="stHeader"] {
        background-color: #F0FDF4;
        border-bottom: 1px solid #BBF7D0;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #022C22 !important;
        border-right: 2px solid #10B981 !important;
    }
    [data-testid="stSidebar"] * { color: #A7F3D0 !important; }
    [data-testid="stSidebar"] hr { border-color: #065F46 !important; }

    /* ── Botones de navegación ── */
    [data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #6EE7B7 !important;
        border: 1px solid #065F46 !important;
        border-radius: 8px !important;
        text-align: left !important;
        padding: 10px 14px !important;
        width: 100% !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #10B981 !important;
        border-color: #10B981 !important;
        color: white !important;
    }
    [data-testid="stSidebar"] .stButton > button:focus {
        background-color: #059669 !important;
        border-color: #059669 !important;
        color: white !important;
        box-shadow: none !important;
    }

    /* ── Selectbox sidebar ── */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #064E3B !important;
        border-color: #065F46 !important;
        color: #A7F3D0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox svg { fill: #6EE7B7 !important; }

    /* ── Métricas ── */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF, #F0FDF4) !important;
        border: 1px solid #BBF7D0 !important;
        border-left: 4px solid #10B981 !important;
        border-radius: 10px !important;
        padding: 16px !important;
        box-shadow: 0 2px 8px rgba(16,185,129,0.08) !important;
    }
    div[data-testid="metric-container"] label {
        color: #059669 !important;
        font-size: 11px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        font-weight: 600 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 800 !important;
        font-size: 24px !important;
    }

    /* ── Títulos ── */
    h1 { color: #022C22 !important; font-weight: 900 !important; }
    h2 { color: #059669 !important; font-weight: 700 !important; }
    h3 { color: #065F46 !important; font-weight: 600 !important; }
    p  { color: #1E293B !important; }

    /* ── Dividers ── */
    hr { border-color: #BBF7D0 !important; }

    /* ── Inputs ── */
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        border: 1px solid #BBF7D0 !important;
        border-left: 3px solid #10B981 !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #10B981 !important;
        box-shadow: 0 0 0 3px rgba(16,185,129,0.15) !important;
    }
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #BBF7D0 !important;
        color: #0F172A !important;
        border-radius: 8px !important;
    }
    .stNumberInput > div > div > input {
        background-color: #FFFFFF !important;
        border: 1px solid #BBF7D0 !important;
        color: #0F172A !important;
        border-radius: 8px !important;
    }

    /* ── Radio ── */
    .stRadio > div {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 12px !important;
        border: 1px solid #BBF7D0 !important;
    }

    /* ── Botón primario ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10B981, #059669) !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
        letter-spacing: 0.5px !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #059669, #047857) !important;
        box-shadow: 0 4px 12px rgba(16,185,129,0.3) !important;
    }

    /* ── Dataframes ── */
    [data-testid="stDataFrame"] {
        border-radius: 10px !important;
        border: 1px solid #BBF7D0 !important;
        overflow: hidden !important;
    }

    /* ── Info boxes ── */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
    }

    /* ── Caption ── */
    .stCaption { color: #059669 !important; font-size: 12px !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #DCFCE7 !important;
        border-radius: 8px !important;
        padding: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #059669 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Estado de idioma ────────────────────────────────────
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'

# ── Sidebar ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 28px 0 16px 0;'>
        <div style='font-size:38px;'>⚡</div>
        <div style='font-size:22px; font-weight:900; color:#10B981;
                    letter-spacing:3px; margin-top:6px;'>TechPulse</div>
        <div style='font-size:9px; color:#6EE7B7; margin-top:6px;
                    letter-spacing:2px; text-transform:uppercase;'>
            Product Intelligence Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    lang_options = {'🇬🇧 English': 'en', '🇪🇸 Español': 'es'}
    selected_lang = st.selectbox(
        "🌐 Language / Idioma",
        options=list(lang_options.keys()),
        index=0 if st.session_state['lang'] == 'en' else 1,
    )
    st.session_state['lang'] = lang_options[selected_lang]
    lang = st.session_state['lang']

    st.divider()

    NAV_OPTIONS = [
        ("🏠", "Overview"    if lang == 'en' else "Inicio",         "p01_overview"),
        ("🌍", "Ecosystem"   if lang == 'en' else "Ecosistema",      "p02_ecosystem"),
        ("📈", "Forecasting" if lang == 'en' else "Forecasting",     "p03_forecasting"),
        ("🗺️", "Market Map"  if lang == 'en' else "Mapa de Mercado", "p04_market_map"),
        ("🤖", "Recommender" if lang == 'en' else "Recomendador",    "p05_recommender"),
        ("👤", "About"       if lang == 'en' else "Acerca de",       "p06_about"),
    ]

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'p01_overview'

    st.markdown(
        "<div style='font-size:9px;color:#6EE7B7;margin-bottom:8px;"
        "letter-spacing:2px;text-transform:uppercase;'>Navigation</div>",
        unsafe_allow_html=True)

    for icon, label, page_id in NAV_OPTIONS:
        if st.button(f"{icon}  {label}", key=f"nav_{page_id}",
                     use_container_width=True):
            st.session_state['current_page'] = page_id
            st.rerun()

    st.divider()
    st.markdown("""
    <div style='font-size:10px; color:#6EE7B7; text-align:center; padding:8px 0;'>
        Bryan A. López Guerrero<br>
        <a href='https://github.com/anthonylopez-dev'
           style='color:#34D399; text-decoration:none; font-weight:600;'>
           github.com/anthonylopez-dev
        </a>
    </div>
    """, unsafe_allow_html=True)

# ── Cargar página con importlib ─────────────────────────
def load_page(page_id):
    page_file = APP_DIR / 'views' / f'{page_id}.py'
    spec   = importlib.util.spec_from_file_location(page_id, page_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

page_id = st.session_state.get('current_page', 'p01_overview')
try:
    page = load_page(page_id)
    page.render(lang)
except Exception as e:
    st.error(f"Error loading page: {e}")
    st.exception(e)