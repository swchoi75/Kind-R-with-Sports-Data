library(DBI)
library(duckdb)
library(here)

# Path
path <- here()

# Find SQL files
sql_folder <- file.path(path, "sql")
sql_files <- sort(list.files(
  sql_folder,
  pattern = "\\.sql$",
  full.names = TRUE,
  recursive = TRUE
))

print(paste("Found SQL files:", length(sql_files)))

# DuckDB execution
# con <- dbConnect(duckdb::duckdb(), dbdir = ":memory:")
db_path <- normalizePath(here("db.db"), mustWork = FALSE)
con <- dbConnect(duckdb::duckdb(), dbdir = db_path)

for (file in sql_files) {
  print(paste("Running:", file))
  sql <- readLines(file, warn = FALSE, encoding = "UTF-8")
  sql <- paste(sql, collapse = "\n")
  dbExecute(con, sql)
}

# Close connection
dbDisconnect(con, shutdown = TRUE)
print("Connection closed")

# 실제로 파일이 생성되었는지 확인
print(file.exists(here("db.db")))