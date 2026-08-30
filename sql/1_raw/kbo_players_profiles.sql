CREATE TABLE IF NOT EXISTS "kbo_players_profiles" AS
SELECT * FROM read_csv_auto('data/kbo_players_profiles.csv');