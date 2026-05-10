# ❌ BAD EXAMPLE — A03:2025 Software Supply Chain Failures
# 문제: 외부 입력을 검증 없이 라이브러리에 그대로 넘김
# 실행: python bad.py

import yaml
import subprocess

# ❌ 문제 1: yaml.load() — 임의 코드 실행 가능 (CVE-2017-18342)
# yaml.safe_load() 가 있는데도 unsafe한 yaml.load() 사용
def parse_config_bad(yaml_string: str) -> dict:
    return yaml.load(yaml_string, Loader=yaml.Loader)  # ❌ Loader 명시해도 FullLoader/Loader는 위험

# ❌ 문제 2: 외부 입력을 shell=True로 실행 — 명령어 인젝션 가능
def run_command_bad(filename: str) -> str:
    return subprocess.check_output(f"cat {filename}", shell=True, text=True)  # ❌

# --- 시뮬레이션 ---
print("=" * 50)
print("❌ BAD: Supply Chain / Unsafe Library Usage")
print("=" * 50)

# 일반 YAML 파싱
normal_yaml = "name: Alice\nage: 30"
print("\n[일반 YAML 파싱]")
print(parse_config_bad(normal_yaml))

# 악성 YAML — yaml.load()는 파이썬 객체를 역직렬화함
# 실제 공격 페이로드는 생략, 위험성만 표시
print("\n[취약한 yaml.load() 사용 중]")
print("→ 악성 YAML 입력 시 임의 코드 실행 가능 ❌")
print("→ CVE-2017-18342 참고")

# 명령어 인젝션 시뮬레이션
print("\n[shell=True 명령어 인젝션 위험]")
safe_input = "test.txt"
print(f"정상 입력: cat {safe_input}")
malicious_input = "test.txt; echo '공격자 코드 실행'"
print(f"악성 입력: cat {malicious_input}")
print("→ shell=True 면 ; 뒤 명령어까지 그대로 실행됨 ❌")