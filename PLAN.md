# PLAN.md — Task Plan

Agents must read this file before starting work and mark completed items here.

---

## Goal

Build an automation hub for repetitive information gathering, summarizing, and alerting.
Use only completely free services. Manage schedules via GitHub Actions.

---

## Phase 1 — Project Foundation

- [x] Write US economic news briefing script (`main.py`)
- [x] Write GitHub Actions workflow (`daily_news.yml`)
- [x] Write CLAUDE.md (project rules and patterns)
- [x] Introduce PLAN.md / PROGRESS.md
- [x] Refactor folder structure
  - `main.py` → `jobs/us_economic_news/main.py`
  - `daily_news.yml` → `.github/workflows/us_economic_news.yml`
  - Create `shared/` folder for common utilities
- [x] `shared/email_sender.py` — extract Gmail SMTP helper
- [x] `shared/ai_client.py` — extract Gemini API helper
- [x] `shared/rss_fetcher.py` — extract RSS parsing helper
- [x] `requirements.txt` final cleanup

## Phase 2 — Add Automation Jobs

- [x] Global tech news briefing (`jobs/tech_news/`)
  - Hacker News, TechCrunch, The Verge RSS
- [x] GitHub trending repos summary (`jobs/github_trending/`)
  - Scrape GitHub Trending page

## Phase 3 — Stabilization

- [x] Strengthen error handling per job (retry on fetch failure)
- [x] Log email send failures
- [x] Write README.md (public-facing documentation)

## Phase 4 — Orchestration

- [x] Create `orchestrator.py` — runs all 3 jobs in parallel (fetch + AI summarize), sends all 3 emails simultaneously once every job is ready
- [x] Replace 3 separate workflows with single `daily_briefing.yml`
- [x] Remove `us_economic_news.yml`, `tech_news.yml`, `github_trending.yml`

---

## Work Rules

- One agent handles one `[ ]` item at a time.
- Before starting, add the item to the `In Progress` section of PROGRESS.md.
- After finishing, change `[ ]` to `[x]` here and update PROGRESS.md.
