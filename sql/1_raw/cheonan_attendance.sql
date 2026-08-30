CREATE TABLE IF NOT EXISTS "cheonan_attendance" AS
SELECT * FROM read_csv_auto('data/cheonan_attendance.csv');