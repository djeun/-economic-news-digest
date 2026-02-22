# Automated News Digest

An automation hub that collects RSS feeds and GitHub Trending data, summarizes them with Gemini AI, and delivers a daily Korean email briefing.
Uses **only free services** (Google Gemini, Gmail, GitHub Actions).

---

## Briefings

| Job | Content | Schedule |
|-----|---------|----------|
| 🇺🇸 US Economic News | CNBC, MarketWatch, Google News | Daily 08:00 PST |
| 💻 Global Tech News | Hacker News, TechCrunch, The Verge | Daily 08:00 PST |
| 🐙 GitHub Trending | Today's trending repositories | Daily 08:00 PST |

---

## Project Structure

```
.
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
├── .github/workflows/           # GitHub Actions schedules
│   ├── us_economic_news.yml
│   ├── tech_news.yml
│   └── github_trending.yml
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

Each workflow runs automatically once activated.
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

# Run
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
