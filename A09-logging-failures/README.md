# A09:2025 — Security Logging & Alerting Failures

## 한 줄 요약

공격당하는데 **로그가 없으면 탐지도 대응도 불가능하다.**

---

## 뭐가 문제야?

| #   | 문제                   | 결과                             |
| --- | ---------------------- | -------------------------------- |
| 1   | 로그인 실패 로그 없음  | 브루트포스 공격 탐지 불가        |
| 2   | 비밀번호를 로그에 기록 | 로그 파일 털리면 비밀번호도 노출 |
| 3   | 이상 탐지 없음         | 공격이 완료될 때까지 모름        |

---

## 직접 테스트해봐

```bash
# Flask 불필요 — 바로 실행
python bad.py
python good.py
```

**bad.py 결과:**

- 브루트포스 시도해도 아무 기록 없음
- 비밀번호가 로그에 평문으로 출력됨

**good.py 결과:**

- 실패마다 WARNING 로그
- 3회 초과 시 CRITICAL 경보 발생
- 비밀번호는 로그에 없음

---

## 핵심 정리

```python
# ❌ 이렇게 하면 안 됨
def login(username, password):
    if check(username, password):
        return True
    return False  # 아무 로그 없음

# ❌ 민감 정보 로그 금지
logger.info(f"시도: {username}, {password}")  # 비밀번호 노출

# ✅ 이렇게 해야 함
def login(username, password, ip):
    if check(username, password):
        logger.info(f"LOGIN_SUCCESS | user={username} ip={ip}")
        return True
    logger.warning(f"LOGIN_FAILED | user={username} ip={ip}")
    return False
```

---

## 로그에 포함할 것 vs 제외할 것

| 포함 ✅     | 제외 ❌           |
| ----------- | ----------------- |
| 타임스탬프  | 비밀번호          |
| 사용자명    | 토큰/세션 ID 전체 |
| IP 주소     | 주민번호/카드번호 |
| 이벤트 종류 | 개인식별정보(PII) |
| 실패 횟수   |                   |

---

## 핵심 한 줄

> 로그는 **공격의 흔적**이다. 없으면 뚫린 것도 모른다.
