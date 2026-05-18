# ❌ BAD EXAMPLE — A07:2025 Identification & Authentication Failures
# 문제: 예측 가능한 세션 토큰 + 로그아웃 후에도 세션 유효
# 실행: python bad.py

import time

# 가상 세션 저장소
SESSIONS: dict[str, str] = {}
counter = 0

# ❌ 문제 1: 순차적 숫자로 세션 ID 생성 → 예측 가능
def generate_token_bad() -> str:
    global counter
    counter += 1
    return f"session_{counter}"  # ❌ session_1, session_2... 순서 뻔함

# ❌ 문제 2: 로그인 시 기존 세션 무효화 안 함
def login_bad(username: str) -> str:
    token = generate_token_bad()
    SESSIONS[token] = username  # ❌ 이전 세션 그대로 살아있음
    return token

# ❌ 문제 3: 로그아웃해도 세션 안 지움
def logout_bad(token: str) -> None:
    pass  # ❌ 아무것도 안 함 → 토큰 재사용 가능

def get_user_bad(token: str) -> str | None:
    return SESSIONS.get(token)

# --- 시뮬레이션 ---
print("=" * 50)
print("❌ BAD: Authentication Failures")
print("=" * 50)

print("\n[예측 가능한 세션 토큰]")
token1 = login_bad("alice")
token2 = login_bad("bob")
token3 = login_bad("admin")
print(f"  alice 토큰: {token1}")
print(f"  bob 토큰:   {token2}")
print(f"  admin 토큰: {token3}")
print(f"  → 패턴이 뻔함 → 공격자가 session_4, session_5 추측 가능 ❌")

print("\n[로그아웃 후 세션 재사용]")
print(f"  로그아웃 전 alice 조회: {get_user_bad(token1)}")
logout_bad(token1)
print(f"  로그아웃 후 alice 조회: {get_user_bad(token1)}")
print(f"  → 로그아웃해도 토큰이 여전히 유효 ❌")