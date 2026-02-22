# 자동화 허브 (Automation Hub)

이 프로젝트는 반복적인 정보 수집·요약·알림 작업을 자동화하는 허브입니다.
GitHub Actions로 스케줄을 관리하고, 무료 서비스만 사용합니다.

---

## 에이전트 협업 규칙

여러 에이전트가 작업을 나눠 진행할 때 아래 두 파일로 상태를 관리한다.

### PLAN.md — 무엇을 해야 하는가

- 전체 작업을 Phase별로 정리한 목록
- `[ ]` = 미완료, `[x]` = 완료
- 에이전트는 **작업 시작 전** 반드시 읽는다
- 작업 완료 후 해당 항목을 `[x]`로 변경한다

### PROGRESS.md — 지금 어디까지 됐는가

- **진행 중**: 현재 어떤 에이전트가 무엇을 하고 있는지
- **완료**: 끝난 작업 목록
- **대기 중**: 다음으로 할 작업
- **블로커**: 막힌 이슈

### 작업 시작 시 순서

1. `PLAN.md` 읽기 → 맡을 `[ ]` 항목 선택
2. `PROGRESS.md`의 `진행 중` 섹션에 추가
3. 작업 수행
4. `PLAN.md`의 `[ ]` → `[x]` 변경
5. `PROGRESS.md` 업데이트 (진행 중 → 완료)

---

## 핵심 원칙: 완전 무료

**아무리 소액이라도 유료 서비스는 사용하지 않습니다.**
새 자동화를 추가할 때 반드시 아래 승인 목록에서만 선택하세요.

### 승인된 무료 서비스 목록

| 역할 | 서비스 | 제한 |
|------|--------|------|
| AI 요약·생성 | Google Gemini 2.5 Flash | 250건/일, 10건/분 |
| 뉴스·데이터 수집 | RSS 피드 (CNBC, MarketWatch, Google News 등) | 제한 없음 |
| 이메일 발송 | Gmail SMTP (앱 비밀번호) | 하루 500건 |
| 스케줄 실행 | GitHub Actions | 월 2,000분 (private repo) |
| 코드 저장 | GitHub | 무료 |

### 사용 금지 서비스 (유료)

- Anthropic / Claude API
- OpenAI API
- NewsAPI.org (무료 플랜도 상업적 제한 있음)
- SendGrid, Mailgun 등 유료 이메일 서비스
- AWS, GCP, Azure 유료 기능

---

## 프로젝트 구조

```
.
├── CLAUDE.md                        # 이 파일
├── requirements.txt                 # 전체 공통 의존성
├── .env.example                     # 환경변수 템플릿
├── .gitignore
│
├── jobs/                            # 자동화 작업별 폴더
│   └── us_economic_news/
│       └── main.py                  # 미국 경제 뉴스 브리핑
│
├── shared/                          # 재사용 유틸리티
│   ├── email_sender.py              # Gmail SMTP 발송 헬퍼
│   ├── ai_client.py                 # Gemini API 헬퍼
│   └── rss_fetcher.py               # RSS 파싱 헬퍼
│
└── .github/
    └── workflows/                   # 각 job의 실행 스케줄
        └── us_economic_news.yml
```

> **현재 상태**: `jobs/`와 `shared/` 폴더는 리팩터링 예정.
> 지금은 `main.py`가 루트에 있음.

---

## 새 자동화 추가 방법

1개의 자동화 = 1개의 job 폴더 + 1개의 workflow 파일.

### 1단계 — job 폴더 생성

```
jobs/{job_name}/
└── main.py
```

`main.py` 필수 구조:

```python
import os
# 환경변수는 항상 os.environ으로만 읽기 (하드코딩 금지)

def fetch_data() -> list:
    """데이터 수집 단계"""
    ...

def process(data: list) -> str:
    """AI 처리 또는 가공 단계"""
    ...

def notify(content: str) -> None:
    """알림 발송 단계 (이메일 등)"""
    ...

def main():
    data = fetch_data()
    content = process(data)
    notify(content)

if __name__ == "__main__":
    main()
```

### 2단계 — workflow 파일 생성

`.github/workflows/{job_name}.yml` 템플릿:

```yaml
name: {작업 이름}

on:
  schedule:
    - cron: "0 23 * * *"   # 매일 08:00 KST
  workflow_dispatch:         # 수동 실행 허용

jobs:
  run:
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
          # job 전용 환경변수 추가 가능
```

### 3단계 — GitHub Secrets 등록

**Settings → Secrets and variables → Actions**에 등록.
공통 Secret은 이미 있으면 재사용, job 전용 값만 추가.

---

## 환경변수 규칙

| 변수명 | 설명 | 공통 여부 |
|--------|------|-----------|
| `GEMINI_API_KEY` | Google AI Studio API 키 | 공통 |
| `GMAIL_USER` | 발송자 Gmail 주소 | 공통 |
| `GMAIL_APP_PASSWORD` | Gmail 앱 비밀번호 | 공통 |
| `RECIPIENT_EMAIL` | 수신자 이메일 | 공통 |

- 새 job에 필요한 변수는 `{JOB_NAME}_{변수명}` 형식으로 추가 (예: `WEATHER_CITY`)
- `.env.example`에 반드시 추가 (값 없이 키만)
- `.env` 파일은 `.gitignore`에 포함 — 절대 커밋하지 않음

---

## 기술 스택

- **언어**: Python 3.12
- **AI**: `google-generativeai` (Gemini 2.5 Flash)
- **RSS 파싱**: `feedparser`
- **이메일**: `smtplib` (표준 라이브러리)
- **HTTP**: `requests`
- **스케줄**: GitHub Actions cron

---

## Gemini API 사용 패턴

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(prompt)
text = response.text
```

- 모델은 항상 `gemini-2.5-flash` 사용 (무료 티어 한도 내)
- 프롬프트는 한국어로 작성, 출력도 한국어 요청
- 하루 작업당 Gemini 호출은 1~2회로 유지

---

## 이메일 발송 패턴

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

## 로컬 테스트 방법

```bash
# 1. 가상환경 생성 및 의존성 설치
python -m venv .venv
source .venv/Scripts/activate   # Windows
pip install -r requirements.txt

# 2. 환경변수 설정 (.env 파일 직접 작성 후)
set -a && source .env && set +a  # bash
# 또는 PowerShell:
# Get-Content .env | ForEach-Object { $k,$v = $_ -split '=',2; [System.Environment]::SetEnvironmentVariable($k,$v) }

# 3. 실행
python main.py                  # 현재 루트 job
python jobs/{job_name}/main.py  # 특정 job
```

GitHub Actions에서 수동 실행하려면:
**Actions 탭 → 워크플로 선택 → Run workflow**

---

## 자동화 아이디어 목록

추후 추가 가능한 자동화 예시:

- [ ] 환율 일일 브리핑 (원/달러, 원/엔)
- [ ] 주요 주식 시황 요약
- [ ] 날씨 주간 예보
- [ ] 특정 키워드 뉴스 모니터링
- [ ] 유튜브 채널 새 영상 알림
- [ ] GitHub 스타 트렌딩 레포 요약
