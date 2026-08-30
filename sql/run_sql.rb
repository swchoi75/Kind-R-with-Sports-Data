require 'duckdb'


# Path
project_root = File.expand_path('../', __dir__)
Dir.chdir(project_root)

# Find SQL files
sql_folder = File.join(project_root, 'sql')
sql_files = Dir.glob(File.join(sql_folder, '**/*.sql')).sort


# DuckDB execution
# con = DuckDB::Database.new(":memory:")
db = DuckDB::Database.new("db.db")
con = db.connect

sql_files.each do |file|
  puts "Running: #{file}"
  sql = File.read(file, encoding: "UTF-8")
  con.query(sql)
end

# Close connection
con.close
puts "Connection closed"
