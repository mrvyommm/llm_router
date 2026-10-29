# Architecture: Reusable LLM Execution Router

**Status:** Initial implementation
**Version:** 0.2

## 1. Architectural objective

Provide a small, reusable Python component for invoking explicitly
selected language models through LiteLLM.

The router handles model execution and response normalization.
Application-specific decisions remain in the application that uses it.

The guiding principle is to keep reusable infrastructure simple and
introduce additional complexity only when a real project requires it.

## 2. Architectural boundaries

### 2.1 Application

The application owns task-specific intelligence, including:

- Selecting a model based on task requirements.
- Choosing between local, free-tier and paid models.
- Defining privacy and spending constraints.
- Evaluating whether a response is satisfactory.
- Deciding whether to retry, change models, revise a prompt or stop.
- Implementing application-specific orchestration and evaluation.

Selection may be determined by a developer, a user, or an intelligent
selection component within the application.

These decisions are not built into the core router.

### 2.2 Router

The router exposes a small execution interface.

Inputs:
- Prompt.
- Explicit model identifier.

Responsibilities:
- Pass the request to the model client.
- Return the client's standardized result.
- Allow execution errors to propagate to the caller.

The router does not select or rank models, evaluate answer quality,
automatically retry, or switch models.

### 2.3 Model client

The client uses the LiteLLM SDK to invoke supported model providers.

It provides an application-level response containing:

- Answer.
- Model identifier.
- Prompt token count, when available.
- Completion token count, when available.
- Total token count, when available.

Provider responses and capabilities can differ. A normalized interface
does not guarantee identical model behavior or response quality.

### 2.4 Model registry

The registry stores lightweight metadata about configured models, such
as their identifiers, providers, cost categories and known capabilities.

The registry is not a live discovery service or health checker.
A configured model is not necessarily reachable, and declared
capabilities are not proof of reliable behavior.

The current router does not depend on the registry for execution.
It may be used by applications that need model metadata.

## 3. Request lifecycle

The initial execution lifecycle is:

1. The application determines which model to use.
2. The application calls the router with a prompt and model identifier.
3. The router delegates the request to the model client.
4. The client invokes the specified model through LiteLLM.
5. The client returns the standardized response.
6. The router returns that response to the application.
7. If execution fails, the error propagates to the application.
8. The application decides what to do next.

A successful invocation does not guarantee a correct or satisfactory
answer. Response evaluation belongs to the application.

## 4. Failure handling and policy boundaries

- The router does not silently select another model.
- The router does not implement automatic retries or fallback.
- Execution errors are exposed to the caller.
- The application decides whether another attempt is appropriate.
- Application-specific spending, privacy and authorization requirements
  must be enforced by the application or an appropriate enforcement
  layer.
- A model recommendation cannot independently authorize restricted
  operations or override enforced policy.
- Secrets must not be committed or exposed in logs.

## 5. Initial implementation

The initial implementation uses:

- Python.
- LiteLLM SDK for model invocation.
- Ollama for local model execution.
- A lightweight model metadata registry.
- unittest and mocked client calls for deterministic tests.

Cloud providers and additional dependencies will be introduced when
required by a concrete application or learning objective.

## 6. Testing strategy

Tests focus on the reusable execution contract:

- Verify that the requested prompt and model identifier are passed to
  the client.
- Verify that the client result is returned unchanged.
- Verify that execution errors propagate to the caller.
- Use mocks to test router behavior independently of provider
  availability.
- Run integration tests against an actual provider to verify real
  execution.

Application-specific model selection and answer-quality evaluation
require separate tests appropriate to each application.

## 7. Future evolution

Additional capabilities will be introduced only when justified by
actual requirements.

Examples include:

- Model selection: when an application needs a reusable selection
  strategy.
- Retry and fallback: when an application's reliability requirements
  justify explicit recovery behavior.
- Evaluation: when response quality must be assessed systematically.
- LangGraph: when meaningful multi-step state and branching justify
  workflow orchestration.
- MCP: when a compatible client needs standardized tool access.
- LiteLLM Proxy: when centralized gateway controls or shared access
  become necessary.

These capabilities are not requirements of the core router.

## 8. Known limitations

The router does not determine the best model for a task or guarantee
that a response is correct.

Provider availability, pricing, quotas and capabilities may change.
The application is responsible for making and evaluating task-specific
decisions.

Successful execution and passing unit tests do not, by themselves,
establish production readiness.
EOF