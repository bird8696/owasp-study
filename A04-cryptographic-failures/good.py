# ✅ GOOD EXAMPLE — A04:2025 Cryptographic Failures
# 수정: bcrypt으로 안전한 비밀번호 해싱
# 실행: python good.py
# 설치: pip install bcrypt

import bcrypt
import hashlib
import secrets

# 가상 DB
USER_DB: dict[str, bytes] = {}

# ✅ bcrypt 사용 — salt 자동 생성 + 느린 해시 (브루트포스 방어)
def register(username: str, password: str) -> None:
    # bcrypt는 내부적으로 salt를 자동 생성해서 붙여줌
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
    USER_DB[username] = hashed  # ✅ 안전한 해시값 저장

def login(username: str, password: str) -> bool:
    stored_hash = USER_DB.get(username)
    if not stored_hash:
        return False
    # ✅ 타이밍 공격 방지: 상수 시간 비교
    return bcrypt.checkpw(password.encode(), stored_hash)

# ✅ 보너스: 안전한 토큰 생성 (세션, API 키 등)
def generate_token() -> str:
    return secrets.token_urlsafe(32)  # ✅ 암호학적으로 안전한 난수

# --- 시뮬레이션 ---
print("=" * 50)
print("✅ GOOD: Safe Cryptographic Practices")
print("=" * 50)

password = "mypassword123"
print(f"\n원본 비밀번호: {password}")

register("alice", password)
print(f"\n[bcrypt 해싱]")
print(f"DB 저장값: {USER_DB['alice']}")
print("→ 매번 다른 salt → 같은 비밀번호도 해시값이 달라짐 ✅")
print("→ 역추적 사실상 불가능 ✅")

print(f"\n[로그인 검증]")
print(f"올바른 비밀번호: {login('alice', 'mypassword123')}")   # True
print(f"틀린 비밀번호:   {login('alice', 'wrongpassword')}")   # False

print(f"\n[같은 비밀번호 두 번 해싱 — salt 덕분에 다른 결과]")
hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
hash2 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
print(f"hash1: {hash1}")
print(f"hash2: {hash2}")
print(f"둘이 같냐: {hash1 == hash2}")  # False — 레인보우 테이블 무력화

print(f"\n[안전한 토큰 생성]")
print(f"토큰: {generate_token()}")