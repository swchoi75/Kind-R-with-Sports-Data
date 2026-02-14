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
This script is a Python conversion of the R script chapter_14.R.
It introduces the F-statistic and Analysis of Variance (ANOVA).
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_histogram, geom_density, geom_function, geom_boxplot, geom_vline
from scipy.stats import f, f_oneway
import statsmodels.api as sm
from statsmodels.formula.api import ols

# %%
np.random.seed(1234)

# %%
# Manual ANOVA calculation demonstration
volleyball_status = pd.DataFrame({
    '항목': ['스파이크', '디그', '서브', '리시브', '블로킹', '2단_연결'],
    '능력치': [30, 75, 45, 80, 25, 70]
})
volleyball_status['카테고리'] = ['공격', '수비', '공격', '수비', '공격', '수비']

# %%
grand_mean = volleyball_status['능력치'].mean()
volleyball_status['편차'] = volleyball_status['능력치'] - grand_mean

# %%
# Add group means
group_means = volleyball_status.groupby('카테고리')['능력치'].transform('mean')
volleyball_status['카테고리_평균'] = group_means

# %%
# Sum of Squares Total (SST)
volleyball_status['편차_제곱'] = volleyball_status['편차'] ** 2
SST = volleyball_status['편차_제곱'].sum()

# %%
# Sum of Squares Within (SSW)
volleyball_status['능력치_카테고리_제곱'] = (volleyball_status['능력치'] - volleyball_status['카테고리_평균']) ** 2
SSW = volleyball_status['능력치_카테고리_제곱'].sum()

# %%
# Sum of Squares Between (SSB)
volleyball_status['카테고리_전체_제곱'] = (volleyball_status['카테고리_평균'] - grand_mean) ** 2
SSB = volleyball_status['카테고리_전체_제곱'].sum()

# %%
print("Manual ANOVA calculations:")
print(f"SST (Total): {SST:.2f}")
print(f"SSB (Between groups): {SSB:.2f}")
print(f"SSW (Within groups): {SSW:.2f}")
print(f"Check (SSB + SSW): {SSB + SSW:.2f}")

# %%
# Degrees of freedom
n_groups = volleyball_status['카테고리'].nunique()
n_total = len(volleyball_status)
df_between = n_groups - 1
df_within = n_total - n_groups

# %%
# F-statistic
F_stat_manual = (SSB / df_between) / (SSW / df_within)
print(f"Manual F-statistic: {F_stat_manual:.2f}")

# %%
# --- ANOVA on NBA Draft Data ---
try:
    nba_players = pd.read_csv(nba_draft_data.csv')
except FileNotFoundError:
    print("
Could not find nba_draft_data.csv'.")
    nba_players = pd.DataFrame()

# %%
if not nba_players.empty:
    nba_players_filtered = nba_players[nba_players['g'] > 67].copy()
    
    pos_map = {'C-PF': 'PF', 'PF-SF': 'PF', 'PG-SG': 'SG', 'SG-PG': 'SG'}
    nba_players_filtered['pos'] = nba_players_filtered['pos'].replace(pos_map)
    
    # Normalize stats by games played
    stats_to_normalize = ['mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']
    for stat in stats_to_normalize:
        if stat in nba_players_filtered.columns:
            nba_players_filtered[stat] = nba_players_filtered[stat] / nba_players_filtered['g']
    
    nba_position = nba_players_filtered[['pos'] + stats_to_normalize].copy()

    p = (ggplot(nba_position, aes(x='pos', y='pts')) + geom_boxplot())
    # print(p)

    # Perform one-way ANOVA using scipy
    # First, get the 'pts' for each position as a separate series
    positions = nba_position['pos'].unique()
    grouped_pts = [nba_position[nba_position['pos'] == pos]['pts'] for pos in positions]
    
    F_stat, p_val = f_oneway(*grouped_pts)
    print(f"
One-way ANOVA for PTS by POS:")
    print(f"F-statistic: {F_stat:.3f}")
    print(f"P-value: {p_val}")

    # Visualize theoretical F-distribution
    dfn = len(positions) - 1
    dfd = len(nba_position) - len(positions)
    x = np.linspace(f.ppf(0.01, dfn, dfd), f.ppf(0.99, dfn, dfd), 100)
    f_df = pd.DataFrame({'x': x, 'y': f.pdf(x, dfn, dfd)})
    
    p_fdist = (ggplot(f_df, aes(x='x', y='y')) +
               geom_line() +
               geom_vline(xintercept=F_stat, color='red', linetype='dashed'))
    # print(p_fdist)

    # Connection to Linear Regression using statsmodels
    model = ols('pts ~ pos', data=nba_position).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print("
ANOVA table from Linear Model:")
    print(anova_table)

# %%
print("
Conversion of chapter_14.R to Python is complete.")
