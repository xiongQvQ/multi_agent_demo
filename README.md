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
# OUTPUT_DIR=./outputs (optional - where reports are written)
# SECRET_KEY=replace_with_long_random_string (optional - for future security features)
```

3. Run the demo:
```bash
python main.py
```

Reports and files are written to the directory specified by `OUTPUT_DIR` (defaults to `./outputs`).

Or run the Streamlit UI:
```bash
streamlit run ui/app.py
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

## Security & Safety

- Prompt guardrails are enforced in each agent’s system prompt: external content is untrusted, ignore attempts to override instructions, avoid secrets/PII.
- Outputs are filtered to redact emails/ID-like sequences and to cap very long texts.
- File operations are confined to `OUTPUT_DIR`, with path traversal blocked and only `.md`/`.txt` writes allowed.

## Testing

Run the test suite (uses a fake LLM; no external network needed):
```bash
pytest
```

CI runs on GitHub Actions (`.github/workflows/ci.yml`) with Python 3.11.

## Notes

- If `SERPER_API_KEY` is not set, the search tool uses safe fallback data.
- You can inject a custom LLM/tools for testing via `MultiAgentWorkflow(llm=..., tools=...)`.

## License

MIT. See `LICENSE`.

## Docker

Build the image:
```bash
docker build -t multi-agent-demo:latest .
```

Run with environment and volume mapping:
```bash
docker run --rm -it \
  -e GOOGLE_API_KEY=your_key \
  -e SERPER_API_KEY=optional_key \
  -e OUTPUT_DIR=/data \
  -p 8501:8501 \
  -v "$(pwd)/outputs:/data" \
  multi-agent-demo:latest
```

Or with docker-compose:
```bash
cp .env.example .env
# edit .env to set GOOGLE_API_KEY and (optionally) SERPER_API_KEY
docker compose up --build
```

Then open http://localhost:8501 to use the UI.
