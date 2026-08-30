CREATE TABLE IF NOT EXISTS "international_soccer_matches_results" AS
SELECT * FROM read_csv_auto(
    'data/international_soccer_matches_results.csv',
    encoding = 'cp949'
);