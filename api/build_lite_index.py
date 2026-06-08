"""
Genera un índice lite de 30k productos para deploy en producción.
Selecciona los productos más votados para máxima relevancia.
"""
import pandas as pd
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

ROOT      = Path(__file__).parent.parent
MODELS    = ROOT / 'models'
PROCESSED = ROOT / 'data' / 'processed'

print("📦 Cargando índice completo...")
df_full    = pd.read_parquet(MODELS / 'recommendation_index.parquet')
emb_full   = np.load(str(MODELS / 'sentence_transformer_embeddings.npy'))

print(f"   Total productos: {len(df_full):,}")

# Seleccionar top 30k por votos
TOP_N = 30000
df_lite = df_full.nlargest(TOP_N, 'votes').copy()
df_lite = df_lite.reset_index(drop=False)  # guardar índice original
orig_idx = df_lite['index'].values
df_lite  = df_lite.drop(columns=['index'])

emb_lite = emb_full[orig_idx]

print(f"   Índice lite: {len(df_lite):,} productos")
print(f"   Votos mínimos en lite: {df_lite['votes'].min():,}")
print(f"   Embeddings shape: {emb_lite.shape}")

# Guardar
df_lite.to_parquet(MODELS / 'recommendation_index_lite.parquet', index=False)
np.save(str(MODELS / 'sentence_transformer_embeddings_lite.npy'), emb_lite)

size_mb = emb_lite.nbytes / 1024 / 1024
print(f"\n✅ Índice lite guardado")
print(f"   Embeddings lite: {size_mb:.1f} MB")
print(f"   Reducción: {(1 - size_mb/184)*100:.0f}% más liviano")