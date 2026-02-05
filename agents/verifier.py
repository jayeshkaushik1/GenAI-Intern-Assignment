import json
from termcolor import colored
from .base_agent import BaseAgent
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

class VerifierAgent(BaseAgent):
    def __init__(self, llm_client):
        super().__init__(llm_client, "Verifier Agent")

    def run(self, original_query, execution_results):
        system_prompt = """
        You are the Verifier Agent.
        Review the execution results against the original query.
        Synthesize a final natural language answer.
        
        Return JSON strictly.
        Format the answer as a list of strings called "answer_points", where each string is a bullet point.
        
        Return JSON:
        {
            "answer_points": [
                "Point 1...",
                "Point 2..."
            ],
            "success": true
        }
        """
        
        user_content = f"Query: {original_query}\nResults: {json.dumps(execution_results)}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        console.print("[bold magenta]Verifying results...[/bold magenta]")
        response = self.llm.chat_completion(messages, json_mode=True)
        
        try:
            data = json.loads(response)
            
            points = data.get("answer_points", [])
            if not points and "final_answer" in data:
                 final_answer = data["final_answer"]
            else:
                 final_answer = "\n".join([f"- {p}" for p in points]) if points else "No answer provided."
            
            # Print Final Answer
            console.print(Panel(Markdown(final_answer), title="Final Answer", style="green", border_style="green"))
            return response 
        except Exception as e:
             console.print(f"[bold red]Verification Error: {e}[/bold red]")
             console.print(f"[dim]Raw Response: {response}[/dim]")
             return response
