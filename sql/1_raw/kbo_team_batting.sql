CREATE TABLE IF NOT EXISTS "data/kbo_team_batting.csv" AS
SELECT * FROM read_csv_auto('data/kbo_team_batting.csv');