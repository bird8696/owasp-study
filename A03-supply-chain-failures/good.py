# ✅ GOOD EXAMPLE — A03:2025 Software Supply Chain Failures
# 수정: 안전한 라이브러리 사용법 + 입력 검증
# 실행: python good.py

import yaml
import subprocess
import shlex
import os

# ✅ 수정 1: yaml.safe_load() 사용 — 파이썬 객체 역직렬화 차단
def parse_config_good(yaml_string: str) -> dict:
    return yaml.safe_load(yaml_string)  # ✅ 임의 코드 실행 불가

# ✅ 수정 2: shell=False + 리스트로 인자 전달 — 명령어 인젝션 차단
def run_command_good(filename: str) -> str:
    # 경로 traversal 방지: 파일명만 추출
    safe_name = os.path.basename(filename)

    # shlex.split 또는 리스트로 명시적 인자 전달
    result = subprocess.check_output(
        ["cat", safe_name],  # ✅ 리스트로 전달 → ; 같은 특수문자 무력화
        shell=False,          # ✅ shell=False
        text=True
    )
    return result

# ✅ 수정 3: 의존성 취약점 검사 방법 안내
def check_dependencies() -> None:
    print("의존성 취약점 검사 명령어:")
    print("  pip-audit")
    print("  pip-audit -r requirements_good.txt")
    print("취약점 발견 시 → pip install 패키지==안전한버전 으로 업데이트")

# --- 시뮬레이션 ---
print("=" * 50)
print("✅ GOOD: Safe Library Usage")
print("=" * 50)

# 안전한 YAML 파싱
normal_yaml = "name: Alice\nage: 30"
print("\n[안전한 yaml.safe_load() 사용]")
print(parse_config_good(normal_yaml))
print("→ 악성 YAML 입력해도 코드 실행 불가 ✅")

# 명령어 인젝션 방어
print("\n[shell=False + 리스트 인자로 인젝션 차단]")
malicious_input = "test.txt; echo '공격 시도'"
safe_name = os.path.basename(malicious_input)
print(f"입력값: {malicious_input}")
print(f"처리 후: {['cat', safe_name]}")
print("→ ; 이후 명령어 실행 불가 ✅")

print("\n[의존성 관리]")
check_dependencies()