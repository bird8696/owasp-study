# ❌ BAD EXAMPLE — A05:2025 Injection (SQL Injection)
# 문제: 외부 입력을 검증 없이 SQL 쿼리에 직접 삽입
# 실행: python bad.py

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

# ❌ 핵심 문제: f-string으로 쿼리 조합 → SQL Injection 가능
def login_bad(conn: sqlite3.Connection, username: str, password: str):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"  실행 쿼리: {query}")
    return conn.execute(query).fetchone()

# --- 시뮬레이션 ---
conn = sqlite3.connect(":memory:")
init_db(conn)

print("=" * 55)
print("❌ BAD: SQL Injection")
print("=" * 55)

print("\n[정상 로그인]")
result = login_bad(conn, "alice", "password123")
print(f"  결과: {result}")

print("\n[SQL Injection 공격 — 비밀번호 없이 로그인]")
# ' OR '1'='1 → WHERE 조건을 항상 참으로 만들어버림
result = login_bad(conn, "admin", "' OR '1'='1")
print(f"  결과: {result}")
print("  → 비밀번호 몰라도 admin 로그인 성공 ❌")

print("\n[SQL Injection 공격 — 전체 DB 덤프]")
# UNION으로 다른 테이블 데이터까지 끌어옴
result = login_bad(conn, "' UNION SELECT 1,username,password,role FROM users--", "x")
print(f"  결과: {result}")
print("  → 전체 유저 테이블 털림 ❌")

conn.close()