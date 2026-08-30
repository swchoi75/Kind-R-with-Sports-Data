CREATE TABLE IF NOT EXISTS kbo_team_slash_untidy AS
SELECT * FROM read_csv_auto('interim/kbo_team_slash_untidy.csv');