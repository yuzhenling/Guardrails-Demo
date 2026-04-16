# Guardrails minimal runnable demo

This project is a minimal NeMo Guardrails (Colang 1.0) setup that demonstrates:

- A **dialog rail** that replies deterministically on greetings (including Chinese).
- A **dialog rail** that refuses common jailbreak / prompt-leak requests.
- **Fallback to LLM** for everything else.

## Setup

Use the existing venv in this repo:

```bash
./.venv/bin/python -m ensurepip --upgrade
./.venv/bin/python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org nemoguardrails openai
```

Make sure Ollama is running locally (default `http://localhost:11434`), and you have the model pulled
(this repo defaults to `deepseek-r1:8b`).

## Run

```bash
./.venv/bin/python run_min.py
```

## Where things live

- `config/config.yml`: LLM + rails enablement.
- `config/rails.co`: Colang flows (greeting + jailbreak refusal).
- `run_min.py`: loads the config and runs a small smoke test.

