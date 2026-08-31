# Episode 02 — Multi-Agent Systems & Coordinator Patterns

## Goal

Understand how to design a multi-agent system using a central Coordinator
and specialized Sub-Agents.

The main pattern covered in this episode is the Hub-and-Spoke architecture.

---

## 1. Why Multi-Agent Systems?

A single agent can become difficult to manage when the task contains
multiple independent areas of work.

Common problems with a single-agent approach:

- Sequential bottlenecks
- Lack of specialization
- Generic results
- Increased latency when many independent tasks must be handled

Multi-agent architecture solves this by splitting work into specialized
sub-agents that can execute independently and, where possible, in parallel.

---

## 2. Hub-and-Spoke Architecture

The architecture contains:

    User
      |
      v
  Coordinator
   /   |   \
  v    v    v
Sub A Sub B Sub C
   \   |   /
      v
  Coordinator
      |
      v
 Final Result

### Coordinator

The Coordinator is the central agent.

Its responsibilities are:

1. Task decomposition
2. Delegation
3. Result aggregation
4. Error handling

All communication should route through the Coordinator.

Sub-agents should not directly communicate with each other.

---

## 3. Task Decomposition

The Coordinator breaks a large task into smaller,
scoped and assignable pieces.

Example:

Research a topic

    Coordinator
       |
       +-- Research Sub-Agent
       +-- Market Sub-Agent
       +-- Technical Sub-Agent
       +-- Writing/Synthesis Sub-Agent

Each sub-agent should have a specific responsibility.

---

## 4. Delegation

The Coordinator decides:

- Which sub-agent is required
- What task the sub-agent should perform
- What context the sub-agent needs
- Which tools the sub-agent is allowed to use

In Claude's agent/SDK patterns, the Coordinator uses the
`task` capability/tool to spawn a sub-agent.

The Coordinator needs the ability to use `task`.

Sub-agents should not normally receive the ability to spawn
more sub-agents, otherwise the architecture can become uncontrolled
or recursive.

---

## 5. Agent Definition

When spawning a sub-agent, the Coordinator provides an agent definition.

Important components:

- `description`
- `prompt`
- `allowed_tools`
- `model`

### Meaning

`description`
: Defines the sub-agent's purpose and role.

`prompt`
: Defines the task, goal, constraints and required context.

`allowed_tools`
: Defines the tools that this particular sub-agent is permitted to use.

`model`
: Defines the model used by the sub-agent.

---

## 6. Parallel Sub-Agent Execution

Independent tasks should be executed in parallel when possible.

If the Coordinator needs three independent sub-agents:

    Sub-Agent 1
    Sub-Agent 2
    Sub-Agent 3

the Coordinator should emit multiple task tool calls
in a single response.

Conceptually:

    Coordinator response
        |
        +-- task -> Sub-Agent 1
        +-- task -> Sub-Agent 2
        +-- task -> Sub-Agent 3

Parallel execution reduces latency.

If execution is sequential:

    S1 -> S2 -> S3

total time is approximately:

    S1 + S2 + S3

For parallel execution:

    S1
    S2
    S3

total time is approximately:

    max(S1, S2, S3)

---

## 7. Context Isolation

This is one of the most important concepts.

A sub-agent starts with a blank context.

It does NOT automatically inherit:

- Coordinator conversation history
- Other sub-agent conversations
- Previous research results
- User conversation history

Therefore, the Coordinator must explicitly provide the
required context when spawning the sub-agent.

### Important Rule

Sub-agent context = whatever the Coordinator explicitly provides.

---

## 8. Context Injection

Bad:

    "Here are some research notes.
     Create the final report."

The sub-agent does not actually know what those research notes are
unless the content is included.

Good:

    Coordinator collects research results

          |
          v

    Coordinator builds structured context

          |
          v

    Coordinator passes that context
    inside the sub-agent prompt

          |
          v

    Synthesis Sub-Agent

The Coordinator is responsible for constructing the context
needed by the sub-agent.

---

## 9. Good vs Bad Sub-Agent Prompting

### Good

Specify:

- The goal
- Relevant context
- Constraints
- Expected responsibility
- Guardrails

Example:

    "Analyze the provided research findings and identify
     evidence supporting and contradicting the claim.
     Use only the supplied evidence."

### Bad

Do not over-specify the exact execution steps unnecessarily.

Example:

    "First go to website A.
     Then search page B.
     Then click C.
     Then generate the report."

The model should generally be given the goal and constraints,
rather than being unnecessarily locked into fragile step-by-step
instructions.

---

## 10. Result Aggregation

Sub-agents perform their individual tasks and return their results
to the Coordinator.

The Coordinator then:

1. Collects the results
2. Evaluates them
3. Handles conflicts/errors
4. Synthesizes the final result

Sub-agents are not responsible for the overall final answer.

The Coordinator owns the final aggregation.

---

## 11. Error Handling

A sub-agent can fail.

The Coordinator must be able to understand what happened and
decide what to do next.

Avoid vague errors such as:

    "Operation failed"

Prefer structured error information such as:

    error_category: timeout
    retryable: true
    attempted_query: "Q3 revenue"
    partial_results: [...]
    alternatives: [...]

This gives the Coordinator enough information to make
a recovery decision.

---

## 12. Local Recovery Before Escalation

A sub-agent should try reasonable local recovery before
escalating the problem to the Coordinator.

Examples:

- Retry a transient timeout
- Adjust an invalid query
- Try an available backup source

Only after local recovery options are exhausted should the
sub-agent escalate to the Coordinator.

---

## 13. Communication Rule

### Correct

    Coordinator
       |
       +--> Sub-Agent A
       |
       +--> Sub-Agent B
       |
       +--> Sub-Agent C

All communication goes through the Coordinator.

### Anti-Pattern

    Sub-Agent A <----> Sub-Agent B

Direct inter-sub-agent communication creates unnecessary
dependencies and reduces observability.

---

## 14. Common Anti-Patterns

### Anti-Pattern 1 — Sequential Spawning

Bad:

    spawn A
      |
      v
    wait
      |
      v
    spawn B
      |
      v
    wait
      |
      v
    spawn C

If the tasks are independent, this unnecessarily increases latency.

Prefer parallel spawning.

---

### Anti-Pattern 2 — Missing Context Injection

Bad:

    Coordinator -> Sub-Agent

    "Create a report from previous findings."

The sub-agent has no knowledge of those findings unless
they are explicitly provided.

Fix:

    Coordinator
       |
       | structured context
       v
    Sub-Agent

---

### Anti-Pattern 3 — Direct Sub-Agent Communication

Do not allow sub-agents to directly depend on or communicate
with other sub-agents.

Use:

    Sub-Agent -> Coordinator -> Sub-Agent

instead.

---

### Anti-Pattern 4 — Overly Narrow Decomposition

If the Coordinator fails to assign an important topic to any
sub-agent, the final synthesis cannot magically recover it.

The decomposition must provide sufficient coverage of the problem.

---

## 15. Exam Cheat Sheet

Remember these facts:

- Coordinator = central decision maker
- Coordinator responsibilities = decomposition, delegation,
  aggregation, error handling
- Hub-and-spoke = Coordinator in the center
- Sub-agents are specialized
- All communication routes through Coordinator
- Sub-agents start with blank context
- Context must be explicitly injected
- Coordinator needs `task` to spawn sub-agents
- Sub-agents should not normally spawn more sub-agents
- Independent tasks → parallel execution
- Multiple parallel sub-agents → multiple task calls in one response
- Parallel latency ≈ maximum task duration
- Sequential latency ≈ sum of task durations
- Coordinator owns final synthesis
- Do not silently resolve source conflicts inside a sub-agent
- Prefer structured error information over generic errors
- Try local recovery before escalation
- Avoid over-orchestration

---

## 16. Practical Files

This folder contains the practical implementation for Episode 02:

- `coordinator.py` — Coordinator implementation
- `sub_agent.py` — Sub-agent implementation
- `agent.py` — Agent entry/example
- `tools.py` — Supporting tools
- `requirements.txt` — Dependencies
- `tests/` — Tests
- `README.md` — This guide

---

## Core Mental Model

Think of the system like this:

                    Coordinator
                   /     |      \
                  /      |       \
                 v       v        v
             Specialist Specialist Specialist
                 \       |        /
                  \      |       /
                   v     v      v
                    Coordinator
                         |
                         v
                    Final Answer

The Coordinator thinks about the whole problem.

The Sub-Agents think deeply about their assigned pieces.

The Coordinator brings everything back together.