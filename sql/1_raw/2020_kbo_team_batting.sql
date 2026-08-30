CREATE TABLE IF NOT EXISTS "2020_kbo_team_batting" AS
SELECT * FROM read_csv_auto('data/2020_kbo_team_batting.csv');