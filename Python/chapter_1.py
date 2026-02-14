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
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

"""
This script is a Python conversion of the R script chapter_1.R.
"""

import pandas as pd
import os

print("Hello, World!")

print(1 + 2)

object_ = 1 + 2
print(object_) # print object_

# In Python, we don't have a direct equivalent of R's ls() to list objects in the current environment in a script.
# We can use dir() but it's not a one-to-one mapping.
# It's better to manage variables explicitly.

del object_ # delete object_

# rm(list = ls()) in R removes all objects from the environment.
# There is no simple direct equivalent in Python scripts.

x = y = z = 1 + 2

print(x)
print(y)
print(z)

print([x, y, z])

print([1, 2, 3])

print(list(range(1, 11)))

print(list(range(1, 11, 2)))

def add_one(x):
  return x + 1

print(add_one(2))

df1 = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
print(df1)

print(type(df1))

print(df1['x'])

df1['z'] = [7, 8, 9]
print(df1)

print(df1.iloc[0]) # Print the first row

print(df1.iloc[:, 0]) # Print the first column

print(df1.iloc[1, 1]) # Print the element at the second row and second column

print(1 == 1)
print(1 == 2)

print(df1['x'] == 1)

print(df1[df1['x'] == 1])

# The original R code df1[, df1$x == 2] is ambiguous.
# It seems to intend to filter columns, but the condition is on rows.
# A more likely intention is to filter rows, which is what is done here.
print(df1[df1['x'] == 2])

print(type(df1))

print(os.getcwd())

# The URL from the R script needs to be the "raw" version to be read by pandas
# batting = pd.read_csv(
#   'https://raw.githubusercontent.com/bigkini/kindeR/main/kbo_batting_qualified.csv'
# )
batting = pd.read_csv('kbo_batting_qualified.csv')

# Assuming 'kbo_batting_qualified.csv' is in the 'R' directory as per the context
try:
    batting_local = pd.read_csv('kbo_batting_qualified.csv')
    print("Successfully read local file.")
except FileNotFoundError:
    print("Local file kbo_batting_qualified.csv' not found, using remote.")
    batting_local = batting

print(type(batting))

batting.info()

print(batting.head())

print(batting.tail(5))

print(batting['avg'].head(5))

print(batting['avg'].mean())

print(batting['avg'].std())

print(batting.describe())

print(pd.Series(range(101)).describe())

# The following R commands are for interactive sessions and don't have direct equivalents for scripts.
# length(ls('package:base'))
# ?ls
# args(rm)
