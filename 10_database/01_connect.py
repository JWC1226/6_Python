"""
    DB 연동
"""
import pandas as pd
import oracledb
from _db import connect, USER, HOST, PORT, NAME, PASS, get_engine

# connection 객체 반환 > _db.py 의 connect 함수
conn = connect()

# cursor() > Cursor 객체 반환
    # excute(sql) 함수를 통해 쿼리문을 실행한 결과를 반환받을 수 있다
with conn.cursor() as cur:
    cur.execute("SELECT(SELECT banner FROM v$version WHERE ROWNUM <= 1) AS v, "
                "sys_context('USERENV', 'DB_NAME') AS db FROM dual")
    # 한 　행 결과: fetchone
    # 여러 행 결과: fetchall
    row = cur.fetchone()
print(f"접속: {USER}@{HOST}:{PORT}/{NAME}")
print(f"조회 결과: v: {row[0]} / db: {row[1]}")

with conn.cursor() as cur:
    cur.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE demo_commit'; "
                "EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; "
                "END IF; END;")
    cur.execute("CREATE TABLE demo_commit (id NUMBER, memo VARCHAR2(50))")

c1 = connect()
with c1.cursor() as cur:
    cur.execute("INSERT INTO demo_commit VALUES (1, '테스트 1')")
    cur.execute("SELECT COUNT(*) FROM demo_commit")
    print(f"데이터 추가 후 바로 확인: {cur.fetchone()[0]}")

c1.close()
c2 = connect()
with c2.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM demo_commit")
    print(f"새로운 커넥션에서 조회: {cur.fetchone()[0]}")
"""
    커밋하지 않고, 커넥션을 반납했을 때(close) 오류가 발생되지 않았다
    DML 실행한 후에는 트랜잭션 관리를 잘 해줘야 한다
"""

c3 = connect()
with c3.cursor() as cur:
    cur.execute("INSERT INTO demo_commit VALUES (2, '테스트 2')")
c3.commit()     # 명시적 커밋
c3.close()

c4 = connect()
with c4.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM demo_commit")
    print(f"커밋 후 결과 조회: {cur.fetchone()[0]}")
c4.close()
print("-" * 40) # --------------------------------------------------

# 파라미터 바인딩
    # executemany(sql, [,,,]) : 동일한 sql을 사용하는데、값만 바꿔서 여러 번 전달
with conn.cursor() as cur:
    cur.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE demo_param'; "
                "EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; "
                "END IF; END;")
    cur.execute("CREATE TABLE demo_param (code VARCHAR2(10), price NUMBER)")
    cur.executemany(
        "INSERT INTO demo_param VALUES (:1, :2)", [("G0001", 24000), ("G0002", 55000), ("G0003", 10000)]
    )
conn.commit()
with conn.cursor() as cur:
    cur.execute("SELECT * FROM demo_param WHERE price > :1", (2000,))
    print(f"결과: {len(cur.fetchall())}행")
"""
    파라미터를 한 개만 넘기더라도 tuple로 전달하는 것을 권장한다
    변수가 여러 개인 경우、문자열을 하나만 전달하게 되면 자동으로 쪼개서 사용한다
"""
print("-" * 40) # --------------------------------------------------

# 조회 결과를 컬럼 이름으로 접근
# Cursor의 기본 반환값은 tuple 형태
plain = oracledb.connect(user=USER, password=PASS, dsn=f"{HOST}:{PORT}/{NAME}")
with plain.cursor() as cur:
    cur.execute("SELECT * FROM demo_param WHERE ROWNUM <= 1")
    print(f"기본 커서: {cur.fetchone()}")
plain.close()

# rowfactory : 컬럼 이름으로 데이터에 접근할 수 있다
with conn.cursor() as cur:
    cur.execute("SELECT * FROM demo_param WHERE ROWNUM <= 1")
    columns = [col[0].lower() for col in cur.description]
    cur.rowfactory = lambda *args: dict(zip(columns, args))
    print(f"rowfactory 설정 후: {cur.fetchone()}")
print("-" * 40) # --------------------------------------------------

#SQLAlchemy 사용하는 이유 > Pandas와의 연계성 때문에 사용한다
engine = get_engine()

df = pd.read_sql("SELECT * FROM demo_param ORDER BY price DESC", engine)
print(df)
print(df.info())
# 가능하다면 DB에서 정렬 후 데이터를 가져오는게 좀 더 빠르다

with conn.cursor() as cur:
    for t in ["demo_commit", "demo_param"]:
        cur.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE {t}'; "
                    "EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; "
                    "END IF; END;")
conn.close()
print("테이블 정리 완료")