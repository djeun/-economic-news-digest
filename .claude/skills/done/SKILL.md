---
name: done
description: 완료한 작업을 PLAN.md와 PROGRESS.md에 반영합니다.
disable-model-invocation: true
allowed-tools: Read, Edit
argument-hint: [작업 내용 또는 키워드]
---

`$ARGUMENTS`에 해당하는 작업을 완료 처리하세요.

## 절차

### 1. PLAN.md 업데이트

PLAN.md를 읽고 `$ARGUMENTS`와 가장 일치하는 `[ ]` 항목을 찾아 `[x]`로 변경한다.
- 여러 항목이 매칭되면 사용자에게 어떤 항목인지 확인한다.
- 매칭되는 항목이 없으면 사용자에게 알린다.

### 2. PROGRESS.md 업데이트

PROGRESS.md를 다음과 같이 수정한다:
- `진행 중` 섹션에 해당 항목이 있으면 제거한다.
- `완료` 섹션에 추가한다:

```
- [x] {작업 내용}
```

- `변경 이력` 테이블에 오늘 날짜와 완료 내용을 추가한다.

### 3. 완료 후 안내

변경된 내용을 요약해서 보여주고, PLAN.md에 남은 작업 수를 알려준다.
