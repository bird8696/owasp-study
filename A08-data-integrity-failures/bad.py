# ❌ BAD EXAMPLE — A08:2025 Data Integrity Failures
# 문제: 신뢰할 수 없는 데이터를 검증 없이 역직렬화
# 예시 1: pickle로 외부 데이터 역직렬화 → 임의 코드 실행
# 예시 2: 무결성 검증 없이 파일 사용
# 실행: python bad.py

import pickle
import json

# ❌ 문제 1: pickle 역직렬화 — 악성 데이터로 임의 코드 실행 가능
def load_user_data_bad(data: bytes) -> dict:
    return pickle.loads(data)  # ❌ 외부 입력을 pickle로 역직렬화

# 악성 pickle 페이로드 생성 (실제 공격 시연용)
class MaliciousPayload:
    def __reduce__(self):
        # __reduce__ 로 역직렬화 시점에 임의 코드 실행
        import os
        return (os.system, ("echo '공격자 코드 실행됨 — 실제라면 서버 장악'",))

# ❌ 문제 2: 파일 무결성 검증 없음
def load_config_bad(filepath: str) -> dict:
    with open(filepath) as f:
        return json.load(f)  # ❌ 파일이 변조됐는지 확인 안 함

# --- 시뮬레이션 ---
print("=" * 55)
print("❌ BAD: Data Integrity Failures")
print("=" * 55)

print("\n[정상 pickle 데이터]")
normal_data = pickle.dumps({"username": "alice", "role": "user"})
print(f"  결과: {load_user_data_bad(normal_data)}")

print("\n[악성 pickle 페이로드 역직렬화]")
malicious_data = pickle.dumps(MaliciousPayload())
print("  악성 데이터 역직렬화 실행:")
load_user_data_bad(malicious_data)
print("  → pickle.loads() 한 줄로 임의 코드 실행됨 ❌")

print("\n[무결성 검증 없는 파일 로드]")
print("  → 파일이 공격자에 의해 변조돼도 탐지 불가 ❌")