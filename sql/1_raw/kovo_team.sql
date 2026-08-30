CREATE TABLE IF NOT EXISTS "kovo_team" AS
SELECT * FROM read_csv_auto('data/kovo_team.csv');