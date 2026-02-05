import requests
import os
from typing import Dict, Any
from .base_tool import BaseTool

class GitHubTool(BaseTool):
    name = "github_tool"
    description = "Searches for GitHub repositories and returns details (stars, description). Args: query (str)"

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
                            "description": "The search query for repositories"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

    def execute(self, query: str) -> str:
        try:
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=3"
            headers = {"Accept": "application/vnd.github.v3+json"}
            
            # Use token if available to avoid rate limits
            token = os.getenv("GITHUB_TOKEN")
            if token and token != "optional_github_token_here":
                headers["Authorization"] = f"token {token}"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                return f"Error searching GitHub: {response.status_code} - {response.text}"
            
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                return f"No repositories found for query: {query}"
            
            results = []
            for item in items:
                repo_info = (
                    f"Name: {item['full_name']}\n"
                    f"Stars: {item['stargazers_count']}\n"
                    f"Description: {item['description']}\n"
                    f"URL: {item['html_url']}\n"
                )
                results.append(repo_info)
            
            return "\n---\n".join(results)
        except Exception as e:
            return f"Error executing GitHubTool: {str(e)}"
