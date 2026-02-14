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
This script is a Python conversion of the R script chapter_12.R.
It focuses on t-tests, their relationship with permutation tests, and statistical power.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_boxplot, geom_histogram, geom_vline, facet_grid, geom_density
from scipy.stats import ttest_ind, ttest_1samp, t
from statsmodels.stats.power import ttest_power

# %%
np.random.seed(1234)

# %%
# Load and prepare data
try:
    uefa_big5_match_results = pd.read_csv('R/19_20_uefa_big_5.csv')
except FileNotFoundError:
    print("Could not find 'R/19_20_uefa_big_5.csv'.")
    uefa_big5_match_results = pd.DataFrame()

# %%
if not uefa_big5_match_results.empty:
    uefa_big5_match_results['장소'] = pd.Categorical(uefa_big5_match_results['장소'], categories=['안방', '방문'], ordered=True)
    uefa_big5_match_results['시기'] = pd.Categorical(uefa_big5_match_results['시기'], categories=['BC', 'AC'], ordered=True)

    uefa_big5_match_results_period = uefa_big5_match_results[
        (uefa_big5_match_results['장소'] == '안방') &
        (uefa_big5_match_results['리그'] != '리그1')
    ]
    uefa_big5_results_period = uefa_big5_match_results_period.groupby(['팀', '시기'])['승리'].mean().reset_index()
    uefa_big5_results_period = uefa_big5_results_period.rename(columns={'승리': '승률'})

    # Independent samples t-test
    ac_rates = uefa_big5_results_period[uefa_big5_results_period['시기'] == 'AC']['승률']
    bc_rates = uefa_big5_results_period[uefa_big5_results_period['시기'] == 'BC']['승률']
    
    # Welch's t-test (var.equal = False)
    t_stat, p_val = ttest_ind(ac_rates, bc_rates, equal_var=False, alternative='less')
    print(f"Welch's t-test: statistic={t_stat:.3f}, p-value={p_val:.3f}")

    # Student's t-test (var.equal = True)
    t_stat_student, p_val_student = ttest_ind(ac_rates, bc_rates, equal_var=True, alternative='less')
    print(f"Student's t-test: statistic={t_stat_student:.3f}, p-value={p_val_student:.3f}")

    # Paired t-test
    paired_data = uefa_big5_results_period.pivot(index='팀', columns='시기', values='승률').reset_index()
    paired_data = paired_data.dropna(subset=['AC', 'BC'])
    paired_data['diff'] = paired_data['AC'] - paired_data['BC']
    
    t_stat_paired, p_val_paired = ttest_1samp(paired_data['diff'], popmean=0, alternative='less')
    print(f"
Paired t-test: statistic={t_stat_paired:.3f}, p-value={p_val_paired:.3f}")

    # Power analysis
    # First, find the parameters needed
    delta = paired_data['diff'].mean()
    sd_diff = paired_data['diff'].std()
    effect_size = delta / sd_diff # Cohen's d
    
    power = 0.8
    alpha = 0.05
    
    # Calculate required sample size
    required_n = ttest_power(effect_size=effect_size, nobs=None, alpha=alpha, power=power, alternative='smaller')
    print(f"
Required sample size for power=0.8: {np.ceil(required_n)}")
    
    # Using parameters from the R script for NBA data
    # power.t.test(delta = .106, sd = .158, ...)
    nba_delta = 0.106
    nba_sd = 0.158
    nba_effect_size = nba_delta / nba_sd
    required_n_nba = ttest_power(effect_size=nba_effect_size, nobs=None, alpha=alpha, power=power, alternative='one-sided')
    print(f"Required sample size for NBA data: {np.ceil(required_n_nba)}")
    
    # Simulating H0 and H1 distributions for NBA data
    try:
        nba_match_results = pd.read_csv('R/19_20_nba.csv')
    except FileNotFoundError:
        print("
Could not find 'R/19_20_nba.csv'. Skipping H0/H1 simulation.")
        nba_match_results = pd.DataFrame()

    if not nba_match_results.empty:
        nba_bc = nba_match_results[nba_match_results['시기'] == 'BC'].copy()
        nba_bc['장소'] = pd.Categorical(nba_bc['장소'], categories=['안방', '방문'], ordered=True)
        
        nba_bc_summary = nba_bc.groupby(['팀', '장소'])['승리'].mean().reset_index()
        nba_bc_summary = nba_bc_summary.rename(columns={'승리':'승률'})

        # H0 simulation (permutation)
        h0_diffs = []
        for _ in range(1000):
            permuted_labels = np.random.permutation(nba_bc_summary['장소'])
            permuted_df = nba_bc_summary.copy()
            permuted_df['장소'] = permuted_labels
            permuted_means = permuted_df.groupby('장소')['승률'].mean()
            h0_diffs.append(permuted_means['안방'] - permuted_means['방문'])

        nba_simulation_h0 = pd.DataFrame({'stat': h0_diffs, 'type': 'h0'})

        # H1 simulation (bootstrap)
        nba_bc_wide = nba_bc_summary.pivot(index='팀', columns='장소', values='승률').reset_index().dropna()
        nba_bc_wide['차이'] = nba_bc_wide['안방'] - nba_bc_wide['방문']
        
        h1_means = []
        for _ in range(1000):
            bootstrap_sample = nba_bc_wide['차이'].sample(frac=1, replace=True)
            h1_means.append(bootstrap_sample.mean())
        
        nba_simulation_h1 = pd.DataFrame({'stat': h1_means, 'type': 'h1'})

        # Combine and plot
        nba_simulations = pd.concat([nba_simulation_h0, nba_simulation_h1], ignore_index=True)
        
        # Critical value for one-sided test at alpha=0.05
        critical_value = nba_simulation_h0['stat'].quantile(0.95)
        
        power_simulated = (nba_simulation_h1['stat'] > critical_value).mean()
        print(f"
Simulated Power: {power_simulated:.3f}")
        
        p = (ggplot(nba_simulations, aes(x='stat', fill='type')) +
             geom_density(alpha=0.5) +
             geom_vline(xintercept=critical_value, linetype='dashed', size=1))
        # print(p)

# %%
print("
Conversion of chapter_12.R to Python is complete.")
