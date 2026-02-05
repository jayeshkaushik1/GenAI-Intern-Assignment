# GenAI Intern Assignment – AI Operations Assistant
An end-to-end multi agent AI system that can plan tasks, execute them using real world APIs, and verify results to produce a final human readable answer.

The assistant supports:

- Weather information

- GitHub repository search

- Indian news

- Stock prices (NSE/BSE)

- Wikipedia 

Built with a **Planner-Executor-Verifier** architecture and a beautiful CLI interface.

## Quick Start

```bash
# After setup
python3 main.py
```

## Architecture

The system follows a multi-agent architectural pattern:

1.  **Planner Agent**:
    *   **Role**: Analyzes the user's request.
    *   **Output**: Generates a JSON plan with specific tool calls.

2.  **Executor Agent**:
    *   **Role**: Executes the plan using specific tools.
    *   **Tools**:
        *   `WeatherTool`: Real-time weather (OpenMeteo).
        *   `GitHubTool`: Repository search.
        *   `NewsTool`: **GNews API**.
        *   `StockTool`: **Yahoo Finance (NSE/BSE Support)**.
        *   `WikipediaTool`: Summaries and infos.

3.  **Verifier Agent**:
    *   **Role**: Reviews results and synthesizes a final answer.
    *   **Output**: A clean, bulleted list of facts.

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- API Keys for Groq (LLM) and GNews.
  
### 2. Clone Repository
```bash
git clone https://github.com/jayeshkaushik1/GenAI-Intern-Assignment.git
cd GenAI-Intern-Assignment
```

### 3. Installation
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure Environment
cp .env.example .env
```

### 4. Configuration
Edit `.env` and add your keys:
```env
# Required: LLM Provider
GROQ_API_KEY=... 

# Required: News Tool
GNEWS_API_KEY=...
```

### 5. Run the Project
```bash
python main.py
```

## Example Prompts

Try these commands to see the assistant in action:

1.  **City Weather**:
    ```bash
    python3 main.py "What is the current temperature in New Delhi and Mumbai?"
    ```

2.  **Stocks (NSE/BSE)**:
    ```bash
    python3 main.py "Get the stock price of Reliance and Eternal"
    ```
    *(Note: It automatically handles symbols like `Reliance.NS` and `Eternal.NS`)*

3.  **News**:
    ```bash
    python3 main.py "Top news today"
    ```
    
4. **Wikipedia**:

    ```bash
    python3 main.py "Who is Mukesh Ambani"
    ```

5.  **Complex Multi-Step**:
    ```bash
    python3 main.py "Check the weather in Bangalore and find the latest news about ISRO"
    ```

## Integrated APIs

1.  **Groq API**:
    *   **Purpose**: Provides the LLM reasoning engine (Llama 3.3 70B Versatile).
    *   **Usage**: Planning, reasoning, and result verification.

2.  **OpenMeteo API**:
    *   **Purpose**: Real-time weather data.
    *   **Auth**: Public (No key required).

3.  **GitHub API**:
    *   **Purpose**: Searches GitHub repositories and retrieves repository metadata.
    *   **Auth**: Public (Rate limited) or Token-based.
    
4.  **GNews API**:
    *   **Purpose**: Fetches the latest news headlines from India and topic based news.
    *   **Auth**: API Key (GNEWS_API_KEY).
    
5.  **Yahoo Finance API (via yfinance)**:
    *   **Purpose**: Retrieves stock prices for Indian (NSE/BSE) and global markets.
    *   **Auth**: Public (No API key required).
6.  **Wikipedia API (via Python wikipedia library)**:
    *   **Purpose**: Fetches short summaries for informational and encyclopedic queries.
    *   **Auth**: Public (No API key required).


## Known Limitations

1.  **API Rate Limits:**: Free tier APIs may enforce request limits under heavy usage.
2.  **Stock Delay**: Data is fetched from Yahoo Finance, which may have a slight delay compared to real time trading terminals.
3.  **Context Window:** Very large outputs may be truncated due to LLM context limits.

## Project Structure

A detailed overview of the codebase:

```text
ai_ops_assistant/
├── agents/                     # Core Agent Logic
│   ├── base_agent.py           # Base class for all agents
│   ├── planner.py              # Plan Agent: Decomposes tasks into JSON steps
│   ├── executor.py             # Execute Agent: Runs tools (API calls) safely
│   └── verifier.py             # Verify Agent: Synthesizes final answer and checks quality
│
├── tools/                      # Tool Integrations (Skills)
│   ├── base_tool.py            # Abstract base class for tools
│   ├── weather_tool.py         # OpenMeteo API (Weather data)
│   ├── news_tool.py            # GNews API
│   ├── stock_tool.py           # Yahoo Finance (NSE/BSE support)
│   ├── wikipedia_tool.py       # Wikipedia Summary API
│   └── github_tool.py          # GitHub API (Repo search)
│
├── llm/                        # LLM Interface
│   └── client.py               # Groq/OpenAI Client wrapper with error handling
│
├── main.py                     # Entry Point (CLI and Interaction Loop)
├── .env.example                # Template for API keys
└── requirements.txt            # Python dependencies
```
Made with ❤️ by Jayesh Kaushik

Questions? 
Issues? 
Open a GitHub issue!
