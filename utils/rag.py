import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from config.config import CHROMA_PERSIST_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from models.embeddings import get_embedding_model

LOADERS = {".pdf": PyPDFLoader, ".txt": TextLoader, ".docx": Docx2txtLoader}


def load_documents(file_paths):
    docs = []
    for path in file_paths:
        ext = os.path.splitext(path)[-1].lower()
        loader_cls = LOADERS.get(ext)
        if not loader_cls:
            print(f"[RAG] Unsupported file type: {ext}")
            continue
        try:
            docs.extend(loader_cls(path).load())
        except Exception as e:
            print(f"[RAG] Error loading {path}: {e}")
    return docs


def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(docs)


def build_vector_store(file_paths):
    docs   = load_documents(file_paths)
    chunks = chunk_documents(docs)
    embed  = get_embedding_model()
    return Chroma.from_documents(documents=chunks, embedding=embed, persist_directory=CHROMA_PERSIST_DIR)


def load_vector_store():
    if not os.path.exists(CHROMA_PERSIST_DIR):
        return None
    try:
        return Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=get_embedding_model())
    except Exception as e:
        print(f"[RAG] Could not load vector store: {e}")
        return None


def retrieve_context(query, vector_store, k=4):
    try:
        results = vector_store.similarity_search(query, k=k)
        return "\n\n".join(doc.page_content for doc in results)
    except Exception as e:
        print(f"[RAG] Retrieval error: {e}")
        return ""
