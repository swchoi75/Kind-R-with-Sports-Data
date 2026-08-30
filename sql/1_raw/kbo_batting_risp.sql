CREATE TABLE IF NOT EXISTS kbo_batting_risp AS
SELECT * FROM read_csv_auto('data/kbo_batting_risp.csv');