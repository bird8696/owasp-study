# A08:2025 — Data Integrity Failures

## 한 줄 요약

외부 데이터를 **검증 없이 역직렬화하면** 공격자가 임의 코드를 실행할 수 있다.

---

## 뭐가 문제야?

| #   | 문제                                     | 위험도                             |
| --- | ---------------------------------------- | ---------------------------------- |
| 1   | `pickle.loads()` 로 외부 데이터 역직렬화 | 악성 데이터 한 줄로 서버 장악 가능 |
| 2   | 파일/데이터 무결성 검증 없음             | 변조된 설정 파일 탐지 불가         |

---

## 직접 테스트해봐

```bash
# Flask 불필요 — 바로 실행
python bad.py
python good.py
```

**bad.py 결과:**

- 악성 pickle 데이터 역직렬화 시 `echo` 명령어 실행됨
- 실제 공격이라면 `os.system("rm -rf /")` 같은 것도 실행 가능

**good.py 결과:**

- JSON은 코드 실행 기능 자체가 없음
- HMAC 서명으로 데이터 변조 즉시 탐지

---

## 핵심 정리

```python
# ❌ 절대 쓰지 마 (외부 데이터에)
pickle.loads(외부_데이터)       # 임의 코드 실행 가능
marshal.loads(외부_데이터)      # 동일하게 위험

# ✅ 외부 데이터엔 JSON
json.loads(외부_데이터)         # 코드 실행 기능 없음

# ✅ 무결성 검증은 HMAC
sig = hmac.new(key, data, sha256).hexdigest()
hmac.compare_digest(sig, received_sig)  # 타이밍 공격 방지
```

---

## 핵심 한 줄

> `pickle`은 **신뢰할 수 있는 내부 데이터**에만 써라. 외부 입력엔 절대 금지.
