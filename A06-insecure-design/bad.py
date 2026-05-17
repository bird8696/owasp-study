# ❌ BAD EXAMPLE — A06:2025 Insecure Design
# 문제: 설계 단계에서 보안을 고려하지 않음
# 예시: 로그인 시도 횟수 제한 없음 → 브루트포스 무한 가능
# 실행: python bad.py

import time

# 가상 DB
USERS: dict[str, str] = {
    "alice": "password123",
    "admin": "supersecret",
}

# ❌ 문제 1: 로그인 시도 횟수 제한 없음
# ❌ 문제 2: 계정 잠금 없음
# ❌ 문제 3: 실패 로그 없음
def login_bad(username: str, password: str) -> bool:
    return USERS.get(username) == password

# --- 시뮬레이션: 브루트포스 공격 ---
print("=" * 50)
print("❌ BAD: Insecure Design (No Rate Limiting)")
print("=" * 50)

# 공격자가 흔한 비밀번호 목록으로 무한 시도
wordlist = ["1234", "0000", "admin", "qwerty", "password123"]

print("\n[브루트포스 공격 시뮬레이션]")
print(f"대상 계정: alice")
print(f"시도 횟수 제한: 없음 ❌\n")

for attempt, pw in enumerate(wordlist, 1):
    result = login_bad("alice", pw)
    print(f"  시도 {attempt}: {pw!r} → {'성공 ❌' if result else '실패'}")
    if result:
        print(f"\n  → 비밀번호 발견: {pw!r}")
        print(f"  → 총 {attempt}번 만에 계정 탈취 완료 ❌")
        break