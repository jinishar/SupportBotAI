import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.config import TAVILY_API_KEY, MAX_SEARCH_RESULTS

def web_search(query: str) -> str:
    if not TAVILY_API_KEY:
        return ""
    try:
        from tavily import TavilyClient
        client  = TavilyClient(api_key=TAVILY_API_KEY)
        results = client.search(query=query, max_results=MAX_SEARCH_RESULTS, search_depth="basic")
        snippets = []
        for r in results.get("results", []):
            snippets.append(f"**{r.get('title','')}**\n{r.get('content','')}\nSource: {r.get('url','')}")
        return "\n\n".join(snippets)
    except Exception as e:
        print(f"[WebSearch] Error: {e}")
        return ""