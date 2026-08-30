import duckdb
from pathlib import Path

# Path
path = Path(__file__).resolve().parents[1]


# Folder names
sql_folder = path / "sql"


# Get all SQL files
sql_files = sorted(sql_folder.rglob("*.sql"))


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