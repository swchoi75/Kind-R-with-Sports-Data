import duckdb
from pathlib import Path


# Path
path = Path(__file__).resolve().parents[1]


# Find SQL files
sql_folder = path / "sql"
sql_files = sorted(sql_folder.rglob("*.sql"))
print(f"Found SQL files: {len(sql_files)}")


# DuckDB execution
# con = duckdb.connect(database=":memory:")
con = duckdb.connect(database="db.db")


for file in sql_files:
    print(f"Running: {file}")
    with open(file, "r", encoding="utf-8") as f:
        sql = f.read()
    con.sql(sql)


# Close connection
con.close()
print("Connection closed")


# 실제로 파일이 생성되었는지 확인
print((path / "db.db").exists())