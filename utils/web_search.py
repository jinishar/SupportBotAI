import os
from tavily import TavilyClient

def web_search(query: str) -> str:
    try:
        import streamlit as st
        api_key = st.secrets.get("TAVILY_API_KEY", "")
    except:
        api_key = os.getenv("TAVILY_API_KEY", "")
    
    if not api_key:
        return ""
    try:
        client = TavilyClient(api_key=api_key)
        results = client.search(query=query, max_results=3, search_depth="basic")
        snippets = []
        for r in results.get("results", []):
            snippets.append(f"**{r.get('title','')}**\n{r.get('content','')}\nSource: {r.get('url','')}")
        return "\n\n".join(snippets)
    except Exception as e:
        return ""