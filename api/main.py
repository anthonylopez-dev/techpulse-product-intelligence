"""
TechPulse — Product Intelligence API
=====================================
FastAPI REST API for product recommendations, trend analysis,
and market segmentation insights.

Author: Bryan Anthony López Guerrero
GitHub: github.com/anthonylopez-dev
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# ── Rutas ────────────────────────────────────────────────
ROOT      = Path(__file__).parent.parent
PROCESSED = ROOT / 'data' / 'processed'
MODELS    = ROOT / 'models'

# ── App ──────────────────────────────────────────────────
app = FastAPI(
    title="TechPulse — Product Intelligence API",
    description="""
## TechPulse Product Intelligence API

A production-ready REST API that powers the TechPulse platform — analyzing
**152,556 digital products** from Product Hunt (2014–2024).

### Capabilities

- **🤖 Semantic Recommendation** — Find relevant products using natural language queries
- **📦 Product Similarity** — Discover products similar to any reference product
- **📈 Trend Forecasting** — Access category growth projections through 2026
- **🗺️ Market Segmentation** — Explore the 10 identified market segments
- **📊 Ecosystem Insights** — Query aggregated statistics about the product ecosystem

### Authentication
This API is currently open (no authentication required).

### Data Sources
- Kaggle Historical Dataset (2014–2021)
- Kaggle 2023–2024 Datasets
- Product Hunt GraphQL API

### Tech Stack
`FastAPI` · `Sentence Transformers` · `Scikit-learn` · `Pandas` · `Parquet`

---
**Author:** Bryan Anthony López Guerrero  
**GitHub:** [github.com/anthonylopez-dev](https://github.com/anthonylopez-dev)  
**LinkedIn:** [linkedin.com/in/anthonylpz](https://linkedin.com/in/anthonylpz)
    """,
    version="1.0.0",
    contact={
        "name": "Bryan Anthony López Guerrero",
        "url": "https://github.com/anthonylopez-dev",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ─────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Schemas ───────────────────────────────────────────────
class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        description="Natural language description of what you are looking for",
        example="AI tool to write and edit content automatically"
    )
    top_n: int = Field(
        default=10,
        ge=1, le=50,
        description="Number of recommendations to return (1-50)"
    )
    min_votes: int = Field(
        default=0,
        ge=0,
        description="Minimum number of votes to filter results"
    )
    cluster_filter: Optional[str] = Field(
        default=None,
        description="Filter results by market segment name",
        example="AI & Generative Tools"
    )

class SimilarRequest(BaseModel):
    product_name: str = Field(
        ...,
        description="Name of the reference product to find similar products for",
        example="Notion"
    )
    top_n: int = Field(
        default=10,
        ge=1, le=50,
        description="Number of similar products to return (1-50)"
    )

class ProductResult(BaseModel):
    rank: int
    name: str
    tagline: Optional[str]
    cluster_name: Optional[str]
    votes: int
    year: int
    similarity_score: float

class RecommendationResponse(BaseModel):
    query: str
    total_results: int
    results: list[ProductResult]
    processing_time_ms: float

class SimilarResponse(BaseModel):
    reference_product: str
    reference_cluster: Optional[str]
    reference_votes: int
    total_results: int
    results: list[ProductResult]
    processing_time_ms: float

class TrendItem(BaseModel):
    category: str
    current_monthly_volume: float
    forecast_2026_monthly: float
    growth_pct: float
    type: str

class ClusterProfile(BaseModel):
    cluster_id: int
    cluster_name: str
    n_products: int
    avg_votes: float
    top_keywords: str

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    data_loaded: bool
    products_indexed: int
    embedding_dimensions: int

# ── Estado global ─────────────────────────────────────────
_state = {
    'df'        : None,
    'embeddings': None,
    'model'     : None,
    'trends'    : None,
    'profiles'  : None,
}

def get_state():
    """Carga lazy de todos los recursos."""
    if _state['df'] is None:
        _state['df'] = pd.read_parquet(MODELS / 'recommendation_index.parquet')

    if _state['trends'] is None:
        _state['trends'] = pd.read_parquet(PROCESSED / 'category_trends.parquet')

    if _state['profiles'] is None:
        _state['profiles'] = pd.read_parquet(PROCESSED / 'cluster_profiles.parquet')

    if _state['embeddings'] is None:
        emb_path = MODELS / 'sentence_transformer_embeddings.npy'
        if emb_path.exists():
            _state['embeddings'] = np.load(str(emb_path))
        else:
            raise HTTPException(
                status_code=503,
                detail="Embeddings not found. Run notebook 05 first."
            )

    if _state['model'] is None:
        from sentence_transformers import SentenceTransformer
        _state['model'] = SentenceTransformer('all-MiniLM-L6-v2')

    return _state

# ── Endpoints ─────────────────────────────────────────────

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health check",
    description="Returns the current status of the API and loaded resources."
)
def health_check():
    try:
        state = get_state()
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            timestamp=datetime.utcnow().isoformat(),
            data_loaded=True,
            products_indexed=len(state['df']),
            embedding_dimensions=state['embeddings'].shape[1],
        )
    except Exception as e:
        return HealthResponse(
            status="degraded",
            version="1.0.0",
            timestamp=datetime.utcnow().isoformat(),
            data_loaded=False,
            products_indexed=0,
            embedding_dimensions=0,
        )

@app.get(
    "/categories",
    tags=["Ecosystem"],
    summary="List available market segments",
    description="Returns all 10 market segments identified by K-Means clustering.",
    response_description="List of segment names"
)
def get_categories():
    state = get_state()
    df = state['df']
    cluster_col = 'cluster_name' if 'cluster_name' in df.columns else 'cluster'
    segments = sorted(df[cluster_col].dropna().unique().tolist())
    return {
        "total_segments": len(segments),
        "segments": segments
    }

@app.get(
    "/trends",
    response_model=list[TrendItem],
    tags=["Forecasting"],
    summary="Get category trend forecasts",
    description="""
Returns trend forecasting data for all analyzed categories.

Each item includes:
- Current monthly volume of product launches
- Projected volume for end of 2026 (Holt-Winters model)
- Growth percentage
- Whether the category is dominant or emerging
    """,
    response_description="List of trend forecasts sorted by growth rate"
)
def get_trends(
    sort_by: str = Query(
        default="growth_pct",
        description="Sort field: 'growth_pct', 'current_monthly_volume', or 'category'",
        example="growth_pct"
    ),
    order: str = Query(
        default="desc",
        description="Sort order: 'asc' or 'desc'",
        example="desc"
    )
):
    state   = get_state()
    trends  = state['trends'].copy()
    ascending = order == 'asc'

    valid_sort = ['growth_pct', 'last_observed', 'category']
    sort_col   = sort_by if sort_by in valid_sort else 'growth_pct'
    if sort_col == 'current_monthly_volume':
        sort_col = 'last_observed'

    trends = trends.sort_values(sort_col, ascending=ascending)

    return [
        TrendItem(
            category=row['category'],
            current_monthly_volume=round(row['last_observed'], 1),
            forecast_2026_monthly=round(row['forecast_2026'], 1),
            growth_pct=round(row['growth_pct'], 1),
            type='dominant' if row['is_dominant'] else 'emerging',
        )
        for _, row in trends.iterrows()
    ]

@app.get(
    "/clusters",
    response_model=list[ClusterProfile],
    tags=["Market Segmentation"],
    summary="Get market segment profiles",
    description="""
Returns profiles for all 10 market segments identified by K-Means clustering on TF-IDF vectors.

Each profile includes:
- Cluster ID and name
- Number of products in the segment
- Average votes (engagement metric)
- Top defining keywords from TF-IDF analysis
    """,
)
def get_clusters():
    state    = get_state()
    profiles = state['profiles'].copy()

    cluster_name_col = 'cluster_name' if 'cluster_name' in profiles.columns else 'cluster'

    return [
        ClusterProfile(
            cluster_id=int(row['cluster']),
            cluster_name=str(row[cluster_name_col]),
            n_products=int(row['n_products']),
            avg_votes=round(float(row['avg_votes']), 1),
            top_keywords=str(row.get('keywords', ''))[:100],
        )
        for _, row in profiles.sort_values('avg_votes', ascending=False).iterrows()
    ]

@app.post(
    "/recommend/query",
    response_model=RecommendationResponse,
    tags=["Recommendations"],
    summary="Recommend products by free-text query",
    description="""
**Mode A** of the hybrid recommendation engine.

Accepts a natural language description of what you are looking for and returns
the most semantically similar products using **Sentence Transformers (all-MiniLM-L6-v2)**
and cosine similarity over 384-dimensional embeddings.

### Examples
- `"AI tool to write and edit content automatically"`
- `"open source design system for developers"`
- `"app to manage personal finances and budget"`
- `"project management tool for remote teams"`

### How it works
1. The query is encoded into a 384-dimensional semantic vector
2. Cosine similarity is computed against all indexed product embeddings
3. Results are ranked by similarity score and filtered by optional constraints
    """,
    response_description="Ranked list of recommended products with similarity scores"
)
def recommend_by_query(request: QueryRequest):
    import time
    start = time.time()

    state      = get_state()
    df         = state['df']
    embeddings = state['embeddings']
    model      = state['model']

    cluster_col = 'cluster_name' if 'cluster_name' in df.columns else 'cluster'

    # Embedding de la query
    query_emb = model.encode([request.query], normalize_embeddings=True)

    # Filtros
    mask = df['votes'] >= request.min_votes
    if request.cluster_filter:
        mask = mask & (df[cluster_col] == request.cluster_filter)

    filtered_idx  = df[mask].index.tolist()
    if not filtered_idx:
        raise HTTPException(status_code=404, detail="No products found with the given filters.")

    filtered_embs = embeddings[filtered_idx]
    scores        = cosine_similarity(query_emb, filtered_embs)[0]
    top_idx       = scores.argsort()[-request.top_n:][::-1]

    results = df.iloc[[filtered_idx[i] for i in top_idx]].copy()
    results['similarity_score'] = scores[top_idx].round(4)

    elapsed = (time.time() - start) * 1000

    return RecommendationResponse(
        query=request.query,
        total_results=len(results),
        results=[
            ProductResult(
                rank=i+1,
                name=str(row['name']),
                tagline=str(row.get('tagline', '')) if str(row.get('tagline', '')) not in ('nan', 'None', '') else None,
                cluster_name=str(row.get(cluster_col, '')),
                votes=int(row['votes']),
                year=int(row['year']) if pd.notna(row.get('year')) else 0,
                similarity_score=float(row['similarity_score']),
            )
            for i, (_, row) in enumerate(results.iterrows())
        ],
        processing_time_ms=round(elapsed, 2),
    )

@app.post(
    "/recommend/similar",
    response_model=SimilarResponse,
    tags=["Recommendations"],
    summary="Find similar products by reference product name",
    description="""
**Mode B** of the hybrid recommendation engine.

Given a reference product name, finds the most semantically similar products
using pre-computed **Sentence Transformer embeddings** and cosine similarity.

### Examples
- `"Notion"` → productivity and template tools
- `"Figma"` → design and collaboration tools
- `"ChatGPT"` → AI and browser extension tools

### How it works
1. The reference product is located in the index (highest-voted match if multiple)
2. Its embedding vector is used as the search query
3. Results are ranked by cosine similarity, excluding the reference product itself
    """,
    response_description="Ranked list of similar products with similarity scores"
)
def recommend_similar(request: SimilarRequest):
    import time
    start = time.time()

    state      = get_state()
    df         = state['df']
    embeddings = state['embeddings']

    cluster_col = 'cluster_name' if 'cluster_name' in df.columns else 'cluster'

    # Buscar producto de referencia
    matches = df[df['name'].str.lower().str.contains(
        request.product_name.lower(), na=False)]

    if len(matches) == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Product '{request.product_name}' not found in the index."
        )

    ref     = matches.loc[matches['votes'].idxmax()]
    ref_idx = ref.name
    ref_emb = embeddings[ref_idx].reshape(1, -1)

    # Excluir el producto mismo
    mask          = df.index != ref_idx
    filtered_idx  = df[mask].index.tolist()
    filtered_embs = embeddings[filtered_idx]

    scores  = cosine_similarity(ref_emb, filtered_embs)[0]
    top_idx = scores.argsort()[-request.top_n:][::-1]

    results = df.iloc[[filtered_idx[i] for i in top_idx]].copy()
    results['similarity_score'] = scores[top_idx].round(4)

    elapsed = (time.time() - start) * 1000

    return SimilarResponse(
        reference_product=str(ref['name']),
        reference_cluster=str(ref.get(cluster_col, '')),
        reference_votes=int(ref['votes']),
        total_results=len(results),
        results=[
            ProductResult(
                rank=i+1,
                name=str(row['name']),
                tagline=str(row.get('tagline', '')) if str(row.get('tagline', '')) not in ('nan', 'None', '') else None,
                cluster_name=str(row.get(cluster_col, '')),
                votes=int(row['votes']),
                year=int(row['year']) if pd.notna(row.get('year')) else 0,
                similarity_score=float(row['similarity_score']),
            )
            for i, (_, row) in enumerate(results.iterrows())
        ],
        processing_time_ms=round(elapsed, 2),
    )

@app.get(
    "/stats",
    tags=["Ecosystem"],
    summary="Get ecosystem overview statistics",
    description="""
Returns high-level statistics about the analyzed Product Hunt ecosystem.

Includes:
- Total products indexed
- Date range coverage
- Top categories by volume
- Engagement statistics
    """,
)
def get_stats():
    state = get_state()
    df    = state['df']

    cluster_col = 'cluster_name' if 'cluster_name' in df.columns else 'cluster'

    return {
        "total_products_indexed": len(df),
        "embedding_model"       : "all-MiniLM-L6-v2",
        "embedding_dimensions"  : 384,
        "market_segments"       : int(df[cluster_col].nunique()),
        "engagement": {
            "avg_votes"   : round(float(df['votes'].mean()), 1),
            "median_votes": round(float(df['votes'].median()), 1),
            "max_votes"   : int(df['votes'].max()),
            "top_product" : str(df.loc[df['votes'].idxmax(), 'name']),
        },
        "segments_overview": df.groupby(cluster_col)['votes'].agg(
            count='count', avg_votes='mean'
        ).round(1).reset_index().rename(
            columns={cluster_col: 'segment'}
        ).to_dict(orient='records'),
    }