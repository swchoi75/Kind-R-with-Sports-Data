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
This script is a Python conversion of the R script chapter_3.R.
It uses the plotnine library, which is a Python implementation of ggplot2.
"""

import pandas as pd
from plotnine import *
from io import StringIO
import numpy as np
from scipy.stats import norm

# In R, the 'here' package is used for path management.
# In Python, we can define a base path or use relative paths.
# We'll assume the script is run from the project root.
path = '.'

try:
    batting = pd.read_csv(f'{path}/R/kbo_batting_qualified.csv')
except FileNotFoundError:
    print("Could not find kbo_batting_qualified.csv'.")
    batting = pd.DataFrame()

# In plotnine, plots are created by initializing ggplot and adding layers with '+'
if not batting.empty:
    p = (ggplot(data=batting))
    # In R, just running `p` would display the plot. 
    # In a script, you need to explicitly print or save the plot.
    # print(p)

    # Histogram
    p = (ggplot(data=batting, mapping=aes(x='avg')) +
         geom_histogram())
    # print(p)

    p = (ggplot(batting, aes('avg')) +
         geom_histogram())
    # print(p)

    p = (ggplot(batting, aes('avg')) +
         geom_histogram(binwidth=.001))
    # print(p)

    p = (ggplot(batting, aes('avg')) +
         geom_histogram(bins=30, fill="gray", color="red"))
    # print(p)

    # rgb() function in R can be directly used as a string in plotnine
    p = (ggplot(batting, aes('avg')) +
         geom_histogram(
             bins=30,
             fill='#53BFD4', # rgb(0.325, 0.750, 0.830)
             color="white"
         ))
    # print(p)

    # Bar plot
    p = (ggplot(batting, aes('throw_bat')) +
         geom_bar())
    # print(p)
    
    # an alternative way of doing the above
    p = (ggplot(batting, aes(x='throw_bat', y=after_stat('count'))) +
         geom_bar())
    # print(p)
    
    p = (ggplot(batting, aes('throw_bat')) +
     stat_count())
    # print(p)

    # R's table() is similar to pandas' value_counts()
    print(batting['throw_bat'].value_counts())

    bar_example_data = """
    throw_bat,count
    우양,30
    우우,1001
    우좌,155
    좌좌,435
    """
    bar_example = pd.read_csv(StringIO(bar_example_data))

    # when y is already in the data, use geom_col (or geom_bar(stat="identity"))
    p = (ggplot(bar_example, aes(x='throw_bat', y='count')) +
         geom_col())
    # print(p)

    # Reordering factors
    # plotnine can use reorder
    p = (ggplot(bar_example, aes(x='reorder(throw_bat, count)', y='count')) +
         geom_col())
    # print(p)

    p = (ggplot(bar_example, aes(x='reorder(throw_bat, -count)', y='count')) +
         geom_col())
    # print(p)
    
    # fct_infreq from forcats can be replicated by getting value counts and then plotting
    throw_bat_counts = batting['throw_bat'].value_counts().index.tolist()
    batting['throw_bat_ordered'] = pd.Categorical(batting['throw_bat'], categories=throw_bat_counts, ordered=True)
    p = (ggplot(batting, aes(x='throw_bat_ordered')) + geom_bar())
    # print(p)

    # Line plot
    rank1 = batting[batting['rank'] == 1]
    p = (ggplot(rank1, aes(x='year', y='avg')) +
         geom_line())
    # print(p)
    
    p = (ggplot(rank1, aes(x='year', y='avg')) +
         geom_line(size=1)) # lwd is size in plotnine
    # print(p)

    p = (ggplot(rank1, aes(x='year', y='avg')) +
         geom_line(linetype="dashed"))
    # print(p)
    
    p = (ggplot(rank1, aes(x='year', y='avg')) +
         geom_line(linetype='dashed')) # lty=2 is dashed
    # print(p)

    # Load ryu data
    try:
        ryu = pd.read_csv(f'{path}/R/2020_ryu.csv')
    except FileNotFoundError:
        print("Could not find 2020_ryu.csv'.")
        ryu = pd.DataFrame()

    if not ryu.empty:
        print(ryu.shape)
        print(ryu.columns)

        p = (ggplot(ryu, aes(x='reorder(pitch_name, release_speed)', y='release_speed')) +
             geom_point())
        # print(p)

        p = (ggplot(ryu, aes(x='reorder(pitch_name, release_speed)', y='release_speed')) +
             geom_jitter())
        # print(p)

        p = (ggplot(ryu, aes(x='reorder(pitch_name, release_speed)', y='release_speed')) +
             geom_violin() +
             geom_jitter(alpha=.2))
        # print(p)

        p = (ggplot(ryu, aes(x='reorder(pitch_name, release_speed)', y='release_speed')) +
             geom_boxplot())
        # print(p)

        p = (ggplot(ryu, aes(x='plate_x', y='plate_z')) +
             geom_point())
        # print(p)

        p = (ggplot(ryu, aes(x='plate_x', y='plate_z')) +
             geom_point() +
             facet_grid('. ~ pitch_name') +
             coord_fixed())
        # print(p)

        p = (ggplot(ryu, aes(x='plate_x', y='plate_z')) +
             geom_density_2d_filled() +
             facet_grid('stand ~ pitch_name') +
             coord_fixed() +
             guides(fill=False))
        # print(p)
        
        ryu_fastball_changeup = ryu[ryu['pitch_name'].isin(["4-Seam Fastball", "Changeup"])]
        p = (ggplot(ryu_fastball_changeup, aes(x='plate_x', y='plate_z')) +
             geom_density_2d_filled() +
             geom_rect(aes(xmin=-1, xmax=1, ymin=1, ymax=3), color="white", alpha=.1, linetype="dashed", inherit_aes=False) +
             facet_grid('pitch_name ~ stand') +
             coord_fixed() +
             guides(fill=False))
        # print(p)

        p = (ggplot(batting, aes(x='avg', y='obp', shape='throw_bat')) +
             geom_point())
        # print(p)

        p = (ggplot(ryu, aes(x='release_speed')) +
             geom_density(fill='gray75'))
        # print(p)

        p = (ggplot(ryu, aes(x='release_speed')) +
             geom_density(fill='gray75') +
             facet_grid('reorder(pitch_name, -release_speed) ~ .'))
        # print(p)

        # geom_function(fun=dnorm) in ggplot2 needs to be done manually in plotnine
        x_norm = np.linspace(-5, 5, 100)
        y_norm = norm.pdf(x_norm)
        norm_df = pd.DataFrame({'x': x_norm, 'y': y_norm})
        p = (ggplot(norm_df, aes(x='x', y='y')) + geom_line())
        # print(p)
        
        p = (ggplot(norm_df, aes(x='x', y='y')) + geom_area())
        # print(p)

        developers_chore_data = """
response,value
"이름 짓기",49
"개발 가능 혹은 불가능한 사항 설명하기",16
"개발 작업이 끝나는 시간 산정하기",10
"다른 사람과 함께 일하기",8
"다른 개발자 코드 작업하기",8
"내가 수긍 못할 기능 구현하기",3
"문서 작성",2
"테스트 작성",2
"해법 찾기",2
"""
        developers_chore = pd.read_csv(StringIO(developers_chore_data))
        
        p = (ggplot(developers_chore, aes(x='reorder(response, value)', y='value')) +
             geom_col())
        # print(p)

        p = (ggplot(developers_chore, aes(x='reorder(response, value)', y='value')) +
             geom_col() +
             geom_text(aes(label='value'), nudge_y=2) +
             coord_flip())
        # print(p)

        p = (ggplot(developers_chore, aes(x="''", y='value', fill='reorder(response, value)')) +
             geom_col(width=1) +
             coord_polar(theta='y'))
        # print(p)

        rank1 = batting[batting['rank'] == 1]
        p = (ggplot(rank1, aes(x='year', y='avg')) +
             geom_line() +
             ylim(.350, .420))
        # print(p)

        p = (ggplot(rank1, aes(x='year', y='avg')) +
             geom_line() +
             coord_cartesian(ylim=(.350, .420)))
        # print(p)

print("Conversion of chapter_3.R to Python is complete.")
print("Uncomment the print(p) lines to display the plots.")
