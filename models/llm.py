import os
from langchain_groq import ChatGroq

def get_groq_model():
    import streamlit as st
    api_key = st.secrets["GROQ_API_KEY"]
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not set.")
    
    return ChatGroq(api_key=api_key, model_name="llama-3.1-8b-instant")