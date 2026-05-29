# ❌ BAD EXAMPLE — A09:2025 Security Logging & Alerting Failures
# 문제 1: 보안 이벤트 로그 없음 → 공격 탐지 불가
# 문제 2: 민감 정보를 로그에 그대로 기록
# 실행: python bad.py

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USERS: dict[str, str] = {
    "alice": "password123",
    "admin": "supersecret",
}

# ❌ 문제 1: 로그인 실패 이벤트를 아예 안 남김
# 브루트포스 공격이 와도 탐지 자체가 불가능
def login_bad(username: str, password: str) -> bool:
    if USERS.get(username) == password:
        return True
    return False  # ❌ 실패해도 아무 로그 없음

# ❌ 문제 2: 민감 정보를 로그에 그대로 기록
def login_bad_verbose(username: str, password: str) -> bool:
    # ❌ 비밀번호가 로그 파일에 평문으로 남음
    logger.info(f"로그인 시도: username={username}, password={password}")
    if USERS.get(username) == password:
        logger.info(f"로그인 성공: {username}, password={password}")
        return True
    logger.info(f"로그인 실패: {username}, password={password}")
    return False

# --- 시뮬레이션 ---
print("=" * 55)
print("❌ BAD: Security Logging Failures")
print("=" * 55)

print("\n[로그 없는 로그인 — 브루트포스 탐지 불가]")
attempts = ["1234", "0000", "password123"]
for pw in attempts:
    result = login_bad("alice", pw)
    print(f"  시도: {pw!r} → {'성공' if result else '실패'}")
print("  → 몇 번 시도했는지, 어디서 왔는지 기록 없음 ❌")

print("\n[민감 정보 로그 기록]")
login_bad_verbose("alice", "password123")
print("  → 비밀번호가 로그 파일에 평문으로 남음 ❌")
print("  → 로그 파일 털리면 비밀번호까지 노출 ❌")