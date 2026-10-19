# Simple Greeting Agent

Simple AI agent that greets users — proof of concept with no MCP integrations.

## Business challenge

Build a simple conversational AI agent that greets users by name and delivers a personalized welcome experience, serving as a proof of concept for AI agent capabilities on SAP BTP.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Demonstrate AI agent capabilities | — | Working PoC deployed | — | AI Agent Development | user |
| User onboarding experience | — | Personalized greeting delivered | — | User Interaction | user |
| Greeting response time | — | Reduced / near-instant | — | Agent Response | user |

## Key Milestones

1. **Agent scaffolded** — Python A2A agent project created with greeting logic
2. **Greeting capability verified** — Agent correctly responds with personalized greetings in local testing
3. **Agent deployed** — Agent running and reachable on SAP BTP
4. **End-to-end test passed** — Greeting interaction confirmed via client call

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash

### Process Hierarchy

```
Lead to Cash
└── Manage Customers and Channels (generic)
    └── Manage and operate sales channels (generic)
        └── Operate omnichannel customer platforms
└── Plan to Optimize Marketing and Sales (generic)
    └── Develop marketing strategy and plans (generic)
        └── Design and manage customer loyalty program
```

### Summary

A greeting agent maps broadly to Lead to Cash under customer engagement and personalized interaction patterns. The core build is a custom AI agent with no dependency on standard SAP products.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Personalized user greeting | None | — | — | — | — | — | Yes | Fully custom Python agent; no SAP product covers this PoC need |
| No external tool/MCP integration | n/a | — | — | — | — | — | No | Intentionally no MCP servers per user requirement |

### Key findings

- No standard SAP product covers the simple greeting agent use case — full custom development required.
- No APIs or MCP servers are needed; the agent operates purely on conversational logic.
- The solution is a minimal Python A2A agent, ideal as a PoC or learning artifact.
- Key Milestones are defined to support OpenTelemetry business step instrumentation downstream.

## Recommendations

### Simple Greeting AI Agent

#### Executive Summary

Minimal Python A2A agent delivering personalized greetings as a PoC.

#### Recommended Solution

Build a lightweight Python-based AI agent following the A2A protocol on SAP BTP. The agent accepts a user message, extracts the user's name or context, and responds with a friendly personalized greeting. No external MCP tools or SAP system integrations are required.

#### Recommended solution category

AI Agent

#### Intent fit
95%
