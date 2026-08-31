# Episode 01 — Agentic Loop & `stop_reason`

This episode introduces the foundation of how a Claude-powered agent works.

The main focus is the **agentic loop** — how Claude reasons, requests tools, receives tool results, continues processing, and finally decides when the task is complete.

---

## 🎯 Learning Objectives

By the end of this episode, you should understand:

- The difference between a normal chat and an AI agent
- `system`, `user`, and `assistant` roles
- How Claude uses tools
- How an agentic loop works
- What `stop_reason` represents
- The difference between:
  - `tool_use`
  - `end_turn`
- Why conversation history must be preserved
- Why the complete assistant response must be appended before tool results
- How to prevent an agentic loop from running indefinitely

---

## 🧠 Chat vs Agent

A normal chat is usually simple:

```text
User
  ↓
Claude
  ↓
Final Response
