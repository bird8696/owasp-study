# ✅ GOOD EXAMPLE — A01:2025 Broken Access Control
# 수정: 내 정보인지 확인 + 관리자만 전체 조회 가능
# 실행: python good.py → http://localhost:5001/user/1 또는 /user/2

from flask import Flask, jsonify, request, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "example-secret"

# 가상 DB
USERS: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com", "ssn": "123-45-6789", "role": "user"},
    2: {"id": 2, "name": "Bob",   "email": "bob@example.com",   "ssn": "987-65-4321", "role": "user"},
    3: {"id": 3, "name": "Admin", "email": "admin@example.com", "ssn": "000-00-0000", "role": "admin"},
}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Not logged in"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/login/<int:user_id>")
def fake_login(user_id: int):
    """테스트용 로그인"""
    session["user_id"] = user_id
    return jsonify({"message": f"Logged in as user {user_id}"})

@app.route("/user/<int:user_id>")
@login_required
def get_user(user_id: int):
    current_user = USERS.get(session["user_id"])
    target_user  = USERS.get(user_id)

    if not target_user:
        return jsonify({"error": "User not found"}), 404

    # ✅ 핵심 수정 1: 본인 or 관리자만 조회 가능
    is_owner = session["user_id"] == user_id
    is_admin = current_user and current_user.get("role") == "admin"

    if not (is_owner or is_admin):
        # ✅ 핵심 수정 2: 존재 여부도 노출하지 않음 (404로 통일)
        return jsonify({"error": "Not found"}), 404

    # ✅ 핵심 수정 3: 관리자가 아니면 민감 정보(SSN) 제외
    if is_admin:
        return jsonify(target_user)
    else:
        safe_user = {k: v for k, v in target_user.items() if k != "ssn"}
        return jsonify(safe_user)

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8081)