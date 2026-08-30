CREATE TABLE IF NOT EXISTS "nba_draft_data" AS
SELECT * FROM read_csv_auto(
    'data/nba_draft_data.csv',
    encoding = 'cp949'
 );