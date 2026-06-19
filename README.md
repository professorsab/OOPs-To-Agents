<!--
  Paste this as README.md in the OOPs-To-Agents repo (root level, next to requirements.txt).
  Fix every <!-- CONFIRM --> note before publishing — these are my best guesses from folder
  names and commit messages, not verified facts about your code.
-->

<h1 align="center">OOPs-To-Agents</h1>

<p align="center">
  <i>A staged progression from hand-rolled, OOP-based agents to full multi-agent frameworks.</i>
</p>

---

## What this is

A structured set of projects tracing one path through agent development: starting from
plain object-oriented agent design, then layering in increasingly capable frameworks —
CrewAI, LangChain, LangGraph — and finishing with a retrieval-augmented pipeline and an
applied demo.

<!-- CONFIRM: is there actually OOP-fundamentals code in here (e.g. inside Agents/), or
     was that the conceptual starting point with no surviving code? If the latter, say so
     explicitly rather than implying a folder that doesn't exist. -->

Each stage is kept as its own module so the jump between approaches — what a framework
buys you over a hand-rolled implementation, and where that trade-off stops paying off —
stays visible rather than getting flattened into one codebase.

## Structure

| Folder | Stage |
| --- | --- |
| `Agents/` | Framework-free agents built from base OOP principles — classes, inheritance, explicit state. <!-- CONFIRM --> |
| `Crew/` | Early CrewAI experiments. <!-- CONFIRM: how does this differ from CrewAi/ below — consider merging the two or renaming one for clarity --> |
| `CrewAi/` | CrewAI-based multi-agent task orchestration. |
| `Langchain/` | LangChain agents and chains. |
| `LangGraph/` | Stateful, graph-based agent workflows in LangGraph. |
| `RAG/` | Retrieval-augmented generation pipeline experiments. |
| `smart_energy_demo/` | Applied capstone — an ACP/MCP-based smart-home energy agent. <!-- CONFIRM: if this overlaps with your separate Smart-Home-Energy-Agent repo, link to it here and say which is canonical --> |

## Quickstart

```bash
git clone https://github.com/professorsab/OOPs-To-Agents.git
cd OOPs-To-Agents
pip install -r requirements.txt
```

Each folder is runnable independently — see the notes inside each one for specific
entry points. <!-- CONFIRM: add a one-line "run with: python ..." note inside each
folder's own README or top-of-file docstring, if you can spare 10 min per folder -->

## Status

Actively growing — each new folder represents a deliberate step up in framework
capability rather than a replacement of the previous one.

## License

MIT — see [LICENSE](LICENSE). <!-- CONFIRM: add a LICENSE file if you don't have one yet -->
