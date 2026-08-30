CREATE TABLE IF NOT EXISTS kbo_batting_qualified AS
SELECT * FROM read_csv_auto('data/kbo_batting_qualified.csv');