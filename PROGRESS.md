# PROGRESS.md — 진행 상황

에이전트가 작업을 시작·완료할 때 이 파일을 업데이트한다.

---

## 진행 중

_현재 진행 중인 작업 없음_

<!-- 작업을 시작하면 아래 형식으로 추가:
- [ ] {작업 내용} — {에이전트 또는 세션 식별자}, 시작: {날짜}
-->

---

## 완료

- [x] 미국 경제 뉴스 브리핑 `main.py` 작성
  - RSS 피드 3개 (CNBC, MarketWatch, Google News) 수집
  - Gemini 1.5 Flash로 한국어 요약
  - Gmail SMTP 이메일 발송
- [x] GitHub Actions 워크플로 작성 (매일 08:00 KST)
- [x] CLAUDE.md 작성 — 프로젝트 규칙, 무료 서비스 목록, 코드 패턴
- [x] PLAN.md / PROGRESS.md 도입
- [x] 폴더 구조 리팩터링
  - `main.py` → `jobs/us_economic_news/main.py`
  - `daily_news.yml` → `.github/workflows/us_economic_news.yml`
  - `shared/rss_fetcher.py`, `shared/ai_client.py`, `shared/email_sender.py` 분리
- [x] 글로벌 테크 뉴스 브리핑 (`jobs/tech_news/main.py`)
  - RSS 피드 3개 (Hacker News, TechCrunch, The Verge) 수집
  - Gemini 2.5 Flash로 한국어 요약 (개발자 포인트 섹션 포함)
  - GitHub Actions 워크플로 작성 (`tech_news.yml`, 매일 08:00 KST)

---

## 대기 중 (다음 작업)

PLAN.md Phase 1 남은 항목:

1. **`requirements.txt` 최종 정리** — 현재 패키지 버전 고정

이후 Phase 2 (새 job 추가):
- GitHub 트렌딩

---

## 블로커 / 이슈

_현재 없음_

---

## 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-02-21 | 프로젝트 초기 셋업. main.py, GitHub Actions, CLAUDE.md 완성 |
| 2026-02-21 | PLAN.md / PROGRESS.md 도입 |
| 2026-02-21 | 폴더 구조 리팩터링 완료. shared/ 분리, jobs/ 구조 적용 |
| 2026-02-21 | 글로벌 테크 뉴스 브리핑 완료. jobs/tech_news/main.py + tech_news.yml 작성 |
