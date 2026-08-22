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
This script is a Python conversion of the R script chapter_8.R.
It covers probability simulations using pandas, numpy, and scipy.
"""

# %%
import pandas as pd
import numpy as np
from scipy.special import comb
from scipy.stats import binom, norm
from plotnine import ggplot, aes, geom_line, geom_col, geom_histogram, coord_cartesian, stat_function
import math

# %%
# choose(45, 6)
print(comb(45, 6))

# %%
# pbirthday is not directly available in scipy, so we define it
def pbirthday(n):
    if n > 365:
        return 1.0
    return 1.0 - math.prod((365 - i) / 365 for i in range(n))

# %%
print(pbirthday(28))

# %%
np.random.seed(1234)

# %%
# Simulation of birthday paradox
def simulate_birthday_paradox(reps, size):
    days = np.arange(1, 366)
    simulations = [pd.DataFrame({'day': np.random.choice(days, size=size, replace=True)}) for _ in range(reps)]
    results = [sim['day'].duplicated().any() for sim in simulations]
    return np.mean(results)

# %%
print(simulate_birthday_paradox(reps=100, size=28))

# %%
# Run simulation for different group sizes
person_counts = range(2, 76)
birthday_simulation_results = [simulate_birthday_paradox(reps=1000, size=n) for n in person_counts]

# %%
birthday_paradox_simulation = pd.DataFrame({
    '사람': person_counts,
    '결과': birthday_simulation_results
})

# %%
print(birthday_paradox_simulation[birthday_paradox_simulation['결과'] >= 0.5].head(1))

# %%
p = (ggplot(birthday_paradox_simulation, aes(x='사람', y='결과')) +
     geom_line() +
     coord_cartesian(xlim=(2, 75)))
p

# %%
# Add theoretical probability
birthday_paradox_simulation['확률'] = [pbirthday(n) for n in person_counts]
p = (ggplot(birthday_paradox_simulation, aes(x='사람')) +
     geom_line(aes(y='확률'), size=2.5, color='#53bfd4', alpha=0.25) +
     geom_line(aes(y='결과'), size=0.75) +
     coord_cartesian(xlim=(2, 75)))
p


# %%
# Coin toss simulation
num_experiments = 100000
num_tosses = 100
coin_tosses = np.random.randint(0, 2, size=(num_experiments, num_tosses))
heads_counts = coin_tosses.sum(axis=1)

# %%
print(f"Number of experiments with exactly 50 heads: {(heads_counts == 50).sum()}")

# %%
p = (ggplot(pd.DataFrame({'앞': heads_counts}), aes(x='앞')) +
     geom_histogram(binwidth=1, fill='gray', color='white'))
p


# %%
# Binomial distribution
# dbinom(x=50, size=100, prob=0.5)
print(binom.pmf(k=50, n=100, p=0.5))

# %%
# 1 - pbinom(50, 100, 0.5)
print(1 - binom.cdf(k=50, n=100, p=0.5))
# or using survival function (sf)
print(binom.sf(k=50, n=100, p=0.5))

# %%
# pbinom(60, 100, 0.5) - pbinom(40, 100, 0.5)
print(binom.cdf(k=60, n=100, p=0.5) - binom.cdf(k=40, n=100, p=0.5))

# %%
# Plotting binomial and normal distributions
x_vals = range(0, 101)
dbinom_data = pd.DataFrame({
    'x': x_vals,
    'prob': [binom.pmf(k=x, n=100, p=0.5) for x in x_vals]
})

# %%
p = (ggplot(dbinom_data, aes(x='x', y='prob')) +
     geom_col(fill='gray', color='white') +
     stat_function(fun=norm.pdf, args={'loc': 50, 'scale': 5}, size=1, color='#53bfd4'))
p

# %%
# Normal distribution
# qnorm(p=0.5, mean=0, sd=1)
print(norm.ppf(q=0.5, loc=0, scale=1))

# %%
# rnorm(10000, mean=0, sd=1)
rnorm_data = pd.DataFrame({'x': norm.rvs(size=10000, loc=0, scale=1)})
p = (ggplot(rnorm_data, aes(x='x')) +
     geom_histogram(fill='gray', color='white', bins=30))
p

# %%
print("Conversion of chapter_8.R to Python is complete.")

