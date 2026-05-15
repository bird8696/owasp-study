# A05:2025 — Injection

## 한 줄 요약

외부 입력이 **검증 없이 쿼리/명령어로 실행되면** 공격자가 DB를 통째로 장악한다.

---

## 뭐가 문제야?

```python
# ❌ 이렇게 하면 터짐
query = f"SELECT * FROM users WHERE username = '{username}'"

# 공격자 입력: ' OR '1'='1
# 실제 실행:   SELECT * FROM users WHERE username = '' OR '1'='1'
# 결과:        WHERE 조건이 항상 참 → 전체 테이블 반환
```

---

## 직접 테스트해봐

```bash
# Flask 불필요 — 바로 실행
python bad.py
python good.py
```

**bad.py 결과에서 확인할 것:**

- 비밀번호 없이 admin 로그인 성공
- UNION으로 전체 유저 테이블 덤프

**good.py 결과에서 확인할 것:**

- 같은 공격 시도 → None 반환으로 차단

---

## 핵심 정리

```python
# ❌ 절대 쓰지 마
query = f"SELECT * FROM users WHERE username = '{username}'"
query = "SELECT * FROM users WHERE username = '" + username + "'"

# ✅ 파라미터 바인딩만 써
query = "SELECT * FROM users WHERE username = ?"
conn.execute(query, (username,))

# ORM 쓴다면 (SQLAlchemy 예시)
User.query.filter_by(username=username).first()  # ✅ 자동으로 안전하게 처리
```

---

## 핵심 한 줄

> 외부 입력은 **절대** 쿼리 문자열에 직접 넣지 마라. 파라미터 바인딩만 써라.
