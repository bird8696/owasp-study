# ✅ GOOD EXAMPLE — A09:2025 Security Logging & Alerting Failures
# 수정: 보안 이벤트 로깅 + 민감 정보 제외 + 이상 탐지 알림
# 실행: python good.py

import logging
import time
from collections import defaultdict

# ✅ 로그 포맷: 시간 + 레벨 + 메시지
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("security")

USERS: dict[str, str] = {
    "alice": "password123",
    "admin": "supersecret",
}

# 실패 횟수 추적 (이상 탐지용)
fail_count: dict[str, int] = defaultdict(int)
ALERT_THRESHOLD = 3  # 3회 이상 실패 시 경보

def login_good(username: str, password: str, ip: str = "127.0.0.1") -> bool:
    if USERS.get(username) == password:
        fail_count[username] = 0  # 성공 시 초기화

        # ✅ 성공 로그: 비밀번호 절대 포함 안 함
        logger.info(f"LOGIN_SUCCESS | user={username} ip={ip}")
        return True
    else:
        fail_count[username] += 1

        # ✅ 실패 로그: 비밀번호 절대 포함 안 함
        logger.warning(f"LOGIN_FAILED | user={username} ip={ip} attempts={fail_count[username]}")

        # ✅ 이상 탐지: 임계값 초과 시 경보
        if fail_count[username] >= ALERT_THRESHOLD:
            logger.critical(
                f"BRUTE_FORCE_DETECTED | user={username} ip={ip} "
                f"attempts={fail_count[username]} → 즉시 조치 필요"
            )
        return False

def access_sensitive_data(username: str, resource: str, ip: str = "127.0.0.1") -> None:
    # ✅ 민감 데이터 접근도 로깅
    logger.info(f"DATA_ACCESS | user={username} resource={resource} ip={ip}")

# --- 시뮬레이션 ---
print("=" * 55)
print("✅ GOOD: Security Logging & Alerting")
print("=" * 55)

print("\n[보안 이벤트 로그 — 브루트포스 탐지]")
attempts = ["1234", "0000", "admin", "qwerty", "password123"]
for pw in attempts:
    login_good("alice", pw, ip="192.168.1.100")

print("\n[민감 데이터 접근 로그]")
access_sensitive_data("alice", "/api/users/profile", ip="192.168.1.100")

print("\n[로그에서 확인 가능한 것들]")
print("  - 언제 / 누가 / 어디서 시도했는지 ✅")
print("  - 몇 번 실패했는지 ✅")
print("  - 브루트포스 탐지 및 경보 ✅")
print("  - 비밀번호는 로그에 없음 ✅")