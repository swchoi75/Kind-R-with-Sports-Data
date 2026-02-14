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
This script is a Python conversion of the R script chapter_10.R.
It demonstrates bootstrapping to estimate confidence intervals using pandas and numpy.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_histogram, geom_vline, annotate

# %%
np.random.seed(1234)

# %%
# Load data
try:
    cheonan_attendance = pd.read_csv('R/cheonan_attendance.csv')
except FileNotFoundError:
    print("Could not find 'R/cheonan_attendance.csv'.")
    cheonan_attendance = pd.DataFrame()

# %%
if not cheonan_attendance.empty:
    # True proportion of females in the population
    true_female_proportion = (cheonan_attendance['성별'] == '여').mean()
    print(f"True female proportion in Cheonan data: {true_female_proportion:.3f}")

    # 1. Take an initial sample from the population
    cheonan_sample_df = cheonan_attendance.sample(n=20, replace=True)
    sample_prop = (cheonan_sample_df['성별'] == '여').mean()
    print(f"Proportion of females in the initial sample: {sample_prop:.3f}")

    # In the R script, a sample of proportions is created first. We'll follow that.
    # This step is a bit convoluted but we replicate it for consistency.
    cheonan_sample_list = []
    for _ in range(10):
        cheonan_sample_list.append(
            {'여성비율': (cheonan_attendance.sample(n=20, replace=True)['성별'] == '여').mean()}
        )
    cheonan_sample = pd.DataFrame(cheonan_sample_list)


    # 2. Bootstrap from the sample
    # The R script bootstraps from `cheonan_sample` which is a dataframe of proportions.
    # A more standard workflow would be to bootstrap from the original sample of 20 people.
    # However, we will follow the R script's logic.

    n_reps = 1000
    bootstrap_means = []
    for _ in range(n_reps):
        # Generate a bootstrap sample by resampling from the sample of proportions
        bootstrap_sample = cheonan_sample['여성비율'].sample(frac=1, replace=True)
        # Calculate the mean of the bootstrap sample
        bootstrap_means.append(bootstrap_sample.mean())

    cheonan_bootstrap = pd.DataFrame({'stat': bootstrap_means})

    # 3. Visualize the bootstrap distribution
    p = (ggplot(cheonan_bootstrap, aes(x='stat')) +
         geom_histogram(binwidth=0.01, fill='gray75', color='white', alpha=0.8))
    # print(p)

    # 4. Calculate the percentile confidence interval
    ci_endpoints = cheonan_bootstrap['stat'].quantile([0.025, 0.975]).to_dict()
    low = ci_endpoints[0.025]
    high = ci_endpoints[0.975]
    print(f"95% Percentile Confidence Interval: ({low:.3f}, {high:.3f})")
    
    # 5. Visualize the confidence interval
    p = (p +
         annotate("rect", xmin=low, xmax=high, ymin=-np.inf, ymax=np.inf, fill="blue", alpha=0.2) +
         geom_vline(xintercept=[low, high], color='blue', linetype='dashed'))
    # print(p)

    # 6. Calculate confidence interval using the standard error method
    point_estimate = cheonan_sample['여성비율'].mean()
    se = cheonan_bootstrap['stat'].std()
    ci_se_low = point_estimate - 1.96 * se
    ci_se_high = point_estimate + 1.96 * se
    print(f"95% SE Confidence Interval: ({ci_se_low:.3f}, {ci_se_high:.3f})")
    
    p = (p +
         geom_vline(xintercept=[ci_se_low, ci_se_high], color='darkorange', linetype='dashed', size=1))
    print(p)


# %%
print("Conversion of chapter_10.R to Python is complete.")

