# 자동화 뉴스 다이제스트

RSS 피드와 GitHub Trending을 수집해 Gemini AI로 한국어 요약 이메일을 발송하는 자동화 허브입니다.
**완전 무료** 서비스만 사용합니다 (Google Gemini, Gmail, GitHub Actions).

---

## 브리핑 종류

| Job | 내용 | 발송 시각 |
|-----|------|-----------|
| 🇺🇸 미국 경제 뉴스 | CNBC, MarketWatch, Google News 요약 | 매일 08:00 PST |
| 💻 글로벌 테크 뉴스 | Hacker News, TechCrunch, The Verge 요약 | 매일 08:00 PST |
| 🐙 GitHub 트렌딩 | 오늘의 트렌딩 레포지터리 분석 | 매일 08:00 PST |

---

## 프로젝트 구조

```
.
├── jobs/                        # 자동화 job별 폴더
│   ├── us_economic_news/
│   │   └── main.py
│   ├── tech_news/
│   │   └── main.py
│   └── github_trending/
│       └── main.py
├── shared/                      # 공통 유틸리티
│   ├── ai_client.py             # Gemini API 헬퍼
│   ├── email_sender.py          # Gmail SMTP 헬퍼
│   └── rss_fetcher.py           # RSS 파싱 헬퍼
├── .github/workflows/           # GitHub Actions 스케줄
│   ├── us_economic_news.yml
│   ├── tech_news.yml
│   └── github_trending.yml
├── requirements.txt
└── .env.example
```

---

## 시작하기

### 1. 레포 포크 또는 클론

```bash
git clone https://github.com/your-username/economic-news-digest.git
cd economic-news-digest
```

### 2. GitHub Secrets 등록

**Settings → Secrets and variables → Actions**에서 아래 4개를 등록합니다.

| Secret 이름 | 설명 | 발급처 |
|-------------|------|--------|
| `GEMINI_API_KEY` | Google AI API 키 | [Google AI Studio](https://aistudio.google.com/) |
| `GMAIL_USER` | 발송자 Gmail 주소 | Gmail |
| `GMAIL_APP_PASSWORD` | Gmail 앱 비밀번호 | Google 계정 → 보안 → 앱 비밀번호 |
| `RECIPIENT_EMAIL` | 수신자 이메일 (쉼표로 여러 명 가능) | - |

### 3. 워크플로 활성화

GitHub Actions 탭에서 각 워크플로를 활성화하면 매일 자동 실행됩니다.
**Run workflow** 버튼으로 즉시 테스트할 수 있습니다.

---

## 로컬 테스트

```bash
# 의존성 설치
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어 실제 값 입력 후:
set -a && source .env && set +a

# 실행
python jobs/us_economic_news/main.py
python jobs/tech_news/main.py
python jobs/github_trending/main.py
```

---

## 기술 스택

- **언어**: Python 3.12
- **AI 요약**: Google Gemini 2.5 Flash (무료 · 250건/일)
- **이메일**: Gmail SMTP (무료 · 500건/일)
- **스케줄**: GitHub Actions (무료 · 월 2,000분)
- **주요 라이브러리**: `feedparser`, `google-genai`, `requests`, `beautifulsoup4`
