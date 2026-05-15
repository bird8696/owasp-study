# ✅ GOOD EXAMPLE — A05:2025 Injection
# 수정: 파라미터 바인딩으로 SQL Injection 차단
# 실행: python good.py

import sqlite3

# DB 초기화
def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        )
    """)
    conn.execute("INSERT INTO users VALUES (1, 'alice', 'password123', 'user')")
    conn.execute("INSERT INTO users VALUES (2, 'bob',   'qwerty',      'user')")
    conn.execute("INSERT INTO users VALUES (3, 'admin', 'supersecret', 'admin')")
    conn.commit()

# ✅ 핵심 수정: 파라미터 바인딩 (?) 사용
# 입력값이 쿼리 구조에 영향을 줄 수 없음
def login_good(conn: sqlite3.Connection, username: str, password: str):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    print(f"  실행 쿼리: {query}")
    print(f"  바인딩 값: ({username!r}, {password!r})")
    return conn.execute(query, (username, password)).fetchone()

# --- 시뮬레이션 ---
conn = sqlite3.connect(":memory:")
init_db(conn)

print("=" * 55)
print("✅ GOOD: Parameterized Query")
print("=" * 55)

print("\n[정상 로그인]")
result = login_good(conn, "alice", "password123")
print(f"  결과: {result} ✅")

print("\n[SQL Injection 시도 — 비밀번호 없이 로그인]")
result = login_good(conn, "admin", "' OR '1'='1")
print(f"  결과: {result}")
print("  → None 반환, 로그인 차단 ✅")

print("\n[SQL Injection 시도 — UNION 공격]")
result = login_good(conn, "' UNION SELECT 1,username,password,role FROM users--", "x")
print(f"  결과: {result}")
print("  → None 반환, DB 덤프 차단 ✅")

print("\n[파라미터 바인딩이 안전한 이유]")
print("  입력값을 문자열 그대로 처리 → SQL 구조 변경 불가")
print("  ' OR '1'='1  →  그냥 비밀번호 문자열로만 취급됨")

conn.close()