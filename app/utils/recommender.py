import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def recommend_by_query(query, df, embeddings, model, top_n=10, min_votes=0, cluster_filter=None):
    query_embedding = model.encode([query], normalize_embeddings=True)
    mask = df['votes'] >= min_votes
    if cluster_filter and cluster_filter != 'All':
        mask = mask & (df['cluster_name'] == cluster_filter)
    filtered_idx  = df[mask].index.tolist()
    filtered_embs = embeddings[filtered_idx]
    scores  = cosine_similarity(query_embedding, filtered_embs)[0]
    top_idx = scores.argsort()[-top_n:][::-1]
    results = df.iloc[[filtered_idx[i] for i in top_idx]].copy()
    results['similarity_score'] = scores[top_idx].round(4)
    results['rank'] = range(1, len(results) + 1)
    return results[['rank', 'name', 'tagline', 'cluster_name',
                     'votes', 'year', 'similarity_score']].reset_index(drop=True)

def recommend_similar(product_name, df, embeddings, top_n=10):
    matches = df[df['name'].str.lower().str.contains(product_name.lower(), na=False)]
    if len(matches) == 0:
        return None, None
    ref = matches.loc[matches['votes'].idxmax()]
    ref_idx = ref.name
    ref_emb = embeddings[ref_idx].reshape(1, -1)
    mask = df.index != ref_idx
    filtered_idx  = df[mask].index.tolist()
    filtered_embs = embeddings[filtered_idx]
    scores  = cosine_similarity(ref_emb, filtered_embs)[0]
    top_idx = scores.argsort()[-top_n:][::-1]
    results = df.iloc[[filtered_idx[i] for i in top_idx]].copy()
    results['similarity_score'] = scores[top_idx].round(4)
    results['rank'] = range(1, len(results) + 1)
    return ref, results[['rank', 'name', 'tagline', 'cluster_name',
                          'votes', 'year', 'similarity_score']].reset_index(drop=True)