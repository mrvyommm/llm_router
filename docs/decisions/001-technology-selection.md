# ADR-001: Initial Technology Selection

- Status: Accepted for the initial implementation, subject to validation
- Date: 2026-10-20

## Context

We want to learn AI engineering while building reusable foundations for
future RAG applications, MCP tools and agentic workflows.

We need consistent access to multiple model providers, transparent
routing rules, explicit spending controls and a path toward measured
quality-aware routing.

Reimplementing mature gateway and provider functionality would add
maintenance work without necessarily creating meaningful value.

## Decision 1: Python

Use Python for application logic.

Rationale:
- Fits the existing project and AI ecosystem.
- Supports the intended provider, testing and orchestration libraries.
- Provides a transferable foundation for future projects.

Revisit only if concrete deployment or integration requirements demand
another language.

## Decision 2: LiteLLM SDK before LiteLLM Proxy

Use LiteLLM SDK for initial model invocation.

Rationale:
- Provides a normalized interface across supported providers.
- Avoids implementing multiple provider-specific adapters.
- Keeps the initial application local and simple.

Alternatives:
- Direct provider SDKs: useful for provider-specific functionality but
  increase integration differences.
- LiteLLM Proxy: offers gateway capabilities, but introduces a separate
  service and operational requirements.

Revisit LiteLLM Proxy when centralized credentials, shared budgets,
access control, rate limits or gateway-level observability are actual
requirements.

## Decision 3: Minimal application-owned model registry

Maintain only metadata required for our routing decisions.

Rationale:
- The application needs a consistent view of task-relevant capabilities,
  configuration and policy.
- A minimal registry avoids duplicating a complete provider catalog.
- It allows us to learn the distinction between metadata, availability
  and eligibility.

Alternatives:
- Query provider metadata dynamically for every decision.
- Adopt a dedicated registry or database.

Revisit when the number of models, metadata freshness requirements or
shared access justify a more sophisticated implementation.

## Decision 4: Deterministic routing before learned routing

Implement explicit eligibility and selection rules first.

Rationale:
- Rules are transparent and straightforward to unit-test.
- They establish a baseline against which more complex strategies can
  be measured.
- They allow hard spending and privacy restrictions to remain under
  deterministic control.

Alternatives:
- LLM-based model selection.
- A trained routing model such as RouteLLM.
- Gateway-provided routing features.

These remain candidates. Evaluate them against the same task dataset,
quality requirements, latency and cost before adoption.

## Decision 5: Evaluate before adopting additional frameworks

Use pytest for deterministic application tests. Begin with structured
logging. Consider Promptfoo or another evaluation framework when the
evaluation dataset and requirements are defined.

Do not introduce LangGraph merely to wrap a simple model call. Adopt it
when stateful branching, evaluation, recovery or escalation makes the
workflow meaningfully more complex.

Do not introduce MCP until a concrete client integration and tool
contract justify it.

## Decision 6: Delay gateway deployment

Do not deploy LiteLLM Proxy or a database in the initial phase.

Rationale:
- The initial use case is a local reusable component.
- An extra service increases setup and operational complexity.
- The SDK is sufficient for initial provider invocation.

Revisit when centralized or multi-application operational requirements
justify the additional infrastructure.

## Consequences

Positive:
- Initial architecture remains understandable and testable.
- Mature provider integration is reused.
- Additional complexity requires evidence and an explicit decision.
- Future alternatives can be compared against a documented baseline.

Negative:
- Initial metadata management may be manual.
- The first routing policy will not be quality-optimal.
- Some gateway-level controls will not be available until the deployment
  architecture changes.

## Validation required

Before claiming the design is successful, verify that:

1. Model calls use the intended provider and configuration.
2. Routing decisions are independently testable.
3. Spending restrictions cannot be bypassed by fallback logic.
4. Failures are bounded and understandable.
5. Quality, latency and cost can be measured on a repeatable dataset.

This ADR must be revised if implementation evidence contradicts its
assumptions or requirements change.
