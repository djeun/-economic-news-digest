# 무료 API 지식 베이스

검증된 완전 무료 API 목록입니다.
"무료 플랜 있음"과 "완전 무료"를 구분합니다. 카드 등록 필요 시 ⚠️ 표시.

---

## AI / 언어 모델

| 이름 | 엔드포인트 | 무료 한도 | API 키 | 검증 | 추가일 | 비고 |
|------|-----------|----------|--------|------|--------|------|
| Google Gemini 1.5 Flash | `generativelanguage.googleapis.com` | 1,500건/일, 15건/분 | 필요 (무료 발급) | ✅ | 2026-02-21 | Google AI Studio에서 발급 |

### Gemini API 키 발급

1. [aistudio.google.com](https://aistudio.google.com) 접속
2. Google 계정 로그인
3. "Get API key" → "Create API key" 클릭
4. 카드 등록 불필요

### Gemini 사용 예시

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("요약해줘: ...")
print(response.text)
```

---

## 환율 / 금융

| 이름 | 엔드포인트 | 무료 한도 | API 키 | 검증 | 추가일 | 비고 |
|------|-----------|----------|--------|------|--------|------|
| ExchangeRate-API (무료 플랜) | `https://open.er-api.com/v6/latest/USD` | 1,500건/월 | 불필요 ⭐ | ✅ | 2026-02-21 | 키 없이 USD 기준 즉시 사용 가능 |

### ExchangeRate-API 무료 사용 예시

```python
import requests

# API 키 없이 바로 사용
res = requests.get("https://open.er-api.com/v6/latest/USD")
data = res.json()
krw = data["rates"]["KRW"]   # 원/달러 환율
jpy = data["rates"]["JPY"]   # 엔/달러 환율
```

---

## 이메일 발송

| 이름 | 방식 | 무료 한도 | 설정 | 검증 | 추가일 |
|------|------|----------|------|------|--------|
| Gmail SMTP | SMTP SSL (포트 465) | 500건/일 | 앱 비밀번호 필요 | ✅ | 2026-02-21 |

### Gmail 앱 비밀번호 발급

1. Google 계정 → 보안 → 2단계 인증 활성화 (필수)
2. "앱 비밀번호" 검색 → 앱 선택: 메일 → 기기: Windows
3. 생성된 16자리를 `GMAIL_APP_PASSWORD` 환경변수에 저장
