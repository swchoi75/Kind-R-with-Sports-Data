library(DBI)
library(duckdb)
library(here)

# Path
path <- here()

# Folder names
sql_folder <- file.path(path, "sql")

# Get all SQL files
sql_files <- sort(list.files(
  sql_folder,
  pattern = "\\.sql$",
  full.names = TRUE,
  recursive = TRUE
))


# DuckDB execution
# con <- dbConnect(duckdb::duckdb(), dbdir = ":memory:")
con <- dbConnect(duckdb::duckdb(), dbdir = "db.db")

for (file in sql_files) {
  print(paste("Running:", file))
  sql <- readLines(file, warn = FALSE, encoding = "UTF-8")
  sql <- paste(sql, collapse = "\n")
  dbExecute(con, sql)
}

# Close connection
dbDisconnect(con, shutdown = TRUE)
print("Connection closed")