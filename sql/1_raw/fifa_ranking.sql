CREATE TABLE IF NOT EXISTS "fifa_ranking" AS
SELECT * FROM read_csv_auto('data/fifa_ranking.csv');