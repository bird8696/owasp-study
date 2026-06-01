# 🔐 OWASP Top 10:2025 스터디

> OWASP Top 10:2025 기준 보안 취약점 입문 예제 모음  
> 각 항목별 취약한 코드(`bad.py`)와 수정된 코드(`good.py`)를 직접 실행하며 비교할 수 있습니다.

---

## 📌 개요

| 항목 | 내용                                       |
| ---- | ------------------------------------------ |
| 기준 | OWASP Top 10:2025                          |
| 언어 | Python 3.11                                |
| 목적 | 보안 취약점 개념 이해 + 직접 실행으로 확인 |
| 대상 | 보안 입문자, 개발자                        |

---

## 🗂️ 목차

| #                                                   | 항목                           | 핵심 개념                      |
| --------------------------------------------------- | ------------------------------ | ------------------------------ |
| [A01](#a01-broken-access-control)                   | Broken Access Control          | 인증 ≠ 인가, IDOR              |
| [A02](#a02-security-misconfiguration)               | Security Misconfiguration      | debug=True, 하드코딩 시크릿    |
| [A03](#a03-software-supply-chain-failures)          | Software Supply Chain Failures | 취약한 의존성, yaml.load()     |
| [A04](#a04-cryptographic-failures)                  | Cryptographic Failures         | MD5/평문 저장 vs bcrypt        |
| [A05](#a05-injection)                               | Injection                      | SQL Injection, 파라미터 바인딩 |
| [A06](#a06-insecure-design)                         | Insecure Design                | 브루트포스 방어, Rate Limiting |
| [A07](#a07-identification--authentication-failures) | Authentication Failures        | 예측 가능한 세션 토큰          |
| [A08](#a08-data-integrity-failures)                 | Data Integrity Failures        | pickle 역직렬화, HMAC          |
| [A09](#a09-security-logging--alerting-failures)     | Logging & Alerting Failures    | 로그 없음, 민감정보 기록       |
| [A10](#a10-system-integrity--failure-handling)      | System Integrity Failures      | 예외 무시, 롤백 없음           |

---

## ⚙️ 실행 방법

```bash
# 저장소 클론
git clone https://github.com/bird8696/owasp-study.git
cd owasp-study

# 의존성 설치 (Flask, bcrypt만 필요)
pip install flask bcrypt pyyaml

# 각 항목 폴더로 이동 후 실행
cd A01-broken-access-control
python bad.py   # 취약한 버전
python good.py  # 수정된 버전
```

> A01, A02는 Flask 서버로 실행됩니다 (포트 8080/8081)  
> 나머지는 Flask 없이 바로 실행됩니다

---

## 📂 항목별 상세

---

### A01: Broken Access Control

> **핵심**: 로그인했다고 다 볼 수 있는 게 아니다. 인증(Authentication) ≠ 인가(Authorization)

**취약점 (bad.py)**

```python
# URL의 숫자만 바꾸면 다른 사람 정보를 볼 수 있음 (IDOR)
@app.route("/user/<int:user_id>")
def get_user(user_id: int):
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify(USERS.get(user_id))  # ❌ 내 정보인지 확인 안 함
```

**수정 (good.py)**

```python
is_owner = session["user_id"] == user_id
is_admin = current_user.get("role") == "admin"
if not (is_owner or is_admin):
    return jsonify({"error": "Not found"}), 404  # ✅ 존재 여부도 숨김
```

---

### A02: Security Misconfiguration

> **핵심**: 코드는 멀쩡한데 설정 하나 잘못해서 서버가 통째로 털린다

**취약점 (bad.py)**

```python
app.secret_key = "1234"           # ❌ 하드코딩된 시크릿 키
app.run(debug=True, port=8080)    # ❌ debug=True → 브라우저에서 코드 실행 가능
```

**수정 (good.py)**

```python
app.secret_key = os.environ.get("FLASK_SECRET", os.urandom(32))  # ✅ 환경변수
app.run(debug=False, host='127.0.0.1', port=8081)                 # ✅ debug=False
```

---

### A03: Software Supply Chain Failures

> **핵심**: 내 코드는 멀쩡한데 가져다 쓴 라이브러리가 털린다

**취약점 (bad.py)**

```python
yaml.load(data, Loader=yaml.Loader)              # ❌ 임의 코드 실행 가능
subprocess.check_output(f"cat {filename}", shell=True)  # ❌ 명령어 인젝션
```

**수정 (good.py)**

```python
yaml.safe_load(data)                              # ✅ 코드 실행 불가
subprocess.check_output(["cat", filename], shell=False)  # ✅ 인젝션 차단
```

```bash
# 실제 취약점 검사
pip install pip-audit
pip-audit  # 설치된 패키지 CVE 목록 확인
```

---

### A04: Cryptographic Failures

> **핵심**: MD5, SHA1은 비밀번호 저장용이 아니다. bcrypt 써라

**취약점 (bad.py)**

```python
hashlib.md5(password.encode()).hexdigest()   # ❌ 레인보우 테이블로 즉시 역추적
```

**수정 (good.py)**

```python
bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))  # ✅ salt + 느린 해시
```

---

### A05: Injection

> **핵심**: 외부 입력은 절대 쿼리 문자열에 직접 넣지 마라

**취약점 (bad.py)**

```python
query = f"SELECT * FROM users WHERE username = '{username}'"
# 공격 입력: ' OR '1'='1 → 비밀번호 없이 로그인 성공
```

**수정 (good.py)**

```python
query = "SELECT * FROM users WHERE username = ?"
conn.execute(query, (username,))  # ✅ 파라미터 바인딩
```

---

### A06: Insecure Design

> **핵심**: 보안은 나중에 붙이는 게 아니라 설계할 때부터 들어가야 한다

**취약점 (bad.py)**

```python
def login(username, password):
    return USERS.get(username) == password  # ❌ 무한 시도 가능
```

**수정 (good.py)**

```python
# ✅ 3회 실패 시 계정 30초 잠금 + 실패 로그 기록
if guard.is_locked(username): return False
if check_password(): ...
else: guard.record_fail(username)
```

---

### A07: Identification & Authentication Failures

> **핵심**: 세션 토큰은 예측 불가능해야 하고, 로그아웃하면 즉시 무효화되어야 한다

**취약점 (bad.py)**

```python
token = f"session_{counter}"  # ❌ session_1, session_2... 예측 가능
def logout(): pass             # ❌ 세션 안 지움
```

**수정 (good.py)**

```python
token = secrets.token_urlsafe(32)  # ✅ 256비트 난수
def logout(token): del SESSIONS[token]  # ✅ 즉시 무효화
```

---

### A08: Data Integrity Failures

> **핵심**: pickle은 신뢰할 수 있는 내부 데이터에만 써라. 외부 입력엔 절대 금지

**취약점 (bad.py)**

```python
pickle.loads(외부_데이터)  # ❌ 악성 데이터로 임의 코드 실행 가능
```

**수정 (good.py)**

```python
json.loads(외부_데이터)    # ✅ 코드 실행 기능 없음
# + HMAC으로 데이터 무결성 서명 및 변조 탐지
```

---

### A09: Security Logging & Alerting Failures

> **핵심**: 로그는 공격의 흔적이다. 없으면 뚫린 것도 모른다

**취약점 (bad.py)**

```python
def login(username, password):
    if check(username, password): return True
    return False  # ❌ 실패해도 아무 로그 없음

logger.info(f"시도: {username}, {password}")  # ❌ 비밀번호 로그에 남음
```

**수정 (good.py)**

```python
logger.warning(f"LOGIN_FAILED | user={username} ip={ip} attempts={count}")
# 3회 초과 시 CRITICAL 경보 발생 ✅
# 비밀번호는 로그에 절대 포함 안 함 ✅
```

---

### A10: System Integrity & Failure Handling

> **핵심**: 시스템은 실패할 때도 안전해야 한다. 예외를 무시하면 보안이 조용히 무너진다

**취약점 (bad.py)**

```python
try:
    check_permission()
except:
    pass  # ❌ 모든 예외 무시 → 권한 검증 건너뜀
```

**수정 (good.py)**

```python
try:
    user = USERS[user_id]
except KeyError:       # ✅ 필요한 예외만 명시적으로 처리
    return None
if user["role"] != "admin":  # ✅ 권한은 별도로 검증
    return None
```

---

## 📚 참고 자료

- [OWASP Top 10:2025 공식 문서](https://owasp.org/www-project-top-ten/)
- [pip-audit](https://github.com/pypa/pip-audit)
- [CrackStation (해시 역추적 테스트)](https://crackstation.net)

---

## ⚠️ 주의사항

이 저장소의 `bad.py` 파일들은 **교육 목적**으로만 작성되었습니다.  
실제 서비스에 취약한 코드를 사용하지 마세요.

---

## 📝 라이선스

MIT License
