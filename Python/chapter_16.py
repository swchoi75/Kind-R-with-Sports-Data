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
This script is a Python conversion of the R script chapter_16.R.
It covers multiple linear regression, multicollinearity, and model evaluation workflows.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_histogram
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# %%
np.random.seed(1234)

# %%
# Load and prepare data
try:
    team_batting = pd.read_csv(kbo_team_batting.csv')
except FileNotFoundError:
    print("Could not find kbo_team_batting.csv'.")
    team_batting = pd.DataFrame()

# %%
if not team_batting.empty:
    team_batting = team_batting.assign(
        runs = lambda df: df['r'] / df['tpa'],
        avg = lambda df: df['h'] / df['ab'],
        obp = lambda df: (df['h'] + df['bb'] + df['hbp']) / (df['ab'] + df['bb'] + df['hbp'] + df['sf']),
        slg = lambda df: (df['h'] + 2*df['X2b'] + 3*df['X3b'] + 4*df['hr']) / df['ab']
    )

    # --- Multicollinearity (VIF) ---
    # Select predictors
    X = team_batting[['avg', 'obp', 'slg']]
    # Add a constant for the intercept
    X['intercept'] = 1
    
    # Calculate VIF for each predictor
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
    
    print("--- Variance Inflation Factor (VIF) ---")
    # We are interested in the VIF for the predictors, not the intercept
    print(vif_data[vif_data['feature'] != 'intercept'])

    # --- Multiple Regression with statsmodels ---
    # Model with all three predictors
    model_full = ols('runs ~ avg + obp + slg', data=team_batting).fit()
    print("
--- Full Model Summary ---")
    print(model_full.summary())
    
    # Model without 'avg' due to high VIF
    model_reduced = ols('runs ~ obp + slg', data=team_batting).fit()
    print("
--- Reduced Model Summary (without avg) ---")
    print(model_reduced.summary())

    # --- scikit-learn for Predictive Modeling Workflow ---
    # 1. Define features (X) and target (y)
    X_skl = team_batting[['obp', 'slg']]
    y_skl = team_batting['runs']

    # 2. Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_skl, y_skl, test_size=0.3, random_state=1234)
    print(f"
Training set size: {len(X_train)}, Testing set size: {len(X_test)}")

    # 3. Create and fit the model
    lm = LinearRegression()
    team_batting_fit = lm.fit(X_train, y_train)
    
    # 4. Make predictions on the test set
    predictions = team_batting_fit.predict(X_test)

    # 5. Evaluate the model with RMSE
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(f"
Root Mean Squared Error (RMSE) on test data: {rmse:.4f}")

# %%
# --- Interaction Terms ---
try:
    kovo_sets_results = pd.read_csv(kovo_sets_results.csv')
except FileNotFoundError:
    print("
Could not find kovo_sets_results.csv'.")
    kovo_sets_results = pd.DataFrame()

# %%
if not kovo_sets_results.empty:
    # Fit a model with an interaction term
    interaction_model = ols('승률 ~ 리시브_효율 * 남녀부', data=kovo_sets_results).fit()
    print("
--- Model with Interaction Term ---")
    print(interaction_model.summary().tables[1]) # Print just the coefficients table


# %%
print("
Conversion of chapter_16.R to Python is complete.")
