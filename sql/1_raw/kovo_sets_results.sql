CREATE TABLE IF NOT EXISTS "kovo_sets_results" AS
SELECT * FROM read_csv_auto('data/kovo_sets_results.csv');