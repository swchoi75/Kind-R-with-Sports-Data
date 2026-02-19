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
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
"""
This script is a Python conversion of the R script chapter_11.R.
It demonstrates hypothesis testing using permutation tests.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_boxplot, geom_histogram, geom_vline, annotate
from scipy.stats import ttest_ind

# %%
np.random.seed(1234)

# %%
# Load data
try:
    uefa_big5_match_results = pd.read_csv('19_20_uefa_big_5.csv')
except FileNotFoundError:
    print("Could not find 19_20_uefa_big_5.csv.")
    uefa_big5_match_results = pd.DataFrame()

# %%
if not uefa_big5_match_results.empty:
    # Prepare data
    uefa_big5_match_results['장소'] = pd.Categorical(uefa_big5_match_results['장소'], categories=['안방', '방문'], ordered=True)
    uefa_big5_match_results['시기'] = pd.Categorical(uefa_big5_match_results['시기'], categories=['BC', 'AC'], ordered=True)
    
    uefa_big5_results = uefa_big5_match_results.groupby(['팀', '장소'])['승리'].mean().reset_index()
    uefa_big5_results = uefa_big5_results.rename(columns={'승리': '승률'})

    p = (ggplot(uefa_big5_results, aes(x='장소', y='승률')) + geom_boxplot())
    # print(p)

    # Observed difference in means
    obs_means = uefa_big5_results.groupby('장소')['승률'].mean()
    obs_diff = obs_means['안방'] - obs_means['방문']
    print(f"Observed difference in mean win rate (Home - Away): {obs_diff:.3f}")

    # Permutation Test
    n_reps = 1000
    null_diffs = []
    for _ in range(n_reps):
        # Permute the '장소' labels
        permuted_labels = np.random.permutation(uefa_big5_results['장소'])
        permuted_df = uefa_big5_results.copy()
        permuted_df['장소'] = permuted_labels
        
        # Calculate the difference in means for the permuted data
        permuted_means = permuted_df.groupby('장소')['승률'].mean()
        null_diffs.append(permuted_means['안방'] - permuted_means['방문'])

    uefa_big5_results_null = pd.DataFrame({'stat': null_diffs})

    # Visualize the null distribution
    p_null = (ggplot(uefa_big5_results_null, aes(x='stat')) +
              geom_histogram(binwidth=0.01, fill='gray75', color='white'))
    # print(p_null)

    # Add observed statistic to the plot
    p_null_with_obs = p_null + geom_vline(xintercept=obs_diff, color='#53bfd4', size=1)
    # print(p_null_with_obs)

    # Calculate p-value
    # For 'greater' direction as the observed diff is positive
    p_value = (uefa_big5_results_null['stat'] >= obs_diff).mean()
    print(f"P-value (one-sided, greater): {p_value}")

    # For two-sided test
    p_value_two_sided = (np.abs(uefa_big5_results_null['stat']) >= np.abs(obs_diff)).mean()
    print(f"P-value (two-sided): {p_value_two_sided}")

    # Shade p-value area
    p_shaded = (p_null_with_obs + 
                annotate("rect", xmin=obs_diff, xmax=np.inf, ymin=-np.inf, ymax=np.inf, fill="#53bfd4", alpha=0.2))
    # print(p_shaded)

    # --- Part 2: Analyzing effect of COVID-19 (BC vs AC) ---
    uefa_big5_match_results_period = uefa_big5_match_results[
        (uefa_big5_match_results['장소'] == '안방') & 
        (uefa_big5_match_results['리그'] != '리그1')
    ]
    uefa_big5_results_period = uefa_big5_match_results_period.groupby(['팀', '시기'])['승리'].mean().reset_index()
    uefa_big5_results_period = uefa_big5_results_period.rename(columns={'승리': '승률'})

    # Observed difference
    obs_means_period = uefa_big5_results_period.groupby('시기')['승률'].mean()
    obs_diff_period = obs_means_period['AC'] - obs_means_period['BC']
    print(f"Observed difference in mean win rate (AC - BC): {obs_diff_period:.3f}")

    # T-test comparison
    ac_rates = uefa_big5_results_period[uefa_big5_results_period['시기'] == 'AC']['승률']
    bc_rates = uefa_big5_results_period[uefa_big5_results_period['시기'] == 'BC']['승률']
    
    # Using 'less' alternative because obs_diff is negative, so we test if AC < BC
    t_stat, p_val_ttest = ttest_ind(ac_rates, bc_rates, equal_var=False, alternative='less')
    print(f"T-test result: statistic={t_stat:.3f}, p-value={p_val_ttest:.3f}")


# %%
print("Conversion of chapter_11.R to Python is complete.")

