import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    try:
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except Exception as e:
        raise RuntimeError(f"Failed to initialise embedding model: {e}")