import polars as pl
import numpy as np
# For the plotting section, we'll need to convert to a plotting-friendly format (like list or df)
# Polars does not have a built-in plotting library like ggplot2.

# --- Data Loading ---
try:
    # Read the data into a Polars DataFrame
    team_batting = pl.read_csv('kbo_team_batting.csv')
except pl.exceptions.ComputeError:
    print("kbo_team_batting.csv not found. Creating a dummy DataFrame for demonstration.")
    # Create a dummy DataFrame if the file is missing
    data = {
        'team': ['OB', 'MBC', '삼미', '삼미', '삼미', '삼미', 'OB', 'MBC'],
        'year': [1982, 1982, 1982, 1983, 1984, 1985, 1983, 1983],
        'g': [80, 80, 80, 100, 100, 100, 100, 100],
        'h': [650, 700, 600, 800, 900, 750, 750, 850],
        'ab': [2500, 2600, 2400, 3000, 3100, 2800, 2900, 3200],
        'X2b': [100, 110, 90, 150, 160, 130, 140, 150],
        'X3b': [10, 12, 8, 15, 18, 14, 16, 17],
        'hr': [50, 60, 45, 75, 80, 65, 70, 85],
        'bb': [200, 210, 190, 250, 260, 230, 240, 250],
        'hbp': [10, 11, 9, 12, 13, 10, 11, 12],
        'sf': [5, 6, 4, 7, 8, 5, 6, 7],
        'r': [300, 320, 280, 400, 450, 380, 410, 460],
        'sb': [50, 55, 45, 70, 75, 60, 65, 70],
        'gidp': [30, 35, 25, 40, 45, 35, 40, 45],
        'batters': [30, 30, 30, 35, 35, 35, 32, 33],
        'sh': [50, 45, 55, 60, 50, 65, 55, 60],
        'e': [70, 65, 75, 80, 70, 85, 75, 80]
    }
    team_batting = pl.DataFrame(data)

# Print DataFrame
print("team_batting head:")
print(team_batting.head())
print("-" * 50)


# --- DPLYR/TIDYVERSE Operations in Polars Chains ---

# team_batting %>% arrange(team)
print("arrange(team):")
(
    team_batting.sort('team')
).pipe(print)
print("-" * 50)

# team_batting %>% arrange(team %>% desc())
print("arrange(team %>% desc()):")
(
    team_batting.sort('team', descending=True)
).pipe(print)
print("-" * 50)

# team_batting %>% arrange(team, year)
print("arrange(team, year):")
(
    team_batting.sort(['team', 'year'])
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982)
print("filter(year == 1982):")
(
    team_batting.filter(pl.col('year') == 1982)
).pipe(print)
print("-" * 50)

# team_batting[1:6, ] / team_batting %>% slice(1:6) (Polars is 0-based, exclusive end)
print("slice(1:6):")
(
    team_batting.slice(offset=0, length=6)
).pipe(print)
print("-" * 50)

# team_batting[sample(1:nrow(team_batting), 5), ] / team_batting %>% sample_n(5)
print("sample_n(5):")
(
    team_batting.sample(n=5)
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% arrange(hr %>% desc()) / arrange(-hr)
print("filter and arrange descending (hr):")
(
    team_batting.filter(pl.col('year') == 1982)
    .sort('hr', descending=True)
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% select(year, team, h, X2b, X3b, hr)
print("filter and select columns:")
(
    team_batting.filter(pl.col('year') == 1982)
    .select('year', 'team', 'h', 'X2b', 'X3b', 'hr')
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% relocate(year, .before = team)
print("relocate(year, .before = team):")
(
    team_batting.filter(pl.col('year') == 1982)
    .select(
        'year',  # Move 'year' to the front
        pl.exclude('year')
    )
    .select(
        'year',
        pl.exclude(['year', 'team']), # Exclude what we've already selected and 'team'
        'team', # Move 'team' after 'year'
        pl.all() # Select the rest of the columns
    )
).pipe(print)
# Note: Polars .select() handles column reordering. A precise .before/.after requires careful exclusion/re-selection.
# The following is a more direct Polars way for .before='team':
print("Polars direct .before='team' (showing key columns):")
(
    team_batting.filter(pl.col('year') == 1982)
    .select(
        pl.col('year').alias('temp_year'), # Alias to avoid name conflict
        pl.all()
    )
    .select(
        pl.col('temp_year').alias('year'),
        pl.col('team'),
        pl.exclude(['temp_year', 'team', 'year']) # Exclude the temp column and the moved columns
    )
    .select(pl.col('year', 'team').head(3), pl.col('g').head(3))
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% relocate(g, .after = year)
print("relocate(g, .after = year):")
(
    team_batting.filter(pl.col('year') == 1982)
    .select(
        'year',
        'g',
        pl.exclude('year', 'g')
    )
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% select(season = year, team, h, X2b, X3b, hr)
print("select with rename:")
(
    team_batting.filter(pl.col('year') == 1982)
    .select(
        pl.col('year').alias('season'),
        'team', 'h', 'X2b', 'X3b', 'hr'
    )
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% select(year, team, h, X2b, X3b, hr) %>% select(-X3b)
print("select and deselect (drop):")
(
    team_batting.filter(pl.col('year') == 1982)
    .select('year', 'team', 'h', 'X2b', 'X3b', 'hr')
    .drop('X3b')
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% select(bb:last_col())
# Polars uses slicing on the columns via string range (inclusive start/end)
print("select bb:last_col():")
(
    team_batting.filter(pl.col('year') == 1982)
    .select(pl.col('bb':))
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% select(2, 1, 7:10) (1-based index)
# Polars uses 0-based indexing for pl.select(pl.col.by_idx())
# 1-based columns 2, 1, 7:10 are 0-based columns 1, 0, 6:9
print("select by 1-based index (0-based in Polars):")
(
    team_batting.filter(pl.col('year') == 1982)
    .select(pl.col.by_idx([1, 0] + list(range(6, 10))))
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% select(year, team, h:hr)
print("select by column name range (h:hr):")
(
    team_batting.filter(pl.col('year') == 1982)
    .select('year', 'team', pl.col('h':'hr'))
).pipe(print)
print("-" * 50)

# team_batting %>% filter(year == 1982) %>% select(year, team, h:hr) %>% mutate(tb = h + X2b + 2 * X3b + 3 * hr)
print("select and mutate (with_columns):")
(
    team_batting.filter(pl.col('year') == 1982)
    .select('year', 'team', pl.col('h':'hr'))
    .with_columns(
        tb=(pl.col('h') + pl.col('X2b') + 2 * pl.col('X3b') + 3 * pl.col('hr'))
    )
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(avg = h / ab) %>% select(year, team, avg)
print("mutate and select:")
(
    team_batting.with_columns(avg=pl.col('h') / pl.col('ab'))
    .select('year', 'team', 'avg')
).pipe(print)
print("-" * 50)

# team_batting %>% transmute(year, team, avg = h / ab)
# transmute is a combination of with_columns and select
print("transmute (select with calculation):")
(
    team_batting.select(
        'year',
        'team',
        avg=pl.col('h') / pl.col('ab')
    )
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(avg = h / ab, .keep = 'used')
# Polars: calculate, then select only the new column and columns used in its creation ('h', 'ab')
print("mutate with .keep = 'used' (select used columns):")
(
    team_batting.with_columns(avg=pl.col('h') / pl.col('ab'))
    .select('h', 'ab', 'avg')
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(avg = h / ab, .keep = 'unused')
# Polars: calculate, then select the new column and columns NOT used ('h', 'ab')
print("mutate with .keep = 'unused' (select unused columns):")
(
    team_batting.with_columns(avg=pl.col('h') / pl.col('ab'))
    .select(pl.exclude('h', 'ab'), 'avg')
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(avg = h / ab, .before = g)
# .before is achieved via .select() reordering
print("mutate with .before = g:")
(
    team_batting.with_columns(avg=pl.col('h') / pl.col('ab'))
    .select(
        pl.exclude('avg', 'g'), # Exclude 'avg' and 'g'
        'avg',                 # Insert 'avg'
        'g',                   # Insert 'g'
        pl.all(),              # Include remaining (already included by pl.exclude)
    )
).pipe(print)
print("-" * 50)

# team_batting %>% group_by(year) %>% mutate(avg = sum(h) / sum(ab), .before = g)
# Calculating league AVG per year and assigning it back (Window Function)
print("group_by(year) %>% mutate(league_avg = sum(h)/sum(ab), .before = g):")
(
    team_batting.with_columns(
        league_avg=(pl.col('h').sum().over('year') / pl.col('ab').sum().over('year'))
    )
    .select(
        pl.exclude('league_avg', 'g'),
        pl.col('league_avg'),
        pl.col('g'),
        pl.all()
    )
).pipe(print)
print("-" * 50)

# team_batting %>% group_by(year) %>% summarise(avg = sum(h) / sum(ab))
print("group_by(year) %>% summarise(avg = sum(h) / sum(ab)):")
df_summarise = (
    team_batting.group_by('year')
    .agg(
        sum_h=pl.col('h').sum(),
        sum_ab=pl.col('ab').sum()
    )
    .with_columns(avg=pl.col('sum_h') / pl.col('sum_ab'))
    .select('year', 'avg') # Only select the result and group key
)
df_summarise.pipe(print)
print("-" * 50)

# team_batting %>% group_by(year) %>% summarise(avg = sum(h) / sum(ab), .groups = 'drop')
# Polars aggregation generally drops the grouping columns to become regular columns
print("summarise with .groups = 'drop': (Same as above)")
df_summarise.pipe(print)
print("-" * 50)

# team_batting %>% group_by(year) %>% summarise(avg = sum(h) / sum(ab), .groups = 'drop') %>% ggplot(aes(x = year, y = avg)) + geom_line()
# Plotting requires converting to Pandas/Matplotlib/Seaborn or using a Polars-compatible visual tool
# Example of conversion to Pandas for plotting:
# df_summarise.to_pandas().plot(x='year', y='avg', kind='line')
print("Plotting step (Polars requires conversion to plot):")
print(df_summarise.to_pandas().head())
print("-" * 50)

# team_batting %>% group_by(year) %>% summarise(avg = sum(h) / sum(ab), .groups = 'drop') %>% filter(year == 1999)
print("summarise and filter:")
(
    df_summarise.filter(pl.col('year') == 1982) # Using 1982 for dummy data
).pipe(print)
print("-" * 50)

# team_batting %>% group_by(year) %>% summarise(avg = sum(h) / sum(ab), .groups = 'drop') %>% arrange(-avg)
print("summarise and arrange descending (avg):")
(
    df_summarise.sort('avg', descending=True)
).pipe(print)
print("-" * 50)

# team_batting %>% group_by(year) %>% summarise(avg = sum(h) / sum(ab), .groups = 'drop') %>% filter(avg == max(avg))
print("summarise and filter for max avg:")
(
    df_summarise.filter(pl.col('avg') == pl.col('avg').max())
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(avg = h / ab, obp = ..., slg = ..., ops = ..., .before = g)
print("mutate multiple stats with .before = g:")
(
    team_batting.with_columns(
        avg=pl.col('h') / pl.col('ab'),
        obp=(pl.col('h') + pl.col('bb') + pl.col('hbp')) / (pl.col('ab') + pl.col('bb') + pl.col('hbp') + pl.col('sf')),
        slg=(pl.col('h') + pl.col('X2b') + 2 * pl.col('X3b') + 3 * pl.col('hr')) / pl.col('ab'),
        ops=pl.col('obp') + pl.col('slg')
    )
    .select(
        pl.exclude('avg', 'obp', 'slg', 'ops', 'g'),
        'avg', 'obp', 'slg', 'ops', 'g',
        pl.all()
    )
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(...) %>% filter(ops >= 0.7 & hr < 70)
print("mutate and filter by multiple conditions:")
df_full_stats_calc = team_batting.with_columns(
    avg=pl.col('h') / pl.col('ab'),
    obp=(pl.col('h') + pl.col('bb') + pl.col('hbp')) / (pl.col('ab') + pl.col('bb') + pl.col('hbp') + pl.col('sf')),
    slg=(pl.col('h') + pl.col('X2b') + 2 * pl.col('X3b') + 3 * pl.col('hr')) / pl.col('ab'),
    ops=pl.col('obp') + pl.col('slg')
)
(
    df_full_stats_calc.filter(
        (pl.col('ops') >= 0.7) & (pl.col('hr') < 70)
    ).select('year', 'team', 'ops', 'hr')
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(...) %>% filter(...) %>% summarise(count = n()) / tally()
print("summarise(count = n()) / tally():")
(
    df_full_stats_calc.filter(
        (pl.col('ops') >= 0.7) & (pl.col('hr') < 70)
    )
    .select(pl.count().alias('count')) # Tally/n() is a simple count
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(...) %>% filter(ops >= 0.7, hr < 70, year %in% 1991:2000)
print("filter by year range (inclusive):")
(
    df_full_stats_calc.filter(
        (pl.col('ops') >= 0.7) &
        (pl.col('hr') < 70) &
        (pl.col('year').is_between(1982, 1983)) # Use 1982:1983 for dummy data
    ).select('year', 'team', 'ops', 'hr')
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(...) %>% filter(...) %>% transmute(year, team, rg = r / g, sb = sb / g)
print("filter and transmute with calculated columns:")
(
    df_full_stats_calc.filter(
        (pl.col('ops') >= 0.7) & (pl.col('hr') < 70)
    )
    .select(
        'year',
        'team',
        rg=pl.col('r') / pl.col('g'),
        sb=pl.col('sb') / pl.col('g')
    )
).pipe(print)
print("-" * 50)

# team_batting %>% transmute(decades = if_else(year <= 1990, '1980', if_else(...)), g, sh)
# Polars uses pl.when().then().otherwise() for nested if_else/case_when
print("transmute with nested if_else (pl.when().then().otherwise()):")
(
    team_batting.select(
        decades=pl.when(pl.col('year') <= 1990).then(pl.lit('1980'))
                .when(pl.col('year') <= 2000).then(pl.lit('1990'))
                .when(pl.col('year') <= 2010).then(pl.lit('2000'))
                .otherwise(pl.lit('2010')),
        'g',
        'sh'
    )
).pipe(print)
print("-" * 50)

# team_batting %>% distinct(year) %>% mutate(decades = case_when(...))
print("distinct(year) and case_when (pl.when().then().otherwise()):")
(
    team_batting.select('year').unique()
    .with_columns(
        decades=pl.when(pl.col('year') <= 1990).then(pl.lit('1980'))
                .when(pl.col('year') <= 2000).then(pl.lit('1990'))
                .when(pl.col('year') <= 2010).then(pl.lit('2000'))
                .when(pl.col('year') <= 2020).then(pl.lit('2010'))
                .otherwise(pl.lit('Unknown'))
    )
).pipe(print)
print("-" * 50)

# team_batting %>% group_by(decades) %>% summarise(sh_mean = sum(sh) / sum(g))
print("group_by(decades) and summarize(sh_mean):")
(
    team_batting.with_columns(
        decades=pl.when(pl.col('year') <= 1990).then(pl.lit('1980'))
                .when(pl.col('year') <= 2000).then(pl.lit('1990'))
                .when(pl.col('year') <= 2010).then(pl.lit('2000'))
                .otherwise(pl.lit('2010'))
    )
    .group_by('decades')
    .agg(
        sh_mean=(pl.col('sh').sum() / pl.col('g').sum())
    )
).pipe(print)
print("-" * 50)

# team_batting %>% group_by(team) %>% summarise(gidp = sum(gidp)) %>% arrange(-gidp) %>% head(3)
print("group_by(team) and summarise, top 3:")
(
    team_batting.group_by('team')
    .agg(gidp=pl.col('gidp').sum())
    .sort('gidp', descending=True)
    .head(3)
).pipe(print)
print("-" * 50)

# team_batting %>% distinct(team)
print("distinct(team):")
(
    team_batting.select('team').unique()
).pipe(print)
print("-" * 50)

# team_batting %>% mutate(team_id = fct_collapse(team, ...), .before = year)
# fct_collapse/case_when mapping teams
team_map_expr = (
    pl.when(pl.col('team').is_in(['OB', '두산'])).then(pl.lit('두산'))
    .when(pl.col('team').is_in(['히어로즈', '넥센', '키움'])).then(pl.lit('키움'))
    .when(pl.col('team').is_in(['빙그레', '한화'])).then(pl.lit('한화'))
    .when(pl.col('team').is_in(['삼미', '삼미·청보', '청보', '태평양'])).then(pl.lit('현대'))
    .when(pl.col('team').is_in(['해태', '해태·KIA', 'KIA'])).then(pl.lit('KIA'))
    .when(pl.col('team').is_in(['LG', 'MBC'])).then(pl.lit('LG'))
    .otherwise(pl.col('team')) # Keep original name if no match
).alias('team_id')

print("mutate with fct_collapse (pl.when) and .before = year:")
(
    team_batting.with_columns(team_map_expr)
    .select(
        'team_id',
        'year',
        'team',
        pl.exclude('team_id', 'year', 'team')
    )
).select('team_id', 'year', 'team').pipe(print) # Print only relevant cols
print("-" * 50)

# team_batting %>% mutate(team_id = fct_collapse(...)) %>% group_by(team_id) %>% summarise(gidp = sum(gidp)) %>% arrange(-gidp)
print("fct_collapse, group_by, summarise, arrange:")
(
    team_batting.with_columns(team_map_expr)
    .group_by('team_id')
    .agg(gidp=pl.col('gidp').sum())
    .sort('gidp', descending=True)
).pipe(print)
print("-" * 50)

# team_batting %>% group_by(year) %>% summarise(across(-team, ~sum(.x) / sum(g)), .groups = 'drop')
# across is done with pl.sum().over() or with custom aggregation
print("group_by(year) %>% summarise(across(-team, ~sum(.x) / sum(g))):")
# Identify all columns except 'team'
sum_cols = [c for c in team_batting.columns if c not in ['year', 'team']]

# Aggregate by calculating sum(col) / sum(g) for each column
(
    team_batting.group_by('year')
    .agg(
        [
            (pl.col(c).sum() / pl.col('g').sum()).alias(f'{c}_per_g')
            for c in sum_cols
        ]
    )
).pipe(print)
print("-" * 50)


# --- String/Lag/Lead Operations (Using Dummy kovo_team data) ---
try:
    kovo_team = pl.read_csv('kovo_team.csv')
except pl.exceptions.ComputeError:
    print("kovo_team.csv not found. Skipping remaining Kovo data processing.")
    exit()

# kovo_team %>% mutate(시즌 = 시즌 %>% str_sub(-4))
print("mutate(시즌 = 시즌 %>% str_sub(-4)):")
(
    kovo_team.with_columns(
        시즌_이름=pl.col('시즌'),
        시즌=pl.col('시즌').str.slice(offset=-4, length=4)
    )
).select('시즌_이름', '시즌').unique().pipe(print)
print("-" * 50)


# kovo_team %>% select(시즌, 팀, contains('공격종합'))
print("select(..., contains('공격종합')):")
(
    kovo_team.select(
        '시즌', '팀', pl.col('*').str.contains('공격종합')
    )
).pipe(print)
print("-" * 50)

# kovo_team %>% select(시즌, 팀, ends_with('세트당_평균')) %>% rename_with(~str_replace(., '_세트당_평균', ''))
print("rename_with (~str_replace(., '_세트당_평균', '')):")
(
    kovo_team.select(
        '시즌', '팀', pl.col('*').str.ends_with('세트당_평균')
    )
    .rename({c: c.replace('_세트당_평균', '') for c in kovo_team.columns if c.endswith('세트당_평균')})
).pipe(print)
print("-" * 50)

# kovo_team %>% group_by(남녀부, 시즌) %>% summarise(리시브_효율 = (sum(리시브_정확) - sum(리시브_실패)) / sum(리시브_시도))
df_rcv_efficiency = (
    kovo_team.group_by('남녀부', '시즌')
    .agg(
        리시브_효율=(pl.col('리시브_정확').sum() - pl.col('리시브_실패').sum()) / pl.col('리시브_시도').sum()
    )
    .sort('남녀부', '시즌') # Sort is required before lag/lead
)

# kovo_team %>% group_by(남녀부, 시즌) %>% summarise(...) %>% mutate(전_시즌 = lag(리시브_효율))
print("mutate(전_시즌 = lag(리시브_효율)) (Window Function):")
(
    df_rcv_efficiency.with_columns(
        전_시즌=pl.col('리시브_효율').shift(1).over('남녀부')
    )
).pipe(print)
print("-" * 50)

# kovo_team %>% group_by(남녀부, 시즌) %>% summarise(...) %>% mutate(다음_시즌 = lead(리시브_효율))
print("mutate(다음_시즌 = lead(리시브_효율)) (Window Function):")
(
    df_rcv_efficiency.with_columns(
        다음_시즌=pl.col('리시브_효율').shift(-1).over('남녀부')
    )
).pipe(print)
print("-" * 50)

# kovo_team %>% group_by(남녀부, 시즌) %>% summarise(...) %>% mutate(차이 = 리시브_효율 - lag(리시브_효율))
df_diff = (
    df_rcv_efficiency.with_columns(
        차이=pl.col('리시브_효율') - pl.col('리시브_효율').shift(1).over('남녀부')
    )
)
print("mutate(차이 = 리시브_효율 - lag(리시브_효율)):")
df_diff.pipe(print)
print("-" * 50)

# kovo_team %>% group_by(남녀부, 시즌) %>% summarise(...) %>% mutate(...) %>% summarise(차이_평균 = mean(차이, na.rm = TRUE))
print("summarise(차이_평균 = mean(차이, na.rm = TRUE)):")
(
    df_diff.group_by('남녀부')
    .agg(차이_평균=pl.col('차이').mean())
).pipe(print)
print("-" * 50)

# kovo_team %>% group_by(남녀부, 시즌) %>% summarise(...) %>% mutate(...) %>% drop_na() %>% arrange(차이)
print("drop_na() %>% arrange(차이):")
(
    df_diff.drop_nulls('차이')
    .sort('차이')
).pipe(print)