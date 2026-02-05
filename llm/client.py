import os
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from termcolor import colored

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        
        # Auto configure for Groq if key is present but no base_url
        if not self.base_url and os.getenv("GROQ_API_KEY"):
            self.base_url = "https://api.groq.com/openai/v1"
        
        self.model = model
        if self.model == "llama3-70b-8192":
             self.model = "llama-3.3-70b-versatile"

        if not self.api_key:
            print(colored("Warning: No API Key (GROQ_API_KEY or OPENAI_API_KEY) found.", "yellow"))
        
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat_completion(self, messages: List[Dict[str, str]], json_mode: bool = False) -> str:
        """
        Sends a chat completion request to the LLM.
        """
        try:
            kwargs = {
                "model": self.model,
                "messages": messages,
            }
            if json_mode:
                kwargs["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content
            if content:
                content = content.replace("```json", "").replace("```", "").strip()
            return content
        except Exception as e:
            print(colored(f"Error calling LLM: {e}", "red"))
            # return empty JSON in case of error to prevent crash in downstream JSON parsing
            return "{}"
