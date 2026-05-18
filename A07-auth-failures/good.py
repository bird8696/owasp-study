# ✅ GOOD EXAMPLE — A07:2025 Identification & Authentication Failures
# 수정: 암호학적 난수 토큰 + 세션 만료 + 로그아웃 시 즉시 무효화
# 실행: python good.py

import secrets
import time
from dataclasses import dataclass

@dataclass
class Session:
    username: str
    created_at: float
    expires_at: float

# 가상 세션 저장소
SESSIONS: dict[str, Session] = {}
SESSION_TTL = 10  # 10초 만료 (실제론 30분~1시간)

# ✅ 수정 1: 암호학적 난수로 토큰 생성 → 예측 불가
def generate_token_good() -> str:
    return secrets.token_urlsafe(32)  # ✅ 256비트 난수

# ✅ 수정 2: 로그인 시 기존 세션 무효화 + 만료 시간 설정
def login_good(username: str) -> str:
    # 기존 세션 무효화
    expired = [t for t, s in SESSIONS.items() if s.username == username]
    for t in expired:
        del SESSIONS[t]

    token = generate_token_good()
    now = time.time()
    SESSIONS[token] = Session(
        username=username,
        created_at=now,
        expires_at=now + SESSION_TTL  # ✅ 만료 시간 설정
    )
    return token

# ✅ 수정 3: 로그아웃 시 세션 즉시 삭제
def logout_good(token: str) -> None:
    SESSIONS.pop(token, None)  # ✅ 토큰 즉시 무효화

# ✅ 수정 4: 세션 조회 시 만료 여부 확인
def get_user_good(token: str) -> str | None:
    session = SESSIONS.get(token)
    if not session:
        return None
    if time.time() > session.expires_at:
        del SESSIONS[token]  # ✅ 만료된 세션 자동 삭제
        print(f"  → 세션 만료됨, 자동 삭제 ✅")
        return None
    return session.username

# --- 시뮬레이션 ---
print("=" * 50)
print("✅ GOOD: Secure Authentication")
print("=" * 50)

print("\n[예측 불가능한 세션 토큰]")
token1 = login_good("alice")
token2 = login_good("bob")
token3 = login_good("admin")
print(f"  alice 토큰: {token1}")
print(f"  bob 토큰:   {token2}")
print(f"  admin 토큰: {token3}")
print(f"  → 완전한 난수, 패턴 없음 ✅")

print("\n[로그아웃 후 세션 무효화]")
print(f"  로그아웃 전 alice 조회: {get_user_good(token1)}")
logout_good(token1)
print(f"  로그아웃 후 alice 조회: {get_user_good(token1)}")
print(f"  → None 반환, 토큰 즉시 무효화 ✅")

print(f"\n[세션 만료 확인] — {SESSION_TTL}초 후 자동 만료")
token4 = login_good("carol")
print(f"  만료 전 조회: {get_user_good(token4)}")
time.sleep(SESSION_TTL + 1)
print(f"  만료 후 조회: {get_user_good(token4)}")