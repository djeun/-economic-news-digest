---
name: test-job
description: 특정 job을 로컬에서 실행해서 테스트합니다.
disable-model-invocation: true
allowed-tools: Read, Bash, Glob
argument-hint: [job_name]
---

`$ARGUMENTS` job을 로컬에서 테스트하세요.

## 절차

### 1. 사전 확인

- `jobs/$ARGUMENTS/main.py` 파일이 존재하는지 확인한다.
- 없으면 사용 가능한 job 목록을 `jobs/` 폴더에서 찾아 보여준다.

### 2. 환경 확인

- `.env` 파일이 존재하는지 확인한다.
- 없으면 `.env.example`을 보여주며 `.env` 파일을 먼저 만들어야 한다고 안내한다.

### 3. 실행

아래 명령을 실행한다:

```bash
python jobs/$ARGUMENTS/main.py
```

환경변수는 `.env` 파일에서 읽는다:

```bash
set -a && source .env && set +a && python jobs/$ARGUMENTS/main.py
```

### 4. 결과 보고

- 성공 시: 출력 내용을 요약해서 보여준다.
- 실패 시: 에러 메시지를 분석하고 수정 방법을 제안한다.
  - 환경변수 누락 → `.env` 설정 안내
  - 모듈 없음 → `pip install -r requirements.txt` 안내
  - API 오류 → 해당 서비스 키 확인 안내
