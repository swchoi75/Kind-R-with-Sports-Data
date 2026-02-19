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
This script is a Python conversion of the R script chapter_5.R.
It uses the pandas library for data tidying, which is the Python equivalent of tidyr.
"""

# %%
import pandas as pd

# %%
# Load the data from the Excel file
try:
    kbo_untidy = pd.read_excel(kbo_team_slash_untidy.xlsx')
    print("Successfully read kbo_team_slash_untidy.xlsx'")
    print(kbo_untidy)
except FileNotFoundError:
    print("Could not find kbo_team_slash_untidy.xlsx'.")
    kbo_untidy = pd.DataFrame()

# %%
if not kbo_untidy.empty:
    # fill(팀) -> ffill()
    kbo_filled_down = kbo_untidy.copy()
    kbo_filled_down['팀'] = kbo_filled_down['팀'].fillna(method='ffill')
    print(kbo_filled_down)

    # fill(팀, .direction = 'up') -> bfill()
    kbo_filled_up = kbo_untidy.copy()
    kbo_filled_up['팀'] = kbo_filled_up['팀'].fillna(method='bfill')
    print(kbo_filled_up)

    # pivot_longer -> melt
    df_long = pd.DataFrame({
        '선수': [1, 2],
        '타율': [.123, .234],
        '출루율': [.456, .567],
        '장타력': [.789, .891]
    })
    df_melted = df_long.melt(id_vars='선수', value_vars=['타율', '출루율', '장타력'],
                             var_name='기록', value_name='성적')
    print(df_melted)

    # pivot_wider -> pivot
    df_wide_data = {
        '선수': [1, 1, 1, 2, 2, 2],
        '기록': ['타율', '출루율', '장타력', '타율', '출루율', '장타력'],
        '성적': [.123, .456, .789, .234, .567, .891]
    }
    df_to_pivot = pd.DataFrame(df_wide_data)
    df_pivoted = df_to_pivot.pivot(index='선수', columns='기록', values='성적').reset_index()
    print(df_pivoted)

    # Applying to the kbo_untidy dataframe
    id_vars = ['팀', '구분']
    value_vars = [col for col in kbo_untidy.columns if col not in id_vars]
    
    kbo_long = kbo_filled_down.melt(id_vars=id_vars, value_vars=value_vars,
                                     var_name='연도', value_name='기록')
    print(kbo_long)
    print(kbo_long.sample(n=10))

    # values_drop_na = TRUE
    kbo_long_no_na = kbo_long.dropna(subset=['기록'])
    print(kbo_long_no_na.sample(n=10))

    # pivot_wider again
    kbo_tidy = kbo_long_no_na.pivot(index=['팀', '연도'], columns='구분', values='기록').reset_index()
    print(kbo_tidy)
    
    # as_factor() for '연도' column can be achieved by converting to category type
    kbo_tidy['연도'] = kbo_tidy['연도'].astype('category')
    print(kbo_tidy.info())

# %%
print("Conversion of chapter_5.R to Python is complete.")
