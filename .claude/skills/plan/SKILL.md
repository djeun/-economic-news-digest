---
name: plan
description: PLAN.md에서 미완료 작업 목록을 보여줍니다.
disable-model-invocation: true
allowed-tools: Read
---

PLAN.md를 읽고 미완료 항목을 Phase별로 정리해서 보여주세요.

## 출력 형식

```
📋 남은 작업 목록

── Phase 1 — 프로젝트 기반 정비 ──
  [ ] 항목 A
  [ ] 항목 B

── Phase 2 — 자동화 job 추가 ──
  [ ] 항목 C

총 N개 남음
```

- `[x]` 완료 항목은 출력하지 않는다.
- 완료된 Phase는 "✅ Phase N 완료" 한 줄로만 표시한다.
- 마지막에 PROGRESS.md의 `진행 중` 섹션도 읽어서, 현재 누군가 작업 중인 항목이 있으면 함께 표시한다.
