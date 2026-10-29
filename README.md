# Reusable LLM Router

**Status:** Initial implementation
**Version:** 0.2

## 1. Purpose

Build a small, reusable Python component for invoking language models
through a consistent interface.

The router accepts an explicitly selected model and a prompt, delegates
execution through LiteLLM, and returns a standardized response.

The project has two objectives:

1. Learn AI engineering through deliberate design, implementation,
   testing and evaluation.
2. Build reusable foundations for future RAG applications, MCP tools,
   AI agents and other LLM-powered systems.

This is an engineering and learning project. Production readiness is
not assumed.

## 2. Architectural principle

Keep reusable infrastructure simple. Add complexity when a real
application demonstrates a need for it.

The application owns task-specific decisions, including:

- Selecting a model based on the task.
- Defining quality, privacy and spending requirements.
- Evaluating whether a response is satisfactory.
- Deciding whether to retry, change models, revise a prompt or stop.
- Implementing application-specific orchestration.

The router does not implement universal model-selection rules,
automatic fallback, retries or answer-quality evaluation.

## 3. Core components

### Router

File: `src/router.py`

Accepts a prompt and explicit model identifier, delegates execution to
the client, and returns its result.

### Model client

File: `src/llm_client.py`

Uses the LiteLLM SDK to invoke the selected model and returns a
standardized response.

The response contains:

- `answer`
- `model`
- `prompt_tokens`
- `completion_tokens`
- `total_tokens`

Token usage may be unavailable for some providers.

### Model registry

File: `src/model_registry.py`

Stores lightweight metadata about known models and their capabilities.

The router does not depend on the registry to execute a request.
Applications may use registry metadata when implementing their own
selection logic.

## 4. Technology

- Python
- LiteLLM SDK
- Ollama for local model execution
- unittest for automated tests
- dotenv for environment-based configuration

Additional providers and dependencies will be introduced when justified
by a concrete requirement.

## 5. Setup and configuration

Activate the project's virtual environment and install dependencies
from `requirements.txt` if they are not already installed.

Configure the model using the project's `.env` file. The current local
defaults are:

- Model: `ollama/granite4:3b`
- Ollama API base: `http://localhost:11434`

Ensure Ollama is installed, the model is available locally, and the
Ollama service is running before attempting a real invocation.

Keep credentials and other secrets out of source control.

## 6. Usage

from router import route_request

result = route_request(
    prompt="Explain MCP in simple terms.",
    model_id="ollama/granite4:3b",
)

print(result["answer"])

from router import route_request

result = route_request(
    prompt="Explain MCP in simple terms.",
    model_id="gemini/gemini-2.5-flash",
)

print(result["answer"])

From the project root, run:
## 7. Gemini cloud provider

Add your Google AI Studio API key to `.env`:

GEMINI_API_KEY=your_api_key

Keep `.env` out of version control. Never commit API keys.

```bash
PYTHONPATH=src python src/router.py