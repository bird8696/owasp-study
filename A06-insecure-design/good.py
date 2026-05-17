# ✅ GOOD EXAMPLE — A06:2025 Insecure Design
# 수정: 설계 단계부터 보안 고려
# 예시: 로그인 시도 횟수 제한 + 계정 잠금 + 실패 로깅
# 실행: python good.py

import time
from collections import defaultdict
from dataclasses import dataclass, field

# 가상 DB
USERS: dict[str, str] = {
    "alice": "password123",
    "admin": "supersecret",
}

@dataclass
class LoginGuard:
    max_attempts: int = 3          # 최대 시도 횟수
    lockout_seconds: int = 30      # 잠금 시간 (초)
    attempts: dict = field(default_factory=lambda: defaultdict(int))
    locked_until: dict = field(default_factory=dict)
    fail_log: list = field(default_factory=list)

    def is_locked(self, username: str) -> bool:
        until = self.locked_until.get(username)
        if until and time.time() < until:
            remaining = int(until - time.time())
            print(f"  → 계정 잠금 중 ({remaining}초 남음) ✅")
            return True
        return False

    def record_fail(self, username: str) -> None:
        self.attempts[username] += 1
        self.fail_log.append(f"[{time.strftime('%H:%M:%S')}] 실패: {username} ({self.attempts[username]}번째)")

        # ✅ 최대 시도 초과 시 계정 잠금
        if self.attempts[username] >= self.max_attempts:
            self.locked_until[username] = time.time() + self.lockout_seconds
            print(f"  → {self.max_attempts}회 초과 — 계정 {self.lockout_seconds}초 잠금 ✅")

    def record_success(self, username: str) -> None:
        self.attempts[username] = 0
        self.locked_until.pop(username, None)

# ✅ 시도 횟수 제한 + 잠금 적용된 로그인
guard = LoginGuard()

def login_good(username: str, password: str) -> bool:
    # ✅ 잠금 확인
    if guard.is_locked(username):
        return False

    if USERS.get(username) == password:
        guard.record_success(username)
        return True
    else:
        guard.record_fail(username)
        return False

# --- 시뮬레이션 ---
print("=" * 50)
print("✅ GOOD: Secure Design (Rate Limiting)")
print("=" * 50)

wordlist = ["1234", "0000", "admin", "qwerty", "password123"]

print("\n[브루트포스 공격 시도]")
print(f"대상 계정: alice")
print(f"시도 횟수 제한: {guard.max_attempts}회 ✅\n")

for attempt, pw in enumerate(wordlist, 1):
    result = login_good("alice", pw)
    print(f"  시도 {attempt}: {pw!r} → {'성공' if result else '실패'}")
    if result:
        break

print(f"\n[실패 로그]")
for log in guard.fail_log:
    print(f"  {log}")