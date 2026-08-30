CREATE TABLE IF NOT EXISTS kbo_team_batting AS
SELECT * FROM read_csv_auto('data/kbo_team_batting.csv');