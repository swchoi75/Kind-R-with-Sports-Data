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
This script is a Python conversion of the R script chapter_15.R.
It covers correlation and simple linear regression using scipy and statsmodels.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, geom_smooth, geom_hline, geom_qq, geom_qq_line
from scipy.stats import pearsonr, shapiro
import statsmodels.api as sm
from statsmodels.formula.api import ols

# %%
np.random.seed(1234)

# %%
# --- Correlation ---
try:
    batting_2020 = pd.read_csv(2020_kbo_team_batting.csv')
except FileNotFoundError:
    print("Could not find 2020_kbo_team_batting.csv'.")
    batting_2020 = pd.DataFrame()

# %%
if not batting_2020.empty:
    # Manual correlation calculation
    batting_2020['runs_z_score'] = (batting_2020['runs'] - batting_2020['runs'].mean()) / batting_2020['runs'].std()
    batting_2020['avg_z_score'] = (batting_2020['avg'] - batting_2020['avg'].mean()) / batting_2020['avg'].std()
    correlation_manual = (batting_2020['runs_z_score'] * batting_2020['avg_z_score']).sum() / (len(batting_2020) - 1)
    print(f"Manually calculated correlation: {correlation_manual:.3f}")

    # Using scipy.stats.pearsonr
    corr, p_value = pearsonr(batting_2020['runs'], batting_2020['avg'])
    print(f"Correlation from scipy: {corr:.3f}, p-value: {p_value:.3f}")

    # --- Simple Linear Regression ---
    # Using statsmodels for regression (equivalent to R's lm)
    model = ols('runs ~ avg', data=batting_2020).fit()

    # Get a summary similar to R's summary(lm_fit)
    print("
--- Linear Model Summary (runs ~ avg) ---")
    print(model.summary())

    # Get coefficients (equivalent to broom::tidy)
    print("
Coefficients:")
    print(model.params)

    # Get model-level stats (equivalent to broom::glance)
    print("
Model Fit:")
    print(f"R-squared: {model.rsquared:.3f}")
    print(f"Adjusted R-squared: {model.rsquared_adj:.3f}")
    print(f"F-statistic: {model.fvalue:.3f}")

    # Get observation-level stats (equivalent to broom::augment)
    augmented_df = batting_2020.copy()
    augmented_df['.fitted'] = model.fittedvalues
    augmented_df['.resid'] = model.resid
    print("
Augmented Dataframe (head):")
    print(augmented_df[['team', 'runs', 'avg', '.fitted', '.resid']].head())

    # Plot with regression line
    p = (ggplot(batting_2020, aes(x='avg', y='runs')) +
         geom_point() +
         geom_smooth(method='lm', se=False))
    # print(p)

    # --- Regression Diagnostics ---
    # Residuals vs. predictor plot
    p_resid = (ggplot(augmented_df, aes(x='avg', y='.resid')) +
               geom_point() +
               geom_hline(yintercept=0, linetype='dashed') +
               geom_smooth())
    # print(p_resid)

    # Q-Q plot for residuals
    # statsmodels.api.qqplot can be used for a quick plot, but we use plotnine for consistency
    p_qq = (ggplot(augmented_df, aes(sample='.resid')) +
            geom_qq() +
            geom_qq_line())
    # print(p_qq)
    
    # Shapiro-Wilk test for normality of residuals
    shapiro_stat, shapiro_p = shapiro(augmented_df['.resid'])
    print(f"
Shapiro-Wilk test for residuals: statistic={shapiro_stat:.3f}, p-value={shapiro_p:.3f}")

# %%
# --- Application: Finding best predictor for runs ---
try:
    team_batting = pd.read_csv(kbo_team_batting.csv')
except FileNotFoundError:
    print("
Could not find kbo_team_batting.csv'.")
    team_batting = pd.DataFrame()

# %%
if not team_batting.empty:
    # Feature engineering
    team_batting = team_batting.assign(
        runs_per_tpa = lambda df: df['r'] / df['tpa'],
        obp = lambda df: (df['h'] + df['bb'] + df['hbp']) / (df['ab'] + df['bb'] + df['hbp'] + df['sf']),
        slg = lambda df: (df['h'] + 2*df['X2b'] + 3*df['X3b'] + 4*df['hr']) / df['ab']
    )
    team_batting['ops'] = team_batting['obp'] + team_batting['slg']

    predictors = ['avg', 'obp', 'slg', 'ops']
    results = []
    for pred in predictors:
        model = ols(f'runs_per_tpa ~ {pred}', data=team_batting).fit()
        results.append({'predictor': pred, 'r_squared': model.rsquared})
    
    r_squared_df = pd.DataFrame(results)
    print("
R-squared for different predictors of runs:")
    print(r_squared_df.sort_values(by='r_squared', ascending=False))

# %%
print("
Conversion of chapter_15.R to Python is complete.")
