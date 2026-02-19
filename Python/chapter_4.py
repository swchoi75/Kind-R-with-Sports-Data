# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
# ---

# %%
"""
This script is a Python conversion of the R script chapter_4.R.
It uses the pandas library for data manipulation, which is the Python equivalent of dplyr.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_line

# %%
# Load the data
try:
    team_batting = pd.read_csv(kbo_team_batting.csv')
except FileNotFoundError:
    print("Could not find kbo_team_batting.csv'.")
    team_batting = pd.DataFrame()

# %%
if not team_batting.empty:
    print(team_batting)

    # arrange(team)
    print(team_batting.sort_values(by='team'))

    # arrange(desc(team))
    print(team_batting.sort_values(by='team', ascending=False))

    # arrange(team, year)
    print(team_batting.sort_values(by=['team', 'year']))

    # filter(year == 1982)
    print(team_batting[team_batting['year'] == 1982])

    # slice(1:6)
    print(team_batting.iloc[0:6])

    # sample_n(5)
    print(team_batting.sample(n=5))

    # filter(year == 1982) %>% arrange(desc(hr))
    print(team_batting[team_batting['year'] == 1982].sort_values(by='hr', ascending=False))

    # select(year, team, h, X2b, X3b, hr)
    print(team_batting[team_batting['year'] == 1982][['year', 'team', 'h', 'X2b', 'X3b', 'hr']])

    # relocate(g, .after = year)
    cols = list(team_batting.columns)
    cols.insert(cols.index('year') + 1, cols.pop(cols.index('g')))
    print(team_batting[team_batting['year'] == 1982][cols])

    # select(season = year, ...) -> rename
    print(team_batting[team_batting['year'] == 1982].rename(columns={'year': 'season'})[['season', 'team', 'h', 'X2b', 'X3b', 'hr']])

    # select(-X3b) -> drop
    print(team_batting[team_batting['year'] == 1982][['year', 'team', 'h', 'X2b', 'X3b', 'hr']].drop(columns='X3b'))

    # select(bb:last_col())
    print(team_batting[team_batting['year'] == 1982].loc[:, 'bb':])
    
    # select(2, 1, 7:10) -> iloc
    print(team_batting[team_batting['year'] == 1982].iloc[:, [1, 0, 6, 7, 8, 9]])

    # select(h:hr)
    print(team_batting[team_batting['year'] == 1982].loc[:, 'h':'hr'])

    # mutate(tb = ...)
    print(team_batting[team_batting['year'] == 1982].loc[:, 'h':'hr'].assign(tb=lambda df: df['h'] + df['X2b'] + 2 * df['X3b'] + 3 * df['hr']))

    # transmute(...)
    print(team_batting.assign(avg=lambda df: df['h'] / df['ab'])[['year', 'team', 'avg']])

    # group_by and summarise
    print(team_batting.groupby('year').apply(lambda df: pd.Series({'avg': df['h'].sum() / df['ab'].sum()})).reset_index())
    
    # plotting with plotnine
    avg_by_year = team_batting.groupby('year').apply(lambda df: pd.Series({'avg': df['h'].sum() / df['ab'].sum()})).reset_index()
    p = (ggplot(avg_by_year, aes(x='year', y='avg')) + geom_line())
    # print(p)

    # Complex chain of operations
    print(team_batting.assign(
        avg=lambda df: df['h'] / df['ab'],
        obp=lambda df: (df['h'] + df['bb'] + df['hbp']) / (df['ab'] + df['bb'] + df['hbp'] + df['sf']),
        slg=lambda df: (df['h'] + df['X2b'] + 2 * df['X3b'] + 3 * df['hr']) / df['ab']
    ).assign(ops=lambda df: df['obp'] + df['slg']))
    
    # case_when -> np.select
    conditions = [
        team_batting['year'] <= 1990,
        team_batting['year'] <= 2000,
        team_batting['year'] <= 2010
    ]
    choices = ['1980', '1990', '2000']
    team_batting['decades'] = np.select(conditions, choices, default='2010')
    print(team_batting[['year', 'decades']])

    # distinct
    print(pd.DataFrame({'value': [1, 1, 3, 3, 3, 3, 5, 5, 5, 5, 5, 5]}).drop_duplicates())

    # fct_collapse -> replace
    team_mapping = {
        'OB': '두산', '두산': '두산',
        '히어로즈': '키움', '넥센': '키움', '키움': '키움',
        '빙그레': '한화', '한화': '한화',
        '삼미': '현대', '삼미·청보': '현대', '청보': '현대', '태평양': '현대',
        '해태': 'KIA', '해태·KIA': 'KIA', 'KIA': 'KIA',
        'LG': 'LG', 'MBC': 'LG'
    }
    team_batting['team_id'] = team_batting['team'].replace(team_mapping)
    print(team_batting.groupby('team_id')['gidp'].sum().sort_values(ascending=False))

    # across equivalent
    print(team_batting.groupby('year').agg({
        'g': 'sum', 'ab': 'sum', 'r': 'sum', 'h': 'sum', # etc. for all columns except team
    }))

    # fct_lump
    # pandas doesn't have a direct equivalent of fct_lump.
    # It can be implemented with value_counts and masking.
    
    try:
        kovo_team = pd.read_csv(kovo_team.csv')
    except FileNotFoundError:
        print("Could not find kovo_team.csv'.")
        kovo_team = pd.DataFrame()
        
    if not kovo_team.empty:
        # str_sub
        print('volleyball'[0])
        print('volleyball'[1])
        print('volleyball'[0:2])
        print('volleyball'[-4:])

        kovo_team['시즌_이름'] = kovo_team['시즌']
        kovo_team['시즌'] = kovo_team['시즌'].str.slice(-4)
        print(kovo_team)
        
        # select with contains, starts_with, ends_with
        print(kovo_team[['시즌', '팀'] + [c for c in kovo_team.columns if '공격종합' in c]])
        print(kovo_team[[c for c in kovo_team.columns if not '_' in c]])
        print(kovo_team[['시즌', '팀'] + [c for c in kovo_team.columns if c.startswith('세트')]])
        print(kovo_team[['시즌', '팀'] + [c for c in kovo_team.columns if c.endswith('세트당_평균')]])
        
        # rename_with
        df_to_rename = kovo_team[['시즌', '팀'] + [c for c in kovo_team.columns if c.endswith('세트당_평균')]]
        renamed_df = df_to_rename.rename(columns=lambda c: c.replace('_세트당_평균', ''))
        print(renamed_df)
        
        # lag/lead -> shift
        reception_eff = kovo_team.groupby(['남녀부', '시즌']).apply(
            lambda df: (df['리시브_정확'].sum() - df['리시브_실패'].sum()) / df['리시브_시도'].sum()
        ).rename('리시브_효율').reset_index()
        
        reception_eff['전_시즌'] = reception_eff.groupby('남녀부')['리시브_효율'].shift(1)
        reception_eff['다음_시즌'] = reception_eff.groupby('남녀부')['리시브_효율'].shift(-1)
        print(reception_eff)
        
        reception_eff['차이'] = reception_eff['리시브_효율'] - reception_eff['전_시즌']
        print(reception_eff.groupby('남녀부')['차이'].mean())
        print(reception_eff.dropna(subset=['차이']).groupby('남녀부')['차이'].mean())

# %%
print("Conversion of chapter_4.R to Python is complete.")

