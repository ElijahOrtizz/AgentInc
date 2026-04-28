# Agent Inc

**Autonomous multi-agent OS** — a personal AI operating system where specialized agents handle trading analysis, job applications, homework, and research simultaneously, powered by the Anthropic API with persistent Supabase memory.

> Built solo. FastAPI · Python · Supabase · Anthropic API · WebSocket

---

## What It Does

Agent Inc is an autonomous task execution OS where each agent is a specialized AI with its own memory, context, and purpose. You dispatch tasks through a chat interface, and agents execute them asynchronously — analyzing trading signals, drafting job applications, completing research, or processing homework assignments — all running simultaneously.

---

## Agents

| Agent | Purpose |
|-------|---------|
| 🧠 **Stryde Agent** | BTC signal analysis, Kalshi odds, trading pipeline coordination |
| 💼 **Job Agent** | Cover letters, resume tailoring, LinkedIn outreach, application tracking |
| 📚 **Homework Agent** | Academic research, paper drafting, assignment review |
| 🔍 **Research Agent** | Deep web research, topic synthesis, fact verification |
| ⚙️ **Base Agent** | General-purpose tasks, file processing, automation |

---

## Features

- **Multi-Agent Architecture** — BaseAgent class with extensible per-agent system prompts, MeetingOrchestrator for task handoffs, asynchronous execution
- **Persistent Memory** — Supabase-backed memory per agent, context survives sessions, scoped so agents don't bleed into each other
- **Smart Routing** — provider_factory.py routes to optimal LLM (Anthropic or local Ollama), toggle per conversation
- **Real-Time UI** — Custom HTML/CSS/JS control panel with live task status, agent health, and chat interface per agent

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

- [x] BaseAgent, JobAgent, StrydeAgent, HomeworkAgent, ResearchAgent
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
