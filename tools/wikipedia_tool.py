import wikipedia
from typing import Dict, Any
from .base_tool import BaseTool

class WikipediaTool(BaseTool):
    name = "wikipedia_tool"
    description = "Searches Wikipedia for a summary of a topic. Args: query (str)"

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
                            "description": "The topic to search for on Wikipedia"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

    def execute(self, query: str) -> str:
        try:
            # Search for the query to get the best match
            search_results = wikipedia.search(query)
            if not search_results:
                return f"No Wikipedia results found for: {query}"
            
            page_title = search_results[0]
            summary = wikipedia.summary(page_title, sentences=3)
            return f"Wikipedia Summary for '{page_title}':\n{summary}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Wikipedia query is ambiguous. Possible options: {e.options[:5]}"
        except wikipedia.exceptions.PageError:
            return f"Wikipedia page not found for: {query}"
        except Exception as e:
            return f"Error executing WikipediaTool: {str(e)}"
