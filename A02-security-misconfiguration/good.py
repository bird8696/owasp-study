# ✅ GOOD EXAMPLE — A02:2025 Security Misconfiguration
# 수정: 환경변수로 설정 분리 + 보안 헤더 + 에러 메시지 최소화
# 실행: python good.py → http://127.0.0.1:8081

import os
from flask import Flask, jsonify

app = Flask(__name__)

# ✅ 수정 1: 시크릿 키를 환경변수에서 읽음
# 터미널에서: set FLASK_SECRET=my-secret-key (Windows)
#             export FLASK_SECRET=my-secret-key (Mac/Linux)
app.secret_key = os.environ.get("FLASK_SECRET", os.urandom(32))

# ✅ 수정 2: 모든 응답에 보안 헤더 추가
@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

@app.route("/user/<int:user_id>")
def get_user(user_id: int):
    users = {1: "Alice", 2: "Bob"}
    user = users.get(user_id)

    # ✅ 수정 3: 에러 메시지에 내부 정보 절대 포함 안 함
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"name": user})

@app.route("/crash")
def crash():
    raise Exception("의도적 크래시")

# ✅ 수정 4: 에러 핸들러로 스택트레이스 노출 차단
@app.errorhandler(Exception)
def handle_error(e):
    # 내부 로그엔 상세 기록, 클라이언트엔 최소한만 반환
    app.logger.error(f"Internal error: {e}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # ✅ 수정 5: debug=False — 운영 환경에선 절대 True 쓰면 안 됨
    app.run(debug=False, host='127.0.0.1', port=8081)