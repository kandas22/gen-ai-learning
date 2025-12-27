"""Web search functionality using SerpAPI"""
from typing import Dict, Any
from serpapi import GoogleSearch
from config import Config

async def search_web(query: str, num_results: int = 10) -> Dict[str, Any]:
    """
    Perform web search using SerpAPI
    
    Args:
        query: Search query string
        num_results: Number of results to return
    
    Returns:
        Dictionary containing search results
    """
    try:
        search = GoogleSearch({
            "q": query,
            "api_key": Config.SERPAPI_API_KEY,
            "num": num_results,
            "tbs": "qdr:m",  # Past month for latest results
            "sort": "date"   # Newest first
        })
        
        results = search.get_dict()
        organic_results = results.get("organic_results", [])
        
        # Format results
        formatted_results = []
        for result in organic_results:
            formatted_results.append({
                "position": result.get("position", 0),
                "title": result.get("title", ""),
                "link": result.get("link", ""),
                "snippet": result.get("snippet", ""),
                "source": result.get("source", "")
            })
        
        return {
            "query": query,
            "results_count": len(formatted_results),
            "results": formatted_results,
            "status": "success"
        }
    
    except Exception as e:
        return {
            "query": query,
            "results_count": 0,
            "results": [],
            "status": "error",
            "error": str(e)
        }
