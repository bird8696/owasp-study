# ❌ BAD EXAMPLE — A02:2025 Security Misconfiguration
# 문제: 잘못된 설정으로 서버 내부가 통째로 노출됨
# 실행: python bad.py → http://127.0.0.1:8080

from flask import Flask, request, jsonify

app = Flask(__name__)

# ❌ 문제 1: 시크릿 키 하드코딩 — 코드만 보면 바로 탈취 가능
app.secret_key = "1234"

# ❌ 문제 2: 보안 헤더 없음 — 브라우저 공격에 무방비

@app.route("/user/<int:user_id>")
def get_user(user_id: int):
    users = {1: "Alice", 2: "Bob"}
    user = users.get(user_id)

    # ❌ 문제 3: 에러 메시지에 내부 정보 노출
    if not user:
        raise ValueError(f"DB에서 user_id={user_id} 조회 실패 — 서버: 192.168.0.10, DB: MySQL 8.0")

    return jsonify({"name": user})

@app.route("/crash")
def crash():
    # ❌ 문제 4: debug=True 상태에서 에러 → 브라우저에 전체 스택트레이스 + 인터랙티브 콘솔 노출
    raise Exception("의도적 크래시 — debug 모드에서 접속해봐")

if __name__ == "__main__":
    # ❌ 문제 4: debug=True → 공격자가 브라우저에서 서버 코드 실행 가능
    app.run(debug=True, host='127.0.0.1', port=8080)