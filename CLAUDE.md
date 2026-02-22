# Automation Hub

This project automates repetitive information gathering, summarizing, and notification tasks.
Schedules are managed via GitHub Actions. Only free services are used.

---

## Agent Collaboration Rules

When multiple agents share work, use the following two files to track state.

### PLAN.md — What needs to be done

- Full task list organized by Phase
- `[ ]` = pending, `[x]` = complete
- Agents **must read this before starting** any task
- Mark items `[x]` after completion

### PROGRESS.md — Current status

- **In progress**: which agent is doing what
- **Completed**: finished tasks
- **Waiting**: next tasks in queue
- **Blockers**: issues blocking progress

### Workflow for starting a task

1. Read `PLAN.md` → pick an unchecked `[ ]` item
2. Add it to the `In Progress` section of `PROGRESS.md`
3. Do the work
4. Change `[ ]` → `[x]` in `PLAN.md`
5. Update `PROGRESS.md` (move from In Progress → Completed)

---

## Core Principle: Completely Free

**No paid services, no matter how cheap.**
When adding new automation, choose only from the approved list below.

### Approved Free Services

| Role | Service | Limit |
|------|---------|-------|
| AI summarization | Google Gemini 2.5 Flash | 250 req/day, 10 req/min |
| News & data | RSS feeds (CNBC, MarketWatch, Google News, etc.) | Unlimited |
| Email delivery | Gmail SMTP (App Password) | 500/day |
| Scheduling | GitHub Actions | 2,000 min/month (private repo) |
| Code hosting | GitHub | Free |

### Banned Services (Paid)

- Anthropic / Claude API
- OpenAI API
- NewsAPI.org (commercial restrictions even on free plan)
- SendGrid, Mailgun, or other paid email services
- AWS, GCP, Azure paid features

---

## Project Structure

```
.
├── CLAUDE.md                        # This file
├── requirements.txt                 # Shared dependencies
├── .env.example                     # Environment variable template
├── .gitignore
│
├── jobs/                            # One folder per automation job
│   ├── us_economic_news/
│   │   └── main.py                  # US economic news briefing
│   ├── tech_news/
│   │   └── main.py                  # Global tech news briefing
│   └── github_trending/
│       └── main.py                  # GitHub trending repos briefing
│
├── shared/                          # Reusable utilities
│   ├── email_sender.py              # Gmail SMTP helper
│   ├── ai_client.py                 # Gemini API helper
│   └── rss_fetcher.py               # RSS parsing helper
│
└── .github/
    └── workflows/                   # Cron schedules per job
        ├── us_economic_news.yml
        ├── tech_news.yml
        └── github_trending.yml
```

---

## Adding a New Automation

1 automation = 1 job folder + 1 workflow file.

### Step 1 — Create the job folder

```
jobs/{job_name}/
└── main.py
```

Required structure for `main.py`:

```python
import os
# Always read env vars via os.environ — never hardcode values

def fetch_data() -> list:
    """Data collection step."""
    ...

def process(data: list) -> str:
    """AI processing or transformation step."""
    ...

def notify(content: str) -> None:
    """Notification step (email, etc.)."""
    ...

def main():
    data = fetch_data()
    content = process(data)
    notify(content)

if __name__ == "__main__":
    main()
```

### Step 2 — Create the workflow file

Template for `.github/workflows/{job_name}.yml`:

```yaml
name: {Job Name}

on:
  schedule:
    - cron: "0 15 * * *"   # 08:00 PDT (UTC-7)
    - cron: "0 16 * * *"   # 08:00 PST (UTC-8)
  workflow_dispatch:

jobs:
  check-time:
    runs-on: ubuntu-latest
    outputs:
      should_run: ${{ steps.check.outputs.should_run }}
    steps:
      - name: Check current PT hour
        id: check
        run: |
          PT_HOUR=$(TZ="America/Los_Angeles" date +"%H")
          if [ "$PT_HOUR" = "08" ]; then
            echo "should_run=true" >> $GITHUB_OUTPUT
          else
            echo "should_run=false" >> $GITHUB_OUTPUT
          fi

  send-briefing:
    needs: check-time
    if: needs.check-time.outputs.should_run == 'true' || github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - run: pip install -r requirements.txt
      - run: python jobs/{job_name}/main.py
        env:
          GEMINI_API_KEY:     ${{ secrets.GEMINI_API_KEY }}
          GMAIL_USER:         ${{ secrets.GMAIL_USER }}
          GMAIL_APP_PASSWORD: ${{ secrets.GMAIL_APP_PASSWORD }}
          RECIPIENT_EMAIL:    ${{ secrets.RECIPIENT_EMAIL }}
```

### Step 3 — Register GitHub Secrets

Go to **Settings → Secrets and variables → Actions**.
Reuse existing shared secrets; only add job-specific values.

---

## Environment Variables

| Variable | Description | Shared |
|----------|-------------|--------|
| `GEMINI_API_KEY` | Google AI Studio API key | Yes |
| `GMAIL_USER` | Sender Gmail address | Yes |
| `GMAIL_APP_PASSWORD` | Gmail App Password | Yes |
| `RECIPIENT_EMAIL` | Recipient email(s) | Yes |

- Job-specific variables should follow the format `{JOB_NAME}_{VAR_NAME}` (e.g., `WEATHER_CITY`)
- Always add new variables to `.env.example` (key only, no value)
- `.env` is in `.gitignore` — never commit it

---

## Tech Stack

- **Language**: Python 3.12
- **AI**: `google-genai` (Gemini 2.5 Flash)
- **RSS parsing**: `feedparser`
- **Scraping**: `requests` + `beautifulsoup4`
- **Email**: `smtplib` (standard library)
- **Scheduling**: GitHub Actions cron

---

## Gemini API Pattern

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)
text = response.text
```

- Always use `gemini-2.5-flash` (within free tier limits)
- Write prompts in Korean; request Korean output
- Keep Gemini calls to 1–2 per job per day

---

## Email Pattern

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject: str, html_body: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = os.environ["GMAIL_USER"]
    msg["To"]      = os.environ["RECIPIENT_EMAIL"]
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.environ["GMAIL_USER"], os.environ["GMAIL_APP_PASSWORD"])
        server.sendmail(msg["From"], msg["To"], msg.as_string())
```

---

## Local Testing

```bash
# 1. Create virtualenv and install dependencies
python -m venv .venv
source .venv/Scripts/activate   # Windows
pip install -r requirements.txt

# 2. Set environment variables
cp .env.example .env
# Fill in your values, then:
set -a && source .env && set +a

# 3. Run
python jobs/us_economic_news/main.py
python jobs/tech_news/main.py
python jobs/github_trending/main.py
```

To trigger manually on GitHub Actions:
**Actions tab → select workflow → Run workflow**

---

## Automation Ideas

Future jobs to consider:

- [ ] Exchange rate briefing (KRW/USD, KRW/JPY)
- [ ] Stock market summary
- [ ] Weekly weather forecast
- [ ] Keyword news monitoring
- [ ] YouTube channel new video alerts
