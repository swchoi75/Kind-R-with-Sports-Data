# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.19.1
# ---

"""
This script is a Python conversion of the R script chapter_2.R.
"""

import pandas as pd
from io import StringIO
import statsmodels.api as sm

# In R, many packages are loaded using library(). 
# In Python, we import the necessary libraries.
# 'tidyverse' is a collection of R packages. The Python equivalent is a combination of libraries
# like pandas, numpy, matplotlib, seaborn, etc.
# 'tidymodels' is used for modeling, scikit-learn is a Python equivalent.

# Load the mtcars dataset from statsmodels
mtcars_data = sm.datasets.get_rdataset("mtcars")
mtcars = mtcars_data.data

# In R: mtcars[sample(1:nrow(mtcars), 10), ]
# In pandas, we can use the sample() method.
print(mtcars.sample(n=10))

# In R: batting <- read_csv('kbo_batting_qualified.csv')
# The file path needs to be relative to the project root.
try:
    batting = pd.read_csv('R/kbo_batting_qualified.csv', encoding='utf-8')
    print("Successfully read 'R/kbo_batting_qualified.csv'")
    # In R: glimpse(batting)
    batting.info()
    print(batting)
except FileNotFoundError:
    print("Could not find 'R/kbo_batting_qualified.csv'.")
    batting = pd.DataFrame() # Create an empty DataFrame

# In R: class(batting)
print(type(batting))

# In R, a data.frame can be converted to a tibble. In pandas, we just use DataFrames.
# The following R code is not necessary in Python:
# batting <- read.csv('kbo_batting_qualified.csv')
# batting <- as_tibble(batting)

# Creating dataframes in pandas
df1 = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
print(df1)

# In R, tribble is used to create tibbles row-by-row.
# In pandas, we can create a DataFrame from a string using io.StringIO
df2_data = """
x,y
1,4
2,5
3,6
"""
df2 = pd.read_csv(StringIO(df2_data))
print(df2)

# In R: 1:10 %>% sum()
# The pipe operator %>% is not a standard feature in Python.
print(sum(range(1, 11)))

# In R: batting %>% print(n = 20)
print(batting.head(20))

# In R: 'kbo_batting_qualified.csv' %>% read.csv() %>% as_tibble() -> batting
# This is another way to write the file reading using pipes.
# The Python equivalent is a simple read_csv.
try:
    batting_from_pipe = pd.read_csv('R/kbo_batting_qualified.csv')
    print("Successfully read 'R/kbo_batting_qualified.csv' again.")
    print(batting_from_pipe)
except FileNotFoundError:
    print("Could not find 'R/kbo_batting_qualified.csv'.")

