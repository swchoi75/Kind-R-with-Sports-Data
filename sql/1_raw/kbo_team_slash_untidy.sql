CREATE TABLE IF NOT EXISTS "kbo_team_slash_untidy" AS
SELECT * FROM read_csv_auto('data/kbo_team_slash_untidy.csv');