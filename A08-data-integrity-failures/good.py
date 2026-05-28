# ✅ GOOD EXAMPLE — A08:2025 Data Integrity Failures
# 수정: pickle 대신 JSON + 파일 무결성 검증 (HMAC)
# 실행: python good.py

import json
import hmac
import hashlib
import os

SECRET_KEY = os.environ.get("APP_SECRET", "dev-secret-change-in-prod")

# ✅ 수정 1: pickle 대신 JSON 사용
# JSON은 코드 실행 기능 자체가 없음
def load_user_data_good(data: str) -> dict:
    parsed = json.loads(data)  # ✅ JSON은 역직렬화로 코드 실행 불가

    # ✅ 수정 2: 스키마 검증 — 필요한 필드만 허용
    allowed_keys = {"username", "role"}
    if not isinstance(parsed, dict) or not parsed.keys() <= allowed_keys:
        raise ValueError(f"허용되지 않은 데이터 구조: {parsed.keys()}")

    return parsed

# ✅ 수정 3: HMAC으로 파일 무결성 서명 + 검증
def sign_config(data: str) -> str:
    """데이터에 HMAC 서명 생성"""
    return hmac.new(
        SECRET_KEY.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()

def verify_and_load_config(data: str, signature: str) -> dict:
    """서명 검증 후 데이터 로드"""
    expected = sign_config(data)

    # ✅ 타이밍 공격 방지: hmac.compare_digest 사용
    if not hmac.compare_digest(expected, signature):
        raise ValueError("무결성 검증 실패 — 데이터 변조 감지 ✅")

    return json.loads(data)

# --- 시뮬레이션 ---
print("=" * 55)
print("✅ GOOD: Data Integrity Protection")
print("=" * 55)

print("\n[JSON 역직렬화 — 코드 실행 불가]")
normal_data = '{"username": "alice", "role": "user"}'
print(f"  결과: {load_user_data_good(normal_data)} ✅")

print("\n[허용되지 않은 필드 차단]")
try:
    suspicious = '{"username": "alice", "role": "admin", "inject": "malicious"}'
    load_user_data_good(suspicious)
except ValueError as e:
    print(f"  → 차단됨: {e} ✅")

print("\n[HMAC 무결성 검증]")
config = '{"db_host": "localhost", "port": 5432}'
sig = sign_config(config)
print(f"  원본 서명: {sig[:32]}...")

print("\n  정상 데이터 검증:")
result = verify_and_load_config(config, sig)
print(f"  → {result} ✅")

print("\n  변조된 데이터 검증:")
tampered = '{"db_host": "attacker.com", "port": 5432}'
try:
    verify_and_load_config(tampered, sig)
except ValueError as e:
    print(f"  → {e} ✅")