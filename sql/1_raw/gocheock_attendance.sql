CREATE TABLE IF NOT EXISTS gocheock_attendance AS
SELECT * FROM read_csv_auto('data/gocheock_attendance.csv');