# ❌ BAD EXAMPLE — A01:2025 Broken Access Control
# 문제: URL의 user_id만 바꾸면 다른 사람 정보를 볼 수 있음 (IDOR)
# 실행: python bad.py → http://localhost:5000/user/1 또는 /user/2

from flask import Flask, jsonify, request, session

app = Flask(__name__)
app.secret_key = "example-secret"

# 가상 DB
USERS: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "ssn": "123-45-6789"},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com",   "ssn": "987-65-4321"},
}

@app.route("/login/<int:user_id>")
def fake_login(user_id: int):
    """테스트용 로그인 — user_id로 세션 설정"""
    session["user_id"] = user_id
    return jsonify({"message": f"Logged in as user {user_id}"})

@app.route("/user/<int:user_id>")
def get_user(user_id: int):
    # ❌ 핵심 문제: 로그인 여부만 확인하고 '내 정보인지'는 확인 안 함
    # 누구든 /user/1, /user/2 URL만 알면 다른 사람 SSN까지 볼 수 있음
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    user = USERS.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)  # ❌ 아무 user_id나 조회 가능

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080)