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
This script is a Python conversion of the R script chapter_9.R.
It focuses on sampling, resampling, and the Central Limit Theorem using pandas and numpy.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_histogram, geom_vline, geom_density, facet_grid
import itertools

# %%
np.random.seed(1234)

# %%
# Load data
try:
    gocheock_attendance = pd.read_csv(gocheock_attendance.csv')
except FileNotFoundError:
    print("Could not find gocheock_attendance.csv'.")
    gocheock_attendance = pd.DataFrame()

# %%
if not gocheock_attendance.empty:
    # Resampling simulation
    reps = 15
    size = 30
    
    samples = [gocheock_attendance.sample(n=size, replace=True) for _ in range(reps)]
    
    # Calculate proportion of '여성' for each sample
    female_proportions = [(sample['성별'] == '여').sum() / size for sample in samples]
    
    # Calculate the mean of the proportions
    mean_proportion = np.mean(female_proportions)
    print(f"Mean of female proportions: {mean_proportion}")

    # Plot the distribution of proportions
    proportions_df = pd.DataFrame({'여성비율': female_proportions})
    p = (ggplot(proportions_df, aes(x='여성비율')) +
         geom_histogram(binwidth=0.05, fill='gray75', color='white'))
    # print(p)

    # True proportion in the original data
    true_proportion = (gocheock_attendance['성별'] == '여').mean()
    print(f"True female proportion: {true_proportion}")
    
    p = p + geom_vline(xintercept=true_proportion, linetype='dashed', color='red')
    # print(p)

# %% [markdown]
# Central Limit Theorem Demonstration

# %%
# 1. Create a non-normal population
population1 = pd.DataFrame({
    'x': np.concatenate([
        np.random.normal(loc=50, scale=10, size=50000),
        np.random.beta(a=50, b=10, size=50000) * 100
    ])
})

# %%
p = (ggplot(population1, aes(x='x')) +
     geom_histogram(bins=30, fill='gray75', color='white'))
# print(p)

# %%
# 2. Simulate sampling and calculate sample means
sizes = [1, 5, 10, 30, 50, 1000]
reps_list = [10, 100, 1000, 10000]
simulation_params = list(itertools.product(sizes, reps_list))

# %%
all_sample_means = []

# %%
for size, reps in simulation_params:
    sample_means = [population1['x'].sample(n=size, replace=True).mean() for _ in range(reps)]
    df = pd.DataFrame({
        'sample_mean': sample_means,
        'size': size,
        'reps': reps
    })
    all_sample_means.append(df)

# %%
sample_mean_tbl = pd.concat(all_sample_means, ignore_index=True)

# %%
# 3. Plot the distribution of sample means
p = (ggplot(sample_mean_tbl, aes(x='sample_mean')) +
     geom_density(fill='gray75') +
     facet_grid('reps ~ size', scales='free_y') +
     geom_vline(xintercept=population1['x'].mean(), linetype='dotted'))
# print(p)

# %%
# 4. Analyze the results
clt_summary = sample_mean_tbl.groupby('size')['sample_mean'].agg(['mean', 'std']).reset_index()
clt_summary = clt_summary.rename(columns={'std': 'se'})
clt_summary['theoretical_se'] = population1['x'].std() / np.sqrt(clt_summary['size'])

# %%
print(clt_summary)


# %%
print("Conversion of chapter_9.R to Python is complete.")

