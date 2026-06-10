<div align="center">

# ⚡ TechPulse
### Plataforma de Inteligencia de Productos

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App_en_Vivo-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://techpulse-intelligence.streamlit.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API_en_Vivo-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://techpulse-api-xxxr.onrender.com/docs)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-10B981?style=for-the-badge)](LICENSE)
[![README EN](https://img.shields.io/badge/README-English-3776AB?style=for-the-badge)](README.md)

**Una década de lanzamientos de productos digitales — analizados, segmentados y proyectados.**

[🚀 App en Vivo](https://techpulse-intelligence.streamlit.app/) · [📡 Documentación API](https://techpulse-api-xxxr.onrender.com/docs) · [📄 Informe ES](reports/pdf/techpulse_report_es.pdf) · [📄 Report EN](reports/pdf/techpulse_report_en.pdf)

</div>

---

## 🎯 Descripción General

TechPulse analiza **152,556 productos digitales** lanzados en Product Hunt entre 2014 y 2024. La plataforma combina tres capas analíticas para entregar inteligencia accionable sobre el ecosistema de productos digitales:

- **📈 Forecasting de Tendencias** — Holt-Winters + descomposición STL proyectando el crecimiento de categorías hasta 2026
- **🗺️ Segmentación de Mercado** — TF-IDF + K-Means + UMAP identificando 10 segmentos distintos de productos
- **🤖 Recomendador Híbrido** — Búsqueda semántica con Sentence Transformers sobre 125,579 productos indexados

> **Hallazgo clave:** El 55.5% de los lanzamientos de 2024 en Product Hunt son productos relacionados con IA — el cambio estructural más significativo en el ecosistema de productos digitales en una década.

---

## 🌐 Deploys en Producción

| Servicio | URL | Estado |
|---|---|---|
| App Streamlit | [techpulse-intelligence.streamlit.app](https://techpulse-intelligence.streamlit.app/) | ✅ En vivo |
| FastAPI | [techpulse-api-xxxr.onrender.com/docs](https://techpulse-api-xxxr.onrender.com/docs) | ✅ En vivo |

> ⚠️ La API está en Render Free tier — el primer request puede tardar ~50 segundos en despertar.

---

## 🏗️ Arquitectura

```
techpulse/
├── notebooks/          ← 7 notebooks analíticos (pipeline end-to-end)
│   ├── 01_data_collection.ipynb
│   ├── 02_eda_ecosystem.ipynb
│   ├── 03_trend_forecasting.ipynb
│   ├── 04_product_clustering.ipynb
│   ├── 05_recommendation_engine.ipynb
│   ├── 06_business_insights.ipynb
│   └── 07_report.ipynb
├── app/                ← App Streamlit multi-página (6 páginas, bilingüe)
│   ├── main.py
│   ├── views/
│   ├── utils/
│   └── i18n.py
├── api/                ← API REST FastAPI (7 endpoints)
│   └── main.py
├── data/
│   ├── external/       ← Datasets crudos de Kaggle
│   └── processed/      ← Archivos Parquet (dataset maestro, forecasts, clusters)
├── models/             ← Modelos entrenados e índice de recomendación
└── reports/
    ├── figures/        ← 18 visualizaciones publicables
    └── pdf/            ← Informes PDF bilingüe
```

---

## 🔬 Pipeline Técnico

| Etapa | Notebook | Tecnología | Output |
|---|---|---|---|
| Recolección de Datos | `01` | Pandas · Parquet · Kaggle API | 152,556 productos unificados |
| EDA | `02` | Plotly · Seaborn · Matplotlib | 7 visualizaciones |
| Forecasting | `03` | Holt-Winters · STL | Proyecciones hasta 2026 |
| Clustering | `04` | TF-IDF · K-Means · UMAP | 10 segmentos de mercado |
| Recomendador | `05` | Sentence Transformers · Similitud Coseno | 125,579 productos indexados |
| Insights de Negocio | `06` | Pandas · Plotly | Informe ejecutivo bilingüe |
| Informe PDF | `07` | ReportLab | Informes EN + ES |

---

## 📊 Hallazgos Clave

| Hallazgo | Valor |
|---|---|
| Total de productos analizados | 152,556 |
| Cobertura de datos | 2014 – 2024 (10 años) |
| Productos AI en 2024 | **55.5%** de todos los lanzamientos |
| Año récord | 2023 — 40,615 lanzamientos |
| Categoría de mayor crecimiento | Money (+12.3% proyectado a 2026) |
| Segmento más engaging | Design & Open Source (175 votos promedio) |
| Segmentos de mercado identificados | 10 via K-Means + UMAP |
| Índice de recomendación | 125,579 productos · 384 dimensiones |

---

## 🚀 Instalación Local

### Requisitos
- Python 3.11+
- Miniconda o Miniforge

### Configuración

```bash
# Clonar el repositorio
git clone https://github.com/anthonylopez-dev/techpulse-product-intelligence.git
cd techpulse-product-intelligence

# Crear entorno
conda create -n techpulse python=3.11 -y
conda activate techpulse

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la App Streamlit

```bash
cd app
streamlit run main.py
```

### Ejecutar la FastAPI

```bash
uvicorn api.main:app --reload --port 8000
# Documentación disponible en http://localhost:8000/docs
```

### Generar Embeddings (requerido para el recomendador local)

Ejecuta el notebook `05_recommendation_engine.ipynb` — los embeddings se guardarán en `models/sentence_transformer_embeddings.npy`.

---

## 📡 Referencia de la API

URL base: `https://techpulse-api-xxxr.onrender.com`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/health` | Estado de la API |
| GET | `/stats` | Estadísticas generales del ecosistema |
| GET | `/categories` | Listar todos los segmentos de mercado |
| GET | `/trends` | Forecasts de categorías hasta 2026 |
| GET | `/clusters` | Perfiles de segmentos de mercado |
| POST | `/recommend/query` | Recomendar por consulta en texto libre |
| POST | `/recommend/similar` | Encontrar productos similares |

### Ejemplo: Recomendar por Consulta

```bash
curl -X POST "https://techpulse-api-xxxr.onrender.com/recommend/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "herramienta de IA para escribir contenido automáticamente", "top_n": 5}'
```

### Ejemplo: Encontrar Productos Similares

```bash
curl -X POST "https://techpulse-api-xxxr.onrender.com/recommend/similar" \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Notion", "top_n": 5}'
```

---

## 🗺️ Segmentos de Mercado

| Segmento | Productos | Votos Promedio |
|---|---|---|
| Design & Open Source | ~9,300 | 175 |
| Email & Marketing | ~2,900 | 171 |
| Business & Data Insights | ~11,700 | 139 |
| Browser Extensions | ~4,700 | 134 |
| Mobile Apps | ~11,700 | 126 |
| General Tech Products | ~53,000 | 121 |
| Social Media & Content | ~3,100 | 116 |
| Productivity & Templates | ~9,300 | 113 |
| Online Tools & Platforms | ~5,300 | 90 |
| AI & Generative Tools | ~16,200 | 86 |

---

## 📁 Fuentes de Datos

| Fuente | Cobertura | Registros |
|---|---|---|
| Dataset Histórico Kaggle | 2014–2021 | 76,700 |
| Dataset Kaggle 2023 | 2023 | 40,615 |
| Dataset Kaggle 2024 | 2024 | 35,241 |
| **Dataset Maestro** | **2014–2024** | **152,556** |

> Nota: 2022 no tiene dataset público disponible — documentado como gap de datos conocido.

---

## 🔧 Stack Técnico

```
Datos         → Pandas · NumPy · PyArrow · Parquet
ML/Clustering → Scikit-learn · K-Means · UMAP
Forecasting   → Statsmodels · Holt-Winters · STL
NLP           → Sentence Transformers · TF-IDF
App           → Streamlit · Plotly
API           → FastAPI · Uvicorn
Informes      → ReportLab
DevOps        → Git · GitHub · Streamlit Cloud · Render
```

---

## 🔄 Replicabilidad

Este pipeline es completamente replicable con cualquier dataset de catálogo de productos. Sustituye los datos de Product Hunt con los tuyos y despliega el mismo sistema de inteligencia para:

- **Capital de Riesgo** — Identificar categorías emergentes antes de que alcancen su pico
- **Empresas de Producto** — Hacer benchmarking de engagement vs. el mercado
- **E-commerce** — Recomendar productos a usuarios semánticamente
- **Consultoría** — Generar reportes de paisaje de mercado automáticamente

---

## 👤 Autor

**Bryan Anthony López Guerrero**  
Científico de Datos · Ambato, Ecuador

[![LinkedIn](https://img.shields.io/badge/LinkedIn-anthonylpz-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/anthonylpz)
[![GitHub](https://img.shields.io/badge/GitHub-anthonylopez--dev-181717?style=flat&logo=github)](https://github.com/anthonylopez-dev)

---

## 📄 Licencia

Licencia MIT — ver [LICENSE](LICENSE) para más detalles.

---

<div align="center">
<sub>Construido con ❤️ como parte de un portafolio de Ciencia de Datos · Junio 2026</sub>
</div>
