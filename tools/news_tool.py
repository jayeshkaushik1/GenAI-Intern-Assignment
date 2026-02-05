import requests
import os
from typing import Dict, Any, List
from .base_tool import BaseTool

class NewsTool(BaseTool):
    name = "news_tool"
    description = "Fetches top news from India (GNews). Args: query (optional str), count (int, default 5)"

    def to_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Specific topic to search for (optional)"
                        },
                        "count": {
                            "type": "integer",
                            "description": "Number of stories (default 5)"
                        }
                    },
                    "required": []
                }
            }
        }

    def execute(self, query: str = None, count: int = 5) -> str:
        api_key = os.getenv("GNEWS_API_KEY")
        if not api_key:
            return "Error: GNEWS_API_KEY not found in .env"

        try:
            url = "https://gnews.io/api/v4/top-headlines"
            params = {
                "token": api_key,
                "country": "in",
                "lang": "en",
                "max": count
            }
            
            if query:
                url = "https://gnews.io/api/v4/search"
                params["q"] = query
                del params["country"] 
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code != 200:
                return f"Error from GNews API: {data.get('errors', 'Unknown error')}"

            articles = data.get("articles", [])
            if not articles:
                return "No news found."

            results = []
            for art in articles:
                source = art.get("source", {}).get("name", "Unknown")
                results.append(f"- [{source}] {art['title']} ({art['url']})")

            return "\n".join(results)

        except Exception as e:
            return f"Error executing NewsTool: {str(e)}"
