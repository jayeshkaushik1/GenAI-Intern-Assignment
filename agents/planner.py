import json
from typing import List, Dict, Any
from termcolor import colored
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from .base_agent import BaseAgent
from tools.base_tool import BaseTool

console = Console()

class PlannerAgent(BaseAgent):
    def __init__(self, llm_client, tools: List[BaseTool]):
        super().__init__(llm_client, "Planner Agent")
        self.tools = tools

    def run(self, user_query: str):
        tool_schemas = [tool.to_schema() for tool in self.tools]
        system_prompt = f"""
        You are a Planner Agent. Your job is to break down the user's task into a step-by-step plan.
        Available Tools: {json.dumps(tool_schemas, indent=2)}
        
        Return the plan STRICTLY as a JSON object with a key "plan" containing the list of steps.
        Example format:
        {{
            "plan": [
                {{
                    "step": 1,
                    "tool": "tool_name",
                    "args": {{"arg": "value"}},
                    "reasoning": "explanation"
                }}
            ]
        }}

        Return ONLY the JSON object.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]

        console.print(Panel(f"Thinking about: [bold cyan]{user_query}[/bold cyan]", title="Planner"))
        
        response = self.llm.chat_completion(messages, json_mode=True)
        # console.print(f"[dim]Debug raw response: {response}[/dim]")
        
        try:
            plan = json.loads(response)
            # Support if LLM returns a dict with a key 'plan' or just a list
            if isinstance(plan, dict):
                plan = plan.get("plan", plan.get("steps", []))
            
            # Beautified Plan Output
            plan_text = ""
            for step in plan:
                plan_text += f"**Step {step['step']}**: Use `{step['tool']}`\n> {step['reasoning']}\n\n"
            console.print(Panel(Markdown(plan_text), title="Execution Plan", border_style="blue"))
            
            return plan
        except json.JSONDecodeError:
            console.print("[bold red]Error parsing plan JSON[/bold red]")
            return None
