# ReadyTensor Multi-Agent Demo

A simple multi-agent system built with LangGraph, Gemini, and LangChain to demonstrate agent coordination and tool usage.

## Features

- **3 Agents**: Researcher, Analyst, Reporter
- **3 Tools**: Search, Calculator, File processing
- **Orchestration**: LangGraph workflow management
- **LLM**: Google Gemini integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys:
# GOOGLE_API_KEY=your_gemini_api_key_here
# SERPER_API_KEY=your_serper_api_key_here (optional - for real search)
```

3. Run the demo:
```bash
python main.py
```

## API Keys

- **GOOGLE_API_KEY**: Required for Gemini LLM
- **SERPER_API_KEY**: Optional for real Google search via Serper.dev API (falls back to simulated search if not provided)

## Architecture

```
User Input → Researcher (Search) → Analyst (Calculate) → Reporter (Generate Report) → Output
```

## Demo Example

Ask: "Analyze Apple's stock performance"
- Researcher: Searches for Apple stock information
- Analyst: Calculates relevant metrics
- Reporter: Generates final analysis report