#!/usr/bin/env python3
"""
PreToolUse Hook — 유료 서비스 패키지 설치 차단
Bash 명령 실행 전 유료 서비스 관련 pip install을 감지하면 차단합니다.
"""
import json
import sys

BLOCKED = [
    "anthropic",
    "openai",
    "cohere",
    "replicate",
    "sendgrid",
    "mailgun",
    "boto3",      # AWS
    "azure",
    "pinecone",
]

def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")

    for pkg in BLOCKED:
        if f"pip install {pkg}" in command or f"pip install {pkg}" in command.lower():
            msg = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": (
                        f"🚫 유료 서비스 차단: '{pkg}'는 사용 금지입니다.\n"
                        f"CLAUDE.md의 '승인된 무료 서비스 목록'을 확인하세요.\n"
                        f"AI 요약은 google-generativeai(Gemini)를 사용해야 합니다."
                    )
                }
            }
            print(json.dumps(msg, ensure_ascii=False))
            sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
