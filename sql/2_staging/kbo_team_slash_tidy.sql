CREATE TABLE IF NOT EXISTS kbo_team_slash_tidy AS
SELECT * FROM read_csv_auto('interim/kbo_team_slash_tidy.csv');