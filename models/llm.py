import os
from langchain_groq import ChatGroq

def get_groq_model():
    try:
        import streamlit as st
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY", "")
    
    if not api_key:
        raise ValueError("GROQ_API_KEY not set.")
    
    return ChatGroq(api_key=api_key, model_name="llama-3.1-8b-instant")