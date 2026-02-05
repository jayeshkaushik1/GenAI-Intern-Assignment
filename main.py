import os
import sys
import argparse
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from llm.client import LLMClient
from tools.weather_tool import WeatherTool
from tools.github_tool import GitHubTool
from tools.news_tool import NewsTool
from tools.wikipedia_tool import WikipediaTool
from tools.stock_tool import StockTool
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent

# Load environment variables
load_dotenv()

console = Console()

def run_flow(query, planner, executor, verifier):
    # 1. Plan
    plan = planner.run(query)
    if not plan:
        console.print("[bold red]❌ Failed to generate a plan.[/bold red]")
        return

    # 2. Execute
    results = executor.run(plan)
    
    # 3. Verify
    verifier.run(query, results)

def main():
    parser = argparse.ArgumentParser(description="AI Operations Assistant")
    parser.add_argument("query", nargs="?", help="The natural language task to perform")
    args = parser.parse_args()

    # check for API key
    if not (os.getenv("OPENAI_API_KEY") or os.getenv("GROQ_API_KEY")):
         console.print("[bold red]Error: OPENAI_API_KEY or GROQ_API_KEY not found. Please set it in .env[/bold red]")
         return

    # Initialize Components
    llm = LLMClient()
    
    tools = [
        WeatherTool(),
        GitHubTool(),
        NewsTool(),
        WikipediaTool(),
        StockTool()
    ]
    
    planner = PlannerAgent(llm, tools)
    executor = ExecutorAgent(llm, tools)
    verifier = VerifierAgent(llm)

    # Welcome Banner
    console.print(Panel.fit(
        "[bold green]AI Operations Assistant[/bold green]\n"
        "[italic]Powered by Groq & Llama 3[/italic]\n\n"
        "Available Tools:\n"
        " - 🌤️  Weather (OpenMeteo)\n"
        " - 🐙 GitHub\n"
        " - 📰 News (GNews India)\n"
        " - 📈 Stocks (NSE/BSE)\n"
        " - 📖 Wikipedia",
        border_style="green",
        title="Welcome"
    ))

    # Get Query
    if args.query:
        run_flow(args.query, planner, executor, verifier)
    else:
        while True:
            query = console.input("\n[bold cyan]👤 User (or 'exit'):[/bold cyan] ")
            if query.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye! 👋[/yellow]")
                break
            if not query.strip():
                continue
            run_flow(query, planner, executor, verifier)

if __name__ == "__main__":
    main()
