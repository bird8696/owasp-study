# A01:2025 — Broken Access Control

## 한 줄 요약

로그인했다고 다 볼 수 있는 게 아니다. **"내 것만 볼 수 있어야 한다."**

---

## 뭐가 문제야?

`bad.py`에서는 로그인만 하면 URL의 숫자만 바꿔서 **다른 사람 정보를 전부 볼 수 있어.**
이걸 **IDOR (Insecure Direct Object Reference)** 라고 불러.

```bash
# Alice로 로그인했는데
GET /user/2   # → Bob의 SSN까지 그대로 반환됨 ❌
```

---

## 어떻게 고쳐?

`good.py`에서 적용한 수정 3가지:

| #   | 수정 내용                                                   |
| --- | ----------------------------------------------------------- |
| 1   | **본인 or 관리자만** 조회 가능하도록 역할 확인              |
| 2   | 권한 없으면 **403이 아닌 404** 반환 (존재 여부 자체를 숨김) |
| 3   | 일반 유저에겐 **SSN 같은 민감 필드 제외**하고 반환          |

---

## 직접 테스트해봐

```bash
# 터미널 1 — 취약한 버전
python bad.py

# 터미널 2 — 수정된 버전
python good.py
```

```bash
# bad.py 테스트 (포트 5000)
curl http://localhost:5000/login/1   # Alice로 로그인
curl http://localhost:5000/user/2    # Bob 정보 그대로 노출됨 ❌

# good.py 테스트 (포트 5001)
curl http://localhost:5001/login/1   # Alice로 로그인
curl http://localhost:5001/user/2    # 404 반환 ✅
curl http://localhost:5001/login/3   # Admin으로 로그인
curl http://localhost:5001/user/2    # SSN 포함 전체 반환 ✅
```

---

## 핵심 한 줄

> 인증(Authentication) ≠ 인가(Authorization)
> 로그인 = 신원 확인 / 접근 권한 = 별도로 확인해야 함
