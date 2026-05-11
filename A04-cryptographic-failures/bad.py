# ❌ BAD EXAMPLE — A04:2025 Cryptographic Failures
# 문제: 비밀번호를 평문/약한 해시로 저장
# 실행: python bad.py

import hashlib

# 가상 DB — 실제로는 이런 식으로 저장된 DB가 털리는 거야
USER_DB: dict[str, str] = {}

# ❌ 문제 1: 평문 저장
def register_plain(username: str, password: str) -> None:
    USER_DB[username] = password  # ❌ 비밀번호 그대로 저장

# ❌ 문제 2: MD5 해싱 — 레인보우 테이블로 1초 만에 역추적 가능
def register_md5(username: str, password: str) -> None:
    hashed = hashlib.md5(password.encode()).hexdigest()
    USER_DB[username] = hashed  # ❌ MD5는 해시가 아니라 그냥 인코딩 수준

# ❌ 문제 3: SHA1 — MD5보다 낫지만 여전히 패스워드 해싱엔 부적합
def register_sha1(username: str, password: str) -> None:
    hashed = hashlib.sha1(password.encode()).hexdigest()
    USER_DB[username] = hashed  # ❌ 빠른 해시 = 브루트포스에 취약

# --- 시뮬레이션 ---
print("=" * 50)
print("❌ BAD: Cryptographic Failures")
print("=" * 50)

password = "mypassword123"

print(f"\n원본 비밀번호: {password}")

register_plain("alice", password)
print(f"\n[평문 저장]")
print(f"DB 저장값: {USER_DB['alice']}")
print("→ DB 털리면 비밀번호 바로 노출 ❌")

register_md5("bob", password)
print(f"\n[MD5 해싱]")
print(f"DB 저장값: {USER_DB['bob']}")
print("→ https://crackstation.net 에서 바로 역추적 가능 ❌")

register_sha1("carol", password)
print(f"\n[SHA1 해싱]")
print(f"DB 저장값: {USER_DB['carol']}")
print("→ 레인보우 테이블 + GPU 브루트포스에 취약 ❌")