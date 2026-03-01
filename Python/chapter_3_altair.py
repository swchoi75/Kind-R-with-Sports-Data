# ---
# jupyter:
#   jupytext:
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
import polars as pl
import numpy as np
import altair as alt
from scipy.stats import norm # For the geom_function equivalent

# %%
# --- Data Loading
batting = pl.read_csv("kbo_batting_qualified.csv")
ryu = pl.read_csv("2020_ryu.csv")

# %% [markdown]
# ## Histogram Chart

# %%
alt.Chart(batting).mark_bar().encode(
    alt.X("avg:Q", bin=alt.Bin(maxbins=40)),
    y='count()',
).properties(
    width=600,
    height=400,
    title = "Histogram of AVG",
)

# %%
alt.Chart(batting).mark_bar().encode(
    alt.X("avg:Q", bin=alt.Bin(step=0.001)),
    y='count()',
).properties(
    width=600,
    height=400,
    title = "Histogram of AVG (Binwidth=0.001)",
)

# %%
alt.Chart(batting).mark_bar(
    color="gray",
    stroke="red",
    strokeWidth=1,    
).encode(
    alt.X("avg:Q", bin=alt.Bin(maxbins=30)),
    y='count()',
).properties(
    width=600,
    height=400,
    title = "Histogram of AVG (Bins=30, Gray fill, Red edge)",
)

# %%
alt.Chart(batting).mark_bar(
    color="blue",
    stroke="white",
    strokeWidth=1,    
).encode(
    alt.X("avg:Q", bin=alt.Bin(maxbins=30)),
    y='count()',
).properties(
    width=600,
    height=400,
    title = "Histogram of AVG (Bins=30, Blue fill, White edge)",
)

# %%
alt.Chart(batting).mark_bar(
    color="#53BFD4",
    stroke="white",
    strokeWidth=1,    
).encode(
    alt.X("avg:Q", bin=alt.Bin(maxbins=30)),
    y='count()',
).properties(
    width=600,
    height=400,
    title = "Histogram of AVG (Bins=30, Hex fill, White edge)",
)

# %% [markdown]
# ## Bar Chart

# %%
alt.Chart(batting).mark_bar(size=80).encode(
    x=alt.X("throw_bat:N", sort='-y'),
    y='count()',
).properties(
    width=600,
    height=400,
    title = "Bar Plot (Count) of throw_bat",
)

# %%
# Pre-summarized data example
bar_example = pl.DataFrame(
    {
        "throw_bat": ["우양", "우우", "우좌", "좌좌"],
        "count": [30, 1001, 155, 435],
    }
)
bar_example

# %%
alt.Chart(bar_example).mark_bar().encode(
    x="throw_bat:N",
    y='count',
).properties(
    width=600,
    height=400,
    title = "Bar Plot (Identity) of throw_bat vs count",
)

# %%
alt.Chart(bar_example).mark_bar().encode(
    x=alt.X("throw_bat:N", sort='-y'),
    y='count',
).properties(
    width=600,
    height=400,
    title = "Bar Plot (Identity) of throw_bat vs count",
)

# %% [markdown]
# ## Line Chart

# %%
# Filter data
batting_rank_1 = batting.filter(pl.col("rank") == 1)

# %%
alt.Chart(batting_rank_1).mark_line().encode(
    x="year:N",
    y=alt.Y('avg:Q', scale=alt.Scale(zero=False)),
).properties(
    width=600,
    height=400,
    title = "Line Plot of AVG vs Year (Rank 1 players)",
)

# %%
alt.Chart(batting_rank_1).mark_line(
    strokeWidth=5,
).encode(
    x="year:N",
    y=alt.Y('avg:Q', scale=alt.Scale(zero=False)),
).properties(
    width=600,
    height=400,
    title = "Line Plot of AVG vs Year (strokeWidth=5)",
)

# %%
alt.Chart(batting_rank_1).mark_line(
    strokeWidth=3,
    strokeDash=[10, 10],
).encode(
    x="year:N",
    y=alt.Y('avg:Q', scale=alt.Scale(zero=False)),
).properties(
    width=600,
    height=400,
    title = "Line Plot of AVG vs Year (Dashed linestyle)",
)

# %% [markdown]
# ## Point Chart

# %%
alt.Chart(ryu).mark_point().encode(
    x="pitch_name:N",
    y=alt.Y("release_speed:Q", scale=alt.Scale(zero=False)),
).properties(
    width=600,
    height=400,
    title = "Scatter Plot of Release Speed vs Pitch Name",
)

# %%
alt.Chart(ryu).transform_calculate(
    jitter="(random() - 0.5) * 0.4",   # control spread here
).mark_point().encode(
    x="pitch_name:N",
    y=alt.Y("release_speed:Q", scale=alt.Scale(zero=False)),
    xOffset="jitter:Q"
).properties(
    width=600,
    height=400,
    title = "Scatter Plot of Release Speed vs Pitch Name",
)

# %%
base = alt.Chart(ryu).encode(
    x=alt.X("pitch_name:N"),
    y=alt.Y("release_speed:Q"),
).properties(
    width=600,
    height=400,
    title = "Violin Plot with Jittered Points",
)

# --- Violin ---
violin = base.transform_density(
    density="release_speed",
    as_=["release_speed", "density"],
    groupby=["pitch_name"],
).mark_area(
    orient="horizontal",
    opacity=0.4,
).encode(
    x=alt.X("density:Q", stack="center", title=None),
    y="release_speed:Q",
    color="pitch_name:N",
)

# --- Jittered Points ---
jitter = base.transform_calculate(
    jitter="(random() - 0.5) * 0.4",
).mark_point(
    size=20,
    opacity=0.6,
).encode(
    x=alt.X("pitch_name:N"),
    y="release_speed:Q",
    xOffset="jitter:Q",
    color="pitch_name:N",
)

violin + jitter

# %%
alt.Chart(ryu).mark_boxplot(
     size=150,   # ← increase this (default is usually ~20)
).encode(
    x="pitch_name:N",
    y=alt.Y("release_speed:Q", scale=alt.Scale(zero=False))
).properties(
    width=600,
    height=400,
    title = "Box Plot of Release Speed vs Pitch Name",
)

# %%
alt.Chart(ryu).mark_circle(
    size=60,
    opacity=0.6,
).encode(
    x="plate_x:Q",
    y="plate_z:Q",
).properties(
    width=400,
    height=400,
    title = "Scatter Plot of Plate X vs Plate Z",
)

# %%
alt.Chart(ryu).mark_circle(
    size=60,
    opacity=0.6,
).encode(
    x="plate_x:Q",
    y="plate_z:Q",
    column="pitch_name:N",
).properties(
    width=400,
    height=400,
    title = "Scatter Plot with Facet Grid (Pitch Name)",
)

# %%
alt.Chart(ryu).mark_circle(
    size=60,
    opacity=0.6,
).encode(
    x="plate_x:Q",
    y="plate_z:Q",
    column="pitch_name:N",
    row="stand:N",
).properties(
    width=400,
    height=400,
    title = "2D Density Plot with Facet Grid",
)

# %%
base = alt.Chart(ryu).mark_rect().encode(
    x=alt.X(
        "plate_x:Q",
        bin=alt.Bin(maxbins=30),
        title="plate_x",
    ),
    y=alt.Y(
        "plate_z:Q",
        bin=alt.Bin(maxbins=30),
        title="plate_z",
    ),
    color=alt.Color(
        "count():Q",
        scale=alt.Scale(scheme="reds"),
    )
).properties(
    width=200,
    height=200,
    title="2D Histogram (Binned Density) with Facet Grid",
)

chart = base.facet(
    row="stand:N",
    column="pitch_name:N",
)

chart

# %%
# Conditional plot for 4-Seam Fastball and Changeup
ryu_filtered = ryu.filter(pl.col("pitch_name").is_in(["4-Seam Fastball", "Changeup"]))

# %%
base = alt.Chart(ryu_filtered).mark_rect().encode(
    x=alt.X(
        "plate_x:Q",
        bin=alt.Bin(maxbins=30),
        title="plate_x",
    ),
    y=alt.Y(
        "plate_z:Q",
        bin=alt.Bin(maxbins=30),
        title="plate_z",
    ),
    color=alt.Color(
        "count():Q",
        scale=alt.Scale(scheme="reds"),
    )
).properties(
    width=200,
    height=200,
    title="2D Histogram (Binned Density) with Facet Grid",
)

chart = base.facet(
    row="stand:N",
    column="pitch_name:N",
)

chart

# %%
chart = alt.Chart(batting).mark_point().encode(
    x=alt.X("avg:Q", title="AVG", scale=alt.Scale(zero=False)),
    y=alt.Y("obp:Q", title="OBP", scale=alt.Scale(zero=False)),
    shape=alt.Shape("throw_bat:N", title="Throw Bat"),
).properties(
    width=400,
    height=300,
    title="Scatter Plot of AVG vs OBP, shaped by throw_bat",
)

chart

# %%
# 🔹 Total density
total = alt.Chart(ryu).transform_density(
    "release_speed",
    as_=["release_speed", "density"]
).mark_line(
    color="black",
    strokeWidth=3
).encode(
    x=alt.X("release_speed:Q", title="Release Speed"),
    y=alt.Y("density:Q", title="Density")
).properties(
    width=600,
    height=400,
    title="Density Plot of Release Speed"
)

# 🔹 Density by pitch type
by_pitch = alt.Chart(ryu).transform_density(
    "release_speed",
    as_=["release_speed", "density"],
    groupby=["pitch_name"]  # 👈 THIS IS THE KEY
).mark_line(
    color="gray",
    strokeWidth=2
).encode(
    x="release_speed:Q",
    y="density:Q"
).properties(
    width=400,
    height=200,
    title="Density Plot with Facet Grid (Pitch Name)"
).facet(
    row=alt.Row("pitch_name:N", title="Pitch Name")
)

# 🔹 Combine
chart = total & by_pitch

chart

# %%
# Create the Polars DataFrame
df = pl.DataFrame({"x": list(range(-5, 6))})

# %%
# Define the normal distribution function (dnorm)
# 1. Get range using Polars aggregations
min_val, max_val = df.select(
    pl.col("x").min().alias("min"), 
    pl.col("x").max().alias("max")
).to_dicts()[0].values()

# 2. Generate the values
x_values = np.linspace(min_val, max_val, 500)
y_values = norm.pdf(x_values)

# 3. Create a Polars DataFrame for plotting
df_dist = pl.DataFrame({
    "x": x_values,
    "y": y_values
})

# %%
df = pl.DataFrame({
    "x": x_values,
    "y": y_values
})

chart = alt.Chart(df).mark_line().encode(
    x=alt.X("x:Q", title="x"),
    y=alt.Y("y:Q", title="Probability Density"),
    color=alt.value("steelblue")
).properties(
    width=500,
    height=300,
    title="Line Plot of a Function (dnorm)"
)

chart

# %%
