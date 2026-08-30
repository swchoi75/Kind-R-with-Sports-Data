CREATE TABLE IF NOT EXISTS tennis_big3_results AS
SELECT * FROM read_csv_auto('data/tennis_big3_results.csv');