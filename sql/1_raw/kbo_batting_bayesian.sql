CREATE TABLE IF NOT EXISTS kbo_batting_bayesian AS
SELECT * FROM read_csv_auto('data/kbo_batting_bayesian.csv');