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
This script is a Python conversion of the R script chapter_13.R.
It covers the Chi-squared test for independence and goodness-of-fit using scipy.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_col, facet_grid, scale_x_continuous, geom_text
from scipy.stats import chi2_contingency, chisquare, chi2

# %%
np.random.seed(1234)

# %%
# Load and prepare tennis data
try:
    tennis_big3_results = pd.read_csv(tennis_big3_results.csv')
    
    # Clean column names (like janitor::make_clean_names)
    tennis_big3_results.columns = tennis_big3_results.columns.str.lower().str.replace('[. %]', '_', regex=True).str.replace('__', '_')
    
    # Clean data
    tennis_big3_results['surface'] = tennis_big3_results['surface'].str.lower()
    tennis_big3_results['w_l'] = tennis_big3_results['w_l'].str.lower()

# %%
except FileNotFoundError:
    print("Could not find tennis_big3_results.csv'.")
    tennis_big3_results = pd.DataFrame()

# %%
if not tennis_big3_results.empty:
    # Chi-squared Test of Independence: Surface vs Win/Loss for Nadal
    nadal_data = tennis_big3_results[
        (tennis_big3_results['player'] == 'Rafael Nadal') &
        (tennis_big3_results['surface'].isin(['clay', 'grass', 'hard'])) &
        (tennis_big3_results['w_l'].isin(['w', 'l']))
    ].copy()

    # Create a contingency table
    contingency_table = pd.crosstab(nadal_data['surface'], nadal_data['w_l'])
    print("Contingency Table (Nadal):")
    print(contingency_table)

    # Perform the Chi-squared test
    chi2_stat, p_val, dof, expected = chi2_contingency(contingency_table)
    print(f"
Chi-squared Test for Nadal:")
    print(f"Statistic: {chi2_stat:.3f}")
    print(f"P-value: {p_val}")
    print(f"Degrees of Freedom: {dof}")
    print("Expected Frequencies:")
    print(pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns))
    
    # Visualize the theoretical distribution
    x = np.linspace(chi2.ppf(0.01, dof), chi2.ppf(0.99, dof), 100)
    chi2_df = pd.DataFrame({'x': x, 'y': chi2.pdf(x, dof)})
    p = (ggplot(chi2_df, aes(x='x', y='y')) +
         geom_line() +
         geom_vline(xintercept=chi2_stat, color='red', linetype='dashed'))
    # print(p)

# %%
# Chi-squared Goodness-of-Fit Test: KBO Player Birth Months
try:
    kbo_profile = pd.read_csv(kbo_players_profiles.csv')
except FileNotFoundError:
    print("
Could not find kbo_players_profiles.csv'.")
    kbo_profile = pd.DataFrame()

# %%
if not kbo_profile.empty:
    kbo_profile_korean = kbo_profile[kbo_profile['외국인'] != 1].copy()
    kbo_profile_korean['생일'] = pd.to_datetime(kbo_profile_korean['생년월일'], format='%Y%m%d', errors='coerce')
    kbo_profile_korean['월'] = kbo_profile_korean['생일'].dt.month
    
    # Get observed frequencies
    observed_counts = kbo_profile_korean['월'].value_counts().sort_index()
    print("
Observed Birth Month Counts:")
    print(observed_counts)
    
    # Expected frequencies (uniform distribution)
    total_players = observed_counts.sum()
    expected_prob = 1/12
    expected_counts = total_players * expected_prob
    
    # The chisquare function can take probabilities directly
    gof_stat, gof_p_val = chisquare(f_obs=observed_counts) # default p is uniform
    print(f"
Goodness-of-Fit Test for Birth Months:")
    print(f"Statistic: {gof_stat:.3f}")
    print(f"P-value: {gof_p_val:.3f}")

    # Test for quarterly distribution
    def get_quarter(month):
        if 3 <= month < 6:
            return '1'
        elif 6 <= month < 9:
            return '2'
        elif 9 <= month < 12:
            return '3'
        else:
            return '4'
            
    kbo_profile_korean['분기'] = kbo_profile_korean['월'].apply(get_quarter)
    observed_quarter_counts = kbo_profile_korean['분기'].value_counts().sort_index()
    print("
Observed Birth Quarter Counts:")
    print(observed_quarter_counts)

    gof_stat_q, gof_p_val_q = chisquare(f_obs=observed_quarter_counts)
    print(f"
Goodness-of-Fit Test for Birth Quarters:")
    print(f"Statistic: {gof_stat_q:.3f}")
    print(f"P-value: {gof_p_val_q:.3f}")


# %%
print("
Conversion of chapter_13.R to Python is complete.")

