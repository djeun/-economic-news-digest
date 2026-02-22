# Automated News Digest

An automation hub that collects RSS feeds and GitHub Trending data, summarizes them with Gemini AI, and delivers a daily Korean email briefing.
Uses **only free services** (Google Gemini, Gmail, GitHub Actions).

---

## Briefings

All 3 briefings are fetched and processed in parallel, then sent simultaneously at 08:00 PST every day.

| Job | Content |
|-----|---------|
| 🇺🇸 US Economic News | CNBC, MarketWatch, Google News |
| 💻 Global Tech News | Hacker News, TechCrunch, The Verge |
| 🐙 GitHub Trending | Today's trending repositories |

---

## How It Works

```
orchestrator.py
├── [parallel] US Economic News  → fetch → Gemini AI summarize
├── [parallel] Tech News         → fetch → Gemini AI summarize
└── [parallel] GitHub Trending   → scrape → Gemini AI summarize
         ↓ (all 3 ready)
├── [simultaneous] send email #1
├── [simultaneous] send email #2
└── [simultaneous] send email #3
```

A single GitHub Actions workflow (`daily_briefing.yml`) runs `orchestrator.py` daily.
If one job fails, the other two still send normally.

---

## Project Structure

```
.
├── orchestrator.py              # Runs all 3 jobs in parallel, sends emails simultaneously
├── jobs/                        # One folder per automation job
│   ├── us_economic_news/
│   │   └── main.py
│   ├── tech_news/
│   │   └── main.py
│   └── github_trending/
│       └── main.py
├── shared/                      # Reusable utilities
│   ├── ai_client.py             # Gemini API helper
│   ├── email_sender.py          # Gmail SMTP helper
│   └── rss_fetcher.py           # RSS parsing helper
├── .github/workflows/
│   └── daily_briefing.yml       # Single unified schedule (08:00 PST)
├── requirements.txt
└── .env.example
```

---

## Getting Started

### 1. Fork or clone the repo

```bash
git clone https://github.com/your-username/economic-news-digest.git
cd economic-news-digest
```

### 2. Register GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add the following:

| Secret | Description | Where to get it |
|--------|-------------|-----------------|
| `GEMINI_API_KEY` | Google AI API key | [Google AI Studio](https://aistudio.google.com/) |
| `GMAIL_USER` | Sender Gmail address | Gmail |
| `GMAIL_APP_PASSWORD` | Gmail App Password | Google Account → Security → App Passwords |
| `RECIPIENT_EMAIL` | Recipient email(s), comma-separated | — |

### 3. Enable workflows

The `daily_briefing.yml` workflow runs automatically once activated.
Use the **Run workflow** button in the Actions tab to test immediately.

---

## Local Testing

```bash
# Install dependencies
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Fill in your values, then:
set -a && source .env && set +a

# Run all 3 jobs together (same as production)
python orchestrator.py

# Or run individual jobs for debugging
python jobs/us_economic_news/main.py
python jobs/tech_news/main.py
python jobs/github_trending/main.py
```

---

## Tech Stack

- **Language**: Python 3.12
- **AI summarization**: Google Gemini 2.5 Flash (free · 250 req/day)
- **Email**: Gmail SMTP (free · 500/day)
- **Scheduling**: GitHub Actions (free · 2,000 min/month)
- **Libraries**: `feedparser`, `google-genai`, `requests`, `beautifulsoup4`
