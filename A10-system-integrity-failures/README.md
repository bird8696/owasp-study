# A10:2025 — System Integrity & Failure Handling

## 한 줄 요약

시스템이 오류날 때 **안전하게 실패하지 않으면** 공격자가 그 틈을 파고든다.

---

## 뭐가 문제야?

| #   | 문제                                  | 위험도                                      |
| --- | ------------------------------------- | ------------------------------------------- |
| 1   | 예외를 뭉뚱그려 무시 (`except: pass`) | 권한 검증이 조용히 건너뛰어짐               |
| 2   | 부분 실패 후 롤백 없음                | 잔액 차감만 되고 송금은 안 되는 불일치 상태 |
| 3   | 에러 메시지에 내부 정보 노출          | DB 서버 주소, 테이블명 공격자에게 노출      |

---

## 직접 테스트해봐

```bash
# Flask 불필요 — 바로 실행
python bad.py
python good.py
```

**bad.py 결과:**

- 일반 유저가 관리자 데이터 접근 성공
- 송금 실패했는데 alice 잔액만 500 줄어듦

**good.py 결과:**

- 일반 유저 접근 → None 반환
- 송금 실패 → 롤백으로 잔액 유지

---

## 핵심 정리

```python
# ❌ 절대 쓰지 마
try:
    check_permission()
except:
    pass  # 예외 무시 → 권한 검증 건너뜀

# ✅ 예외는 명확하게 구분
try:
    user = USERS[user_id]
except KeyError:
    return None  # KeyError만 처리

if user["role"] != "admin":  # 권한은 별도로 명시적 처리
    return None

# ❌ 롤백 없는 부분 실패
balance -= amount   # 차감
send(to, amount)    # 실패하면 차감만 됨

# ✅ 실패 시 롤백
snapshot = copy.deepcopy(state)
try:
    balance -= amount
    send(to, amount)
except:
    state.update(snapshot)  # 원상 복구
```

---

## 핵심 한 줄

> 시스템은 **실패할 때도 안전해야 한다.** 예외를 무시하면 보안이 조용히 무너진다.
