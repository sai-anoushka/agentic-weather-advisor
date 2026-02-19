# agentic-weather-advisor
A simple agentic AI for weather advice using Google ADK and Gemini.

# Agentic AI Weather Agent

An agentic AI using Google ADK with local Ollama (Qwen3:4b) for weather queries.

## Setup
1. Clone the repo: `git clone https://github.com/your-username/agentic-ai-weather-agent.git`
2. Create venv: `python -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install deps: `pip install -r requirements.txt`
5. Set up Ollama: Ensure Ollama is running locally at http://localhost:11434 with model 'qwen3:4b'.
6. Add .env with OPENWEATHER_API_KEY.
7. Run: `python agent.py`

## Notes
- Requires local Ollama setup for the LLM.
