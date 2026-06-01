# ❌ BAD EXAMPLE — A10:2025 System Integrity & Failure Handling
# 문제 1: 예외 발생 시 불안전한 상태로 진행 (권한 검증 건너뜀)
# 문제 2: 에러 메시지에 내부 정보 노출
# 문제 3: 부분 실패 후 롤백 없이 DB 불일치 상태 방치
# 실행: python bad.py

# 가상 DB
USERS: dict[int, dict] = {
    1: {"id": 1, "username": "alice", "balance": 1000, "role": "user"},
    2: {"id": 2, "username": "admin", "balance": 9999, "role": "admin"},
}

# ❌ 문제 1: 권한 검증 실패 시 예외를 잡아서 그냥 통과시킴
def get_admin_data_bad(user_id: int) -> dict:
    try:
        user = USERS[user_id]
        if user["role"] != "admin":
            raise PermissionError("관리자만 접근 가능")
        return {"secret": "관리자 전용 데이터"}
    except KeyError:
        # ❌ KeyError 잡으려다 PermissionError도 같이 통과됨
        pass
    except:
        # ❌ 모든 예외를 무시 → 권한 검증 건너뜀
        pass
    return {"secret": "관리자 전용 데이터"}  # ❌ 예외 무시 후 그냥 반환

# ❌ 문제 2: 송금 중 오류 발생 시 롤백 없음 → 잔액 불일치
def transfer_bad(from_id: int, to_id: int, amount: int) -> None:
    USERS[from_id]["balance"] -= amount  # 차감 완료
    # ❌ 여기서 오류 발생하면 차감만 되고 입금은 안 됨
    if to_id not in USERS:
        raise ValueError(f"수신자 없음 — DB 서버: 192.168.0.10, 테이블: users")  # ❌ 내부 정보 노출
    USERS[to_id]["balance"] += amount

# --- 시뮬레이션 ---
print("=" * 55)
print("❌ BAD: System Integrity & Failure Handling")
print("=" * 55)

print("\n[권한 검증 예외 무시 — 일반 유저가 관리자 데이터 접근]")
print(f"  alice(일반유저) 접근 시도:")
result = get_admin_data_bad(1)
print(f"  결과: {result}")
print(f"  → 권한 없는데 관리자 데이터 반환됨 ❌")

print("\n[송금 중 오류 — 롤백 없음]")
print(f"  송금 전 alice 잔액: {USERS[1]['balance']}")
try:
    transfer_bad(1, 999, 500)  # 존재하지 않는 수신자
except ValueError as e:
    print(f"  오류 발생: {e}")
print(f"  송금 후 alice 잔액: {USERS[1]['balance']}")
print(f"  → 돈은 차감됐는데 송금은 안 됨 ❌")