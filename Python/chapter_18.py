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
This script is a Python conversion of the R script chapter_18.R.
It covers probability simulations (Monty Hall problem) and Bayesian statistics.
"""

# %%
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_line, geom_histogram, geom_hline, stat_function
from scipy.stats import beta
from scipy.optimize import fmin_tnc # for fitting beta distribution if beta.fit is not enough

# %%
np.random.seed(1234)

# %%
# --- Monty Hall Simulation ---
n_trials = 10000

# %%
# Simulate car position and initial pick
cars = np.random.randint(1, 4, n_trials)
initial_picks = np.random.randint(1, 4, n_trials)

# %%
# Determine what Monty opens (must not be car, must not be initial pick)
monty_opens = np.zeros(n_trials, dtype=int)
for i in range(n_trials):
    available_doors = [1, 2, 3]
    
    # Remove the car door and the initial pick from options for Monty to open
    # If initial pick is car, Monty can open any of the other two
    if cars[i] == initial_picks[i]:
        options_for_monty = [d for d in available_doors if d != cars[i]]
    else:
        # If initial pick is not car, Monty must open the remaining empty door
        options_for_monty = [d for d in available_doors if d != cars[i] and d != initial_picks[i]]
    
    monty_opens[i] = np.random.choice(options_for_monty)


# %%
# Determine the door if we switch
switched_picks = np.zeros(n_trials, dtype=int)
for i in range(n_trials):
    available_doors = [1, 2, 3]
    options_to_switch_to = [d for d in available_doors if d != initial_picks[i] and d != monty_opens[i]]
    switched_picks[i] = options_to_switch_to[0] # There will only be one option


# %%
# Calculate results
results_df = pd.DataFrame({
    'trial': np.arange(1, n_trials + 1),
    'car': cars,
    'initial_pick': initial_picks,
    'monty_opens': monty_opens,
    'switched_pick': switched_picks
})

# %%
results_df['result_if_switch'] = (results_df['car'] == results_df['switched_pick']).astype(int)
results_df['success_rate'] = results_df['result_if_switch'].expanding().mean()

# %%
# Plot simulation results
p = (ggplot(results_df, aes(x='trial', y='success_rate')) +
     geom_line(size=1.25) +
     geom_hline(yintercept=2/3, linetype='dashed', color='#147893', size=1) +
     scale_y_continuous(limits=(0, 1)))
# print(p)

# %%
# --- Bayesian Batting Average Estimation ---
try:
    kbo_batting_bayesian = pd.read_csv(kbo_batting_bayesian.csv')
except FileNotFoundError:
    print("
Could not find kbo_batting_bayesian.csv'.")
    kbo_batting_bayesian = pd.DataFrame()

# %%
if not kbo_batting_bayesian.empty:
    kbo_batting_250 = kbo_batting_bayesian[kbo_batting_bayesian['tpa'] >= 250].copy()
    kbo_batting_250['avg'] = kbo_batting_250['h'] / kbo_batting_250['ab']

    # Plot histogram of batting averages
    p_hist = (ggplot(kbo_batting_250, aes(x='avg')) +
              geom_histogram(aes(y='stat(density)'), fill='gray80', color='white', bins=30))
    # print(p_hist)

    # Fit Beta distribution to batting averages
    # beta.fit returns (alpha, beta, loc, scale). We want alpha and beta.
    alpha_fit, beta_fit, _, _ = beta.fit(kbo_batting_250['avg'], floc=0, fscale=1)
    
    print(f"
Fitted Beta Distribution Parameters: alpha={alpha_fit:.2f}, beta={beta_fit:.2f}")

    # Overlay fitted Beta distribution PDF
    p_beta = (p_hist +
              stat_function(fun=beta.pdf, args={'a': alpha_fit, 'b': beta_fit, 'loc': 0, 'scale': 1},
                            color='#53bfd4', size=1.25))
    # print(p_beta)
    
    # Mean of the fitted Beta distribution (prior mean)
    prior_mean = alpha_fit / (alpha_fit + beta_fit)
    print(f"Mean of the fitted Beta distribution (prior): {prior_mean:.3f}")

    # Example of Bayesian update
    # Assume a player has 45 hits in 109 at-bats (avg = 0.413)
    player_h = 45
    player_ab = 109
    
    # Posterior parameters: alpha_posterior = alpha_prior + hits, beta_posterior = beta_prior + (at-bats - hits)
    alpha_posterior = alpha_fit + player_h
    beta_posterior = beta_fit + (player_ab - player_h)
    
    posterior_mean = alpha_posterior / (alpha_posterior + beta_posterior)
    print(f"
Player with {player_h} hits in {player_ab} at-bats:")
    print(f"Observed average: {player_h / player_ab:.3f}")
    print(f"Posterior mean batting average: {posterior_mean:.3f}")

# %%
print("
Conversion of chapter_18.R to Python is complete.")
