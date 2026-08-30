CREATE TABLE IF NOT EXISTS "19_20_nba" AS
SELECT * FROM read_csv_auto('data/19_20_nba.csv');