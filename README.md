<div align="center">

# ⚡ TechPulse
### Product Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live_App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://techpulse-intelligence.streamlit.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Live_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://techpulse-api-xxxr.onrender.com/docs)
[![License](https://img.shields.io/badge/License-MIT-10B981?style=for-the-badge)](LICENSE)
[![README ES](https://img.shields.io/badge/README-Español-10B981?style=for-the-badge)](README.es.md)

**A decade of digital product launches — analyzed, segmented, and forecasted.**

[🚀 Live App](https://techpulse-intelligence.streamlit.app/) · [📡 API Docs](https://techpulse-api-xxxr.onrender.com/docs) · [📄 Report EN](reports/pdf/techpulse_report_en.pdf) · [📄 Informe ES](reports/pdf/techpulse_report_es.pdf)

</div>

---

## 🎯 Overview

TechPulse analyzes **152,556 digital products** launched on Product Hunt between 2014 and 2024. The platform combines three analytical layers to deliver actionable intelligence about the digital product ecosystem:

- **📈 Trend Forecasting** — Holt-Winters + STL decomposition projecting category growth through 2026
- **🗺️ Market Segmentation** — TF-IDF + K-Means + UMAP identifying 10 distinct product segments
- **🤖 Hybrid Recommender** — Sentence Transformers semantic search across 125,579 indexed products

> **Key Finding:** 55.5% of 2024 Product Hunt launches are AI-related — the most significant structural shift in the digital product ecosystem in a decade.

---

## 🌐 Live Deployments

| Service | URL | Status |
|---|---|---|
| Streamlit App | [techpulse-intelligence.streamlit.app](https://techpulse-intelligence.streamlit.app/) | ✅ Live |
| FastAPI | [techpulse-api-xxxr.onrender.com/docs](https://techpulse-api-xxxr.onrender.com/docs) | ✅ Live |

> ⚠️ The API is hosted on Render Free tier — first request may take ~50 seconds to wake up.

---

## 🏗️ Architecture

```
techpulse/
├── notebooks/          ← 7 analytical notebooks (end-to-end pipeline)
│   ├── 01_data_collection.ipynb
│   ├── 02_eda_ecosystem.ipynb
│   ├── 03_trend_forecasting.ipynb
│   ├── 04_product_clustering.ipynb
│   ├── 05_recommendation_engine.ipynb
│   ├── 06_business_insights.ipynb
│   └── 07_report.ipynb
├── app/                ← Streamlit multi-page app (6 pages, bilingual)
│   ├── main.py
│   ├── views/
│   ├── utils/
│   └── i18n.py
├── api/                ← FastAPI REST API (7 endpoints)
│   └── main.py
├── data/
│   ├── external/       ← Raw Kaggle datasets
│   └── processed/      ← Parquet files (master dataset, forecasts, clusters)
├── models/             ← Trained models and recommendation index
└── reports/
    ├── figures/        ← 18 publication-ready visualizations
    └── pdf/            ← Bilingual PDF reports
```

---

## 🔬 Technical Pipeline

| Stage | Notebook | Technology | Output |
|---|---|---|---|
| Data Collection | `01` | Pandas · Parquet · Kaggle API | 152,556 unified products |
| EDA | `02` | Plotly · Seaborn · Matplotlib | 7 visualizations |
| Forecasting | `03` | Holt-Winters · STL | Projections to 2026 |
| Clustering | `04` | TF-IDF · K-Means · UMAP | 10 market segments |
| Recommender | `05` | Sentence Transformers · Cosine Similarity | 125,579 indexed products |
| Business Insights | `06` | Pandas · Plotly | Bilingual executive report |
| PDF Report | `07` | ReportLab | EN + ES reports |

---

## 📊 Key Findings

| Finding | Value |
|---|---|
| Total products analyzed | 152,556 |
| Data coverage | 2014 – 2024 (10 years) |
| AI products in 2024 | **55.5%** of all launches |
| Record year | 2023 — 40,615 launches |
| Fastest growing category | Money (+12.3% projected to 2026) |
| Most engaging segment | Design & Open Source (175 avg votes) |
| Market segments identified | 10 via K-Means + UMAP |
| Recommendation index | 125,579 products · 384 dimensions |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Miniconda or Miniforge

### Setup

```bash
# Clone the repository
git clone https://github.com/anthonylopez-dev/techpulse-product-intelligence.git
cd techpulse-product-intelligence

# Create environment
conda create -n techpulse python=3.11 -y
conda activate techpulse

# Install dependencies
pip install -r requirements.txt
```

### Run the Streamlit App

```bash
cd app
streamlit run main.py
```

### Run the FastAPI

```bash
uvicorn api.main:app --reload --port 8000
# Docs available at http://localhost:8000/docs
```

### Generate Embeddings (required for local recommender)

Run notebook `05_recommendation_engine.ipynb` — embeddings will be saved to `models/sentence_transformer_embeddings.npy`.

---

## 📡 API Reference

Base URL: `https://techpulse-api-xxxr.onrender.com`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API health check |
| GET | `/stats` | Ecosystem overview statistics |
| GET | `/categories` | List all market segments |
| GET | `/trends` | Category forecasts to 2026 |
| GET | `/clusters` | Market segment profiles |
| POST | `/recommend/query` | Recommend by free-text query |
| POST | `/recommend/similar` | Find similar products |

### Example: Recommend by Query

```bash
curl -X POST "https://techpulse-api-xxxr.onrender.com/recommend/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "AI tool to write content automatically", "top_n": 5}'
```

### Example: Find Similar Products

```bash
curl -X POST "https://techpulse-api-xxxr.onrender.com/recommend/similar" \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Notion", "top_n": 5}'
```

---

## 🗺️ Market Segments

| Segment | Products | Avg Votes |
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

## 📁 Data Sources

| Source | Coverage | Records |
|---|---|---|
| Kaggle Historical Dataset | 2014–2021 | 76,700 |
| Kaggle 2023 Dataset | 2023 | 40,615 |
| Kaggle 2024 Dataset | 2024 | 35,241 |
| **Master Dataset** | **2014–2024** | **152,556** |

> Note: 2022 has no available public dataset — documented as a known data gap.

---

## 🔧 Tech Stack

```
Data          → Pandas · NumPy · PyArrow · Parquet
ML/Clustering → Scikit-learn · K-Means · UMAP
Forecasting   → Statsmodels · Holt-Winters · STL
NLP           → Sentence Transformers · TF-IDF
App           → Streamlit · Plotly
API           → FastAPI · Uvicorn
Reports       → ReportLab
DevOps        → Git · GitHub · Streamlit Cloud · Render
```

---

## 🔄 Replicability

This pipeline is fully replicable with any product catalog dataset. Replace the Product Hunt data with your own and deploy the same intelligence system for:

- **Venture Capital** — Identify emerging categories before they peak
- **Product Companies** — Benchmark engagement vs. the market
- **E-commerce** — Recommend products to users semantically
- **Consulting** — Generate market landscape reports automatically

---

## 👤 Author

**Bryan Anthony López Guerrero**  
Data Scientist · Ambato, Ecuador

[![LinkedIn](https://img.shields.io/badge/LinkedIn-anthonylpz-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/anthonylpz)
[![GitHub](https://img.shields.io/badge/GitHub-anthonylopez--dev-181717?style=flat&logo=github)](https://github.com/anthonylopez-dev)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
<sub>Built with ❤️ as part of a Data Science portfolio · June 2026</sub>
</div>
