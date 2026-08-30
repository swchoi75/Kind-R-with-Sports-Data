CREATE TABLE IF NOT EXISTS soccer_matches_results_in_progress AS
SELECT * FROM read_csv_auto(
    'data/soccer_matches_results_in_progress.csv',
     encoding = 'cp949'
);