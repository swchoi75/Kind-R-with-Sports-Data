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
This script is a Python conversion of the R script chapter_17.R.
It covers logistic regression, probability simulations, and a scikit-learn ML workflow.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_line, geom_histogram, geom_hline, geom_path, geom_abline, coord_equal
import statsmodels.api as sm
from statsmodels.formula.api import logit
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, roc_auc_score
import matplotlib.pyplot as plt # For ROC curve plotting helper

# %%
np.random.seed(1234)

# %%
# --- Probability Simulations ---
# Lotte Baseball Simulation
n_simulations = 100000
additional_wins = np.random.binomial(n=100, p=0.5, size=n_simulations)
expected_win_rate = (additional_wins + 22) / 144
playoff_threshold = np.random.choice(np.arange(0.486, 0.559, 0.010), size=n_simulations, replace=True)
made_playoffs = np.where(expected_win_rate >= playoff_threshold, 1, 0)

# %%
lotte_simulation = pd.DataFrame({
    '추가_승수': additional_wins,
    '예상_승률': expected_win_rate,
    '마지노선': playoff_threshold,
    '진출_성공': made_playoffs
})

# %%
lotte_summary = lotte_simulation.groupby('추가_승수').agg(
    전체_횟수=('추가_승수', 'size'),
    진출_성공=('진출_성공', 'sum')
).reset_index()
lotte_summary['진출_확률'] = lotte_summary['진출_성공'] / lotte_summary['전체_횟수']

# %%
p = (ggplot(lotte_summary, aes(x='추가_승수', y='진출_확률')) + geom_line())
# print(p)

# %%
# Odds and Logit Plot
x_vals = np.arange(-10, 10.1, 0.1)
y_vals = np.exp(x_vals) / (1 + np.exp(x_vals))
sigmoid_df = pd.DataFrame({'x': x_vals, 'y': y_vals})

# %%
p_sigmoid = (ggplot(sigmoid_df, aes(x='x', y='y')) + geom_line())
# print(p_sigmoid)

# %%
# --- Logistic Regression ---
try:
    kovo_sets = pd.read_csv('R/kovo_set_by_set.csv')
    kovo_sets['승리'] = kovo_sets['승리'].astype('category') # Target variable
except FileNotFoundError:
    print("
Could not find 'R/kovo_set_by_set.csv'.")
    kovo_sets = pd.DataFrame()

# %%
if not kovo_sets.empty:
    kovo_set_male = kovo_sets[kovo_sets['남녀부'] == '남'].copy()

    # Using statsmodels for logistic regression with formula API
    model_formula = '승리 ~ 서브효율 + 리시브효율 + 공격효율 + 블로킹 + 디그'
    glm_model = logit(model_formula, data=kovo_set_male).fit()
    print("
--- Statsmodels Logistic Regression Summary ---")
    print(glm_model.summary().tables[1]) # Coefficients table

    # --- scikit-learn ML Workflow ---
    # 1. Split data
    X = kovo_set_male[['서브효율', '리시브효율', '공격효율', '블로킹', '디그']]
    y = kovo_set_male['승리']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1234, stratify=y)
    
    # 2. Preprocessing Pipeline (Recipe equivalent)
    # Using StandardScaler for normalization
    # No step_corr equivalent is directly used here, but it would be a separate step or feature selection.
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('log_reg', LogisticRegression(random_state=1234))
    ])

    # 3. Fit workflow (model)
    set_lr_fit = pipeline.fit(X_train, y_train)

    # 4. Predict
    y_pred_class_train = set_lr_fit.predict(X_train)
    y_pred_proba_train = set_lr_fit.predict_proba(X_train) # Probabilities for each class

    # 5. Evaluate on training set
    print("
--- Training Set Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_train, y_pred_class_train):.3f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_train, y_pred_class_train))
    
    # Predict and evaluate on test set
    y_pred_class_test = set_lr_fit.predict(X_test)
    print("
--- Test Set Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred_class_test):.3f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred_class_test))

    # ROC Curve and AUC
    # Get probabilities for the positive class (assuming '1' is positive)
    y_scores_train = set_lr_fit.predict_proba(X_train)[:, 1]
    fpr_train, tpr_train, _ = roc_curve(y_train, y_scores_train, pos_label='1')
    roc_auc_train = roc_auc_score(y_train, y_scores_train)
    
    roc_df_train = pd.DataFrame({'1 - specificity': fpr_train, 'sensitivity': tpr_train})
    
    p_roc_train = (ggplot(roc_df_train, aes(x='1 - specificity', y='sensitivity')) +
                   geom_path() +
                   geom_abline(linetype='dotted') +
                   coord_equal())
    # print(p_roc_train)
    
    print(f"ROC AUC on training set: {roc_auc_train:.3f}")

    y_scores_test = set_lr_fit.predict_proba(X_test)[:, 1]
    fpr_test, tpr_test, _ = roc_curve(y_test, y_scores_test, pos_label='1')
    roc_auc_test = roc_auc_score(y_test, y_scores_test)
    print(f"ROC AUC on test set: {roc_auc_test:.3f}")


# %%
print("
Conversion of chapter_17.R to Python is complete.")
