# A07:2025 — Identification & Authentication Failures

## 한 줄 요약

세션 토큰이 **예측 가능하거나 로그아웃 후에도 유효하면** 공격자가 계정을 탈취할 수 있다.

---

## 뭐가 문제야?

| #   | 문제                                    | 위험도                        |
| --- | --------------------------------------- | ----------------------------- |
| 1   | `session_1`, `session_2`... 순차적 토큰 | 공격자가 다음 토큰 예측 가능  |
| 2   | 로그아웃해도 세션 안 지움               | 토큰 탈취 후 계속 재사용 가능 |
| 3   | 세션 만료 없음                          | 한번 탈취하면 영구 사용 가능  |

---

## 직접 테스트해봐

```bash
# Flask 불필요 — 바로 실행
python bad.py
python good.py
```

**bad.py 결과:**

- 토큰이 session_1, session_2, session_3으로 순서대로 생성
- 로그아웃 후에도 토큰으로 alice 조회 가능

**good.py 결과:**

- 토큰이 완전한 난수 (256비트)
- 로그아웃 즉시 None 반환
- 10초 후 자동 만료

---

## 핵심 정리

```python
# ❌ 절대 쓰지 마
session_id = f"session_{counter}"      # 예측 가능
session_id = str(user_id)              # 더 위험
session_id = hashlib.md5(username)     # 역추적 가능

# ✅ 이것만 써
session_id = secrets.token_urlsafe(32) # 256비트 암호학적 난수

# ❌ 로그아웃
def logout(): pass                     # 아무것도 안 함

# ✅ 로그아웃
def logout(token):
    del SESSIONS[token]                # 즉시 무효화
```

---

## 핵심 한 줄

> 세션 토큰은 **예측 불가능**해야 하고, 로그아웃하면 **즉시 무효화**되어야 한다.
