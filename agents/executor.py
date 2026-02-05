from typing import List, Dict, Any
from .base_agent import BaseAgent
from tools.base_tool import BaseTool
from rich.console import Console

console = Console()

class ExecutorAgent(BaseAgent):
    def __init__(self, llm_client, tools: List[BaseTool]):
        super().__init__(llm_client, "Executor Agent")
        self.tool_map = {tool.name: tool for tool in tools}

    def run(self, plan: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        for step in plan:
            tool_name = step.get("tool")
            tool_args = step.get("args", {})
            
            console.print(f"[bold yellow]Executing Step {step['step']}:[/bold yellow] Use [cyan]{tool_name}[/cyan]")
            
            tool = self.tool_map.get(tool_name)
            if not tool:
                error_msg = f"Tool '{tool_name}' not found."
                console.print(f"[bold red]❌ {error_msg}[/bold red]")
                results.append({"step": step['step'], "tool": tool_name, "status": "error", "error": error_msg})
                continue

            try:
                # Execute the tool
                output = tool.execute(**tool_args)
                console.print(f"[bold green]✅ Result:[/bold green] {str(output)[:200]}..." if len(str(output)) > 200 else f"[bold green]✅ Result:[/bold green] {output}")
                results.append({"step": step['step'], "tool": tool_name, "status": "success", "output": output})
            except Exception as e:
                console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
                results.append({"step": step['step'], "tool": tool_name, "status": "error", "error": str(e)})
                
        return results
