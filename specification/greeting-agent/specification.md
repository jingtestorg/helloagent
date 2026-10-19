# Specification: greeting-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` for full context
- [x] Bootstrap agent code in `assets/greeting-agent/` using instructions from the sap-agent-bootstrap section (invoke from inside `assets/greeting-agent/`, use copy commands — do NOT create files manually)
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

No runtime skills are needed — the greeting agent uses a simple system prompt with no multi-step workflows or domain-specific knowledge bases.

---

## Project-Specific Tasks

### System Prompt & Greeting Logic

- [x] Open `assets/greeting-agent/app/agent.py` and update the `@prompt_section` body (`get_system_prompt`) to instruct the agent to:
  - Greet the user in a warm, friendly tone
  - If the user provides their name, address them by name in the greeting
  - If no name is provided, deliver a friendly generic welcome message
  - Keep responses short and cheerful (1–3 sentences)
  - Do NOT call any external tools or perform any system lookups
- [x] Verify the system prompt does not reference any MCP tools or external resources

### No MCP / No External Integration

- [x] Confirm no `requires` entries are added to `asset.yaml` (no MCP server dependencies)
- [x] Confirm `get_mcp_tools()` is NOT called in `agent.py` (no tool loading needed)
- [x] Confirm no MCP server or translation file tasks are needed for this agent

---

## Business Instrumentation

- [x] Implement business step instrumentation for each milestone from the PRD using structured logging and OpenTelemetry custom spans:
  - `M1` — `M1.achieved: greeting agent scaffolded and running locally` / `M1.missed: agent scaffolding failed or did not start`
  - `M2` — `M2.achieved: personalized greeting returned successfully in local test` / `M2.missed: greeting response did not include expected personalization`
  - `M3` — `M3.achieved: agent deployed and reachable on SAP BTP` / `M3.missed: deployment failed or agent endpoint unreachable`
  - `M4` — `M4.achieved: end-to-end greeting interaction confirmed` / `M4.missed: end-to-end test did not return expected greeting response`
- [x] Follow the pattern `[MILESTONE_ID].[achieved|missed]: [description]` for all log statements
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## Testing

- [x] `conftest.py` only sets `IBD_TESTING=true`
- [x] Write one unit test that validates a message containing a name returns a greeting with that name
- [x] Write one unit test that validates a message without a name returns a generic friendly greeting
- [x] Write one integration test that calls the agent's `invoke` function end-to-end with a mocked LLM response
- [x] Run `pytest` from `assets/greeting-agent/` (no args) — coverage at 77% (≥ 70% threshold met)
- [x] Run `pytest` again from `assets/greeting-agent/` (no args) to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/greeting-agent/`
