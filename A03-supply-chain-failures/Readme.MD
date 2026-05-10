# A03:2025 — Software Supply Chain Failures

## 한 줄 요약

내 코드는 멀쩡한데 **가져다 쓴 라이브러리가 털리는 것.**

---

## 뭐가 문제야?

| #   | 문제                     | 위험도                                           |
| --- | ------------------------ | ------------------------------------------------ |
| 1   | 버전 고정 없는 의존성    | 언제 취약한 버전 들어올지 모름                   |
| 2   | `yaml.load()` 사용       | 악성 YAML로 임의 코드 실행 가능 (CVE-2017-18342) |
| 3   | `shell=True` + 외부 입력 | 명령어 인젝션으로 서버 장악 가능                 |

---

## 직접 테스트해봐

```bash
# bad/good 실행 (Flask 불필요 — 바로 실행)
python bad.py
python good.py
```

```bash
# 현재 설치된 패키지 취약점 검사
pip install pip-audit
pip-audit
```

```bash
# 버전 고정된 의존성 설치
pip install -r requirements_good.txt

# 버전 미고정 — 위험
pip install -r requirements_bad.txt
```

---

## 핵심 정리

```python
# ❌ 절대 쓰지 마
yaml.load(data)                              # 임의 코드 실행 가능
subprocess.run(f"cmd {input}", shell=True)   # 명령어 인젝션 가능

# ✅ 이렇게 써
yaml.safe_load(data)                         # 안전
subprocess.run(["cmd", input], shell=False)  # 안전
```

---

## 핵심 한 줄

> 라이브러리도 공격 표면이다. **버전 고정 + 정기적인 취약점 검사**는 선택이 아니라 기본이다.
