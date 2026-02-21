---
name: lookup
description: 지식 베이스에서 키워드로 관련 정보를 검색합니다.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep
argument-hint: [키워드]
---

`.claude/knowledge/` 지식 베이스에서 `$ARGUMENTS`와 관련된 정보를 찾아주세요.

## 검색 절차

1. `.claude/knowledge/INDEX.md`의 태그 인덱스에서 `$ARGUMENTS`와 관련된 파일을 먼저 확인한다.
2. 관련 파일들을 읽어 `$ARGUMENTS`가 포함된 행·섹션을 찾는다.
3. 매칭되는 내용이 없으면 모든 knowledge 파일을 전체 검색한다.

## 출력 형식

```
🔍 검색어: {키워드}

📂 {파일명}
  {관련 내용 발췌 — 표 행, 코드 블록, 설명 등}

📂 {파일명}
  {관련 내용 발췌}

---
총 {N}건 발견 | 더 추가하려면 /save-research 사용
```

- 발견된 내용이 없으면 "지식 베이스에 없음 — researcher 에이전트로 조사 후 /save-research로 저장하세요" 안내.
- 표 데이터는 그대로 출력하고, 코드 블록도 포함한다.
