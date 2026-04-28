# Agent Inc

**Autonomous multi-agent OS** — a personal AI operating system where specialized agents execute tasks on your behalf, powered by the Anthropic API with persistent Supabase memory.

> Built solo. FastAPI · Python · Supabase · Anthropic API · WebSocket

---

## What It Does

Agent Inc is an autonomous task execution OS. You define what each agent does. Agents run with their own memory, context, and purpose — executing tasks asynchronously through a chat interface while you focus on other things.

---

## Agents

Agents are fully customizable. Each one is built on a shared BaseAgent class and given a system prompt that defines its role. Out of the box, the system ships with several pre-configured agents, but you can add unlimited agents for any purpose without touching core infrastructure.

---

## Features

- **Multi-Agent Architecture** — BaseAgent class with extensible per-agent system prompts, MeetingOrchestrator for task handoffs, fully asynchronous execution
- **Persistent Memory** — Supabase-backed memory per agent, context survives sessions, scoped so agents stay independent
- **Smart Routing** — provider_factory.py routes to optimal LLM (Anthropic or local Ollama), toggle per conversation
- **Real-Time UI** — Custom HTML/CSS/JS control panel with live task status, agent health, and chat interface per agent
- **File Drop Input** — Drop a file on any agent and it auto-processes

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · FastAPI · Uvicorn |
| Memory | Supabase (PostgreSQL) |
| LLM | Anthropic API · claude-sonnet-4-6 |
| Local LLM | Ollama · llama3 |
| Frontend | Vanilla HTML/CSS/JS |
| Architecture | REST + WebSocket · modular agent classes |

---

## Getting Started

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Set LLM_PROVIDER and ANTHROPIC_API_KEY in .env
uvicorn main:app --reload
open Agent.html
```

---

## Roadmap

- [x] Modular multi-agent architecture
- [x] Supabase persistent memory
- [x] FastAPI backend with REST routes
- [x] Smart LLM routing (Anthropic / Ollama)
- [x] File-drop agent input
- [ ] MeetingOrchestrator multi-agent coordination
- [ ] Agent-to-agent task delegation
- [ ] Voice input support

---

## License

MIT License © 2026 Elijah Ortiz
