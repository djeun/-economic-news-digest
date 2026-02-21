# PLAN.md — 전체 작업 계획

에이전트가 작업을 시작하기 전에 이 파일을 읽고,
완료된 항목은 PROGRESS.md에 기록한다.

---

## 목표

반복적인 정보 수집·요약·알림 작업을 자동화하는 허브 구축.
완전 무료 서비스만 사용. GitHub Actions로 스케줄 관리.

---

## Phase 1 — 프로젝트 기반 정비

- [x] 미국 경제 뉴스 브리핑 스크립트 작성 (`main.py`)
- [x] GitHub Actions 워크플로 작성 (`daily_news.yml`)
- [x] CLAUDE.md 작성 (프로젝트 규칙·패턴 문서화)
- [x] PLAN.md / PROGRESS.md 도입
- [x] 폴더 구조 리팩터링
  - `main.py` → `jobs/us_economic_news/main.py`
  - `daily_news.yml` → `.github/workflows/us_economic_news.yml`
  - `shared/` 폴더 생성 (공통 유틸리티)
- [x] `shared/email_sender.py` — Gmail SMTP 헬퍼 분리
- [x] `shared/ai_client.py` — Gemini API 헬퍼 분리
- [x] `shared/rss_fetcher.py` — RSS 파싱 헬퍼 분리
- [ ] `requirements.txt` 최종 정리

## Phase 2 — 자동화 job 추가

- [ ] 환율 브리핑 (`jobs/exchange_rate/`)
  - 원/달러, 원/엔, 원/유로 일일 환율 요약
  - 무료 소스: exchangerate-api.com (무료 티어) 또는 Yahoo Finance RSS
- [ ] 글로벌 테크 뉴스 브리핑 (`jobs/tech_news/`)
  - Hacker News Top Stories RSS 활용
- [ ] GitHub 트렌딩 레포 요약 (`jobs/github_trending/`)
  - GitHub Trending 페이지 스크래핑

## Phase 3 — 안정화

- [ ] 각 job별 에러 처리 강화 (뉴스 수집 실패 시 재시도)
- [ ] 이메일 발송 실패 시 로그 남기기
- [ ] README.md 작성 (외부 공개용 설명)

---

## 작업 규칙

- 한 에이전트는 한 번에 하나의 `[ ]` 항목만 담당한다.
- 작업 시작 전 PROGRESS.md의 `진행 중` 섹션에 자신이 맡은 항목을 기록한다.
- 작업 완료 후 이 파일의 `[ ]`를 `[x]`로 변경하고, PROGRESS.md를 업데이트한다.
