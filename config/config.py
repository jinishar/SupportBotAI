import os

import streamlit as st
GROQ_API_KEY   = st.secrets.get("GROQ_API_KEY", "")
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY", "")

GROQ_MODEL         = "llama-3.1-8b-instant"
CHROMA_PERSIST_DIR = "chroma_db"
CHUNK_SIZE         = 500
CHUNK_OVERLAP      = 50
APP_TITLE          = "SupportAI – Customer Support Bot"
APP_ICON           = "🤖"
MAX_SEARCH_RESULTS = 3