# ✅ GOOD EXAMPLE — A10:2025 System Integrity & Failure Handling
# 수정: 예외별 명확한 처리 + 트랜잭션 롤백 + 안전한 에러 메시지
# 실행: python good.py

import logging
import copy

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("system")

# 가상 DB
USERS: dict[int, dict] = {
    1: {"id": 1, "username": "alice", "balance": 1000, "role": "user"},
    2: {"id": 2, "username": "admin", "balance": 9999, "role": "admin"},
}

# ✅ 수정 1: 예외를 명확하게 구분해서 처리
def get_admin_data_good(user_id: int) -> dict | None:
    try:
        user = USERS[user_id]
    except KeyError:
        # ✅ KeyError만 잡음 — PermissionError는 절대 무시 안 함
        logger.warning(f"존재하지 않는 유저 접근 시도: id={user_id}")
        return None

    # ✅ 권한 검증은 try 밖에서 명시적으로 처리
    if user["role"] != "admin":
        logger.warning(f"권한 없는 접근 시도: user={user['username']} role={user['role']}")
        return None  # ✅ 권한 없으면 절대 통과 안 함

    return {"secret": "관리자 전용 데이터"}

# ✅ 수정 2: 트랜잭션처럼 처리 — 실패 시 롤백
def transfer_good(from_id: int, to_id: int, amount: int) -> bool:
    # ✅ 롤백을 위해 변경 전 상태 저장
    snapshot = copy.deepcopy(USERS)

    try:
        if from_id not in USERS:
            raise ValueError("송금자를 찾을 수 없습니다")
        if to_id not in USERS:
            raise ValueError("수신자를 찾을 수 없습니다")
        if USERS[from_id]["balance"] < amount:
            raise ValueError("잔액이 부족합니다")

        USERS[from_id]["balance"] -= amount
        USERS[to_id]["balance"] += amount

        logger.info(f"TRANSFER_SUCCESS | from={from_id} to={to_id} amount={amount}")
        return True

    except ValueError as e:
        # ✅ 실패 시 롤백 — 내부 정보 없는 안전한 에러 메시지
        USERS.update(snapshot)
        logger.error(f"TRANSFER_FAILED | from={from_id} to={to_id} reason={e}")
        print(f"  → 송금 실패: {e} (롤백 완료) ✅")
        return False

# --- 시뮬레이션 ---
print("=" * 55)
print("✅ GOOD: System Integrity & Failure Handling")
print("=" * 55)

print("\n[권한 검증 — 명확한 예외 처리]")
print(f"  alice(일반유저) 접근 시도:")
result = get_admin_data_good(1)
print(f"  결과: {result}")
print(f"  → None 반환, 권한 검증 통과 불가 ✅")

print(f"\n  admin 접근 시도:")
result = get_admin_data_good(2)
print(f"  결과: {result} ✅")

print("\n[송금 중 오류 — 롤백 처리]")
print(f"  송금 전 alice 잔액: {USERS[1]['balance']}")
transfer_good(1, 999, 500)  # 존재하지 않는 수신자
print(f"  송금 후 alice 잔액: {USERS[1]['balance']}")
print(f"  → 잔액 그대로 유지됨 ✅")

print("\n[정상 송금]")
print(f"  alice → admin 300원 송금")
transfer_good(1, 2, 300)
print(f"  alice 잔액: {USERS[1]['balance']}")
print(f"  admin 잔액: {USERS[2]['balance']}")