import os
from dotenv import load_dotenv

load_dotenv()

# Credenciais
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Modelos
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-4o-mini")

# Caminhos
DATA_DIR = "data"
INDEX_DIR = "index"  # ignorado no git, gerado pela ingestão

# Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# LGPD
CONFIDENCIALIDADE_PADRAO = "interno"
