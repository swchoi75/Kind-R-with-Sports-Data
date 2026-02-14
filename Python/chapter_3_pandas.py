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
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm # For the geom_function equivalent

# %%
# --- Data Loading
batting = pd.read_csv("kbo_batting_qualified.csv")
ryu = pd.read_csv("2020_ryu.csv")

# %% [markdown]
# ## Histogram Chart

# %%
plt.figure(figsize=(8, 5))
sns.histplot(data=batting, x="avg")
plt.title("Histogram of AVG (Seaborn default)")
plt.show()

# %%
# For a specific bin width, use the `binwidth` parameter
plt.figure(figsize=(8, 5))
sns.histplot(data=batting, x="avg", binwidth=0.001)
plt.title("Histogram of AVG (Binwidth=0.001)")
plt.show()

# %%
# 'color' sets the edge color, 'facecolor' or 'fill' is for the bar color
plt.figure(figsize=(8, 5))
sns.histplot(data=batting, x="avg", bins=30, edgecolor="red", facecolor="gray")
plt.title("Histogram of AVG (Bins=30, Gray fill, Red edge)")
plt.show()

# %%
plt.figure(figsize=(8, 5))
sns.histplot(data=batting, x="avg", bins=30, edgecolor="white", facecolor="blue")
plt.title("Histogram of AVG (Bins=30, Blue fill, White edge)")
plt.show()

# %%
plt.figure(figsize=(8, 5))
sns.histplot(data=batting, x="avg", bins=30, edgecolor="white", facecolor="#53BFD4")
plt.title("Histogram of AVG (Bins=30, Hex fill, White edge)")
plt.show()

# %% [markdown]
# ## Bar Chart

# %%
# This is a Count Plot in Seaborn
plt.figure(figsize=(8, 5))
sns.countplot(data=batting, x="throw_bat")
plt.title("Bar Plot (Count) of throw_bat")
plt.show()

# %%
# Pre-summarized data example
bar_example = pd.DataFrame(
    {
        "throw_bat": ["우양", "우우", "우좌", "좌좌"],
        "count": [30, 1001, 155, 435],
    }
)
bar_example

# %%
# This is a Bar Plot of pre-calculated values in Seaborn
plt.figure(figsize=(8, 5))
sns.barplot(data=bar_example, x="throw_bat", y="count")
plt.title("Bar Plot (Identity) of throw_bat vs count")
plt.show()

# %%
# Ordering the bars by 'count' in descending order (order=-1)
order_list = bar_example.sort_values(by="count", ascending=False)["throw_bat"].tolist()
sns.barplot(data=bar_example, x="throw_bat", y="count", order=order_list)
plt.title("Bar Plot (Identity), ordered by count (descending)")
plt.show()

# %% [markdown]
# ## Line Chart

# %%
# Filter data
batting_rank_1 = batting[batting["rank"] == 1]

# %%
# Seaborn Line Plot
plt.figure(figsize=(8, 5))
sns.lineplot(data=batting_rank_1, x="year", y="avg")
plt.title("Line Plot of AVG vs Year (Rank 1 players)")
plt.show()

# %%
# Set line thickness ('size' is 'linewidth' in Matplotlib/Seaborn)
plt.figure(figsize=(8, 5))
sns.lineplot(data=batting_rank_1, x="year", y="avg", linewidth=3) # Use a visible thickness for example
plt.title("Line Plot of AVG vs Year (Linewidth=3)")
plt.show()

# %%
# Set line style ('linetype' is 'linestyle' in Matplotlib/Seaborn)
plt.figure(figsize=(8, 5))
sns.lineplot(data=batting_rank_1, x="year", y="avg", linestyle="--") # or 'dashed'
plt.title("Line Plot of AVG vs Year (Dashed linestyle)")
plt.show()

# %% [markdown]
# ## Point Chart

# %%
# Scatter Plot for geom_point
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=ryu,
    x="pitch_name",
    y="release_speed",
)
plt.title("Scatter Plot of Release Speed vs Pitch Name")
plt.show()

# %%
# Jitter is achieved by adding noise; Seaborn's `stripplot` with jitter can be an equivalent for categorical X
plt.figure(figsize=(8, 5))
sns.stripplot(
    data=ryu,
    x="pitch_name",
    y="release_speed",
    jitter=0.2, # Add horizontal jitter
)
plt.title("Strip Plot (Jitter) of Release Speed vs Pitch Name")
plt.show()

# %%
# Combine Violin Plot and Jitter (Strip Plot)
plt.figure(figsize=(10, 6))
sns.violinplot(
    data=ryu,
    x="pitch_name",
    y="release_speed",
    inner=None, # Remove inner box/lines for cleaner look
    color=".8"
)
sns.stripplot(
    data=ryu,
    x="pitch_name",
    y="release_speed",
    alpha=0.2,
    size=3,
    color="black"
)
plt.title("Violin Plot with Jittered Points")
plt.show()

# %%
# boxplot()
plt.figure(figsize=(8, 5))
sns.boxplot(
    data=ryu,
    x="pitch_name",
    y="release_speed",
)
plt.title("Box Plot of Release Speed vs Pitch Name")
plt.show()

# %%
# p + geom_point() (plate_x vs plate_z)
plt.figure(figsize=(6, 6))
sns.scatterplot(data=ryu, x="plate_x", y="plate_z")
plt.gca().set_aspect('equal', adjustable='box') # To mimic coord_fixed()
plt.title("Scatter Plot of Plate X vs Plate Z")
plt.show()

# %%
# p + geom_point() + facet_grid(x="pitch_name") + coord_fixed()
g = sns.FacetGrid(ryu, col="pitch_name", height=4, aspect=1) # height=4, aspect=1 for coord_fixed-like
g.map(sns.scatterplot, "plate_x", "plate_z")
g.set_titles(col_template="{col_name}")
plt.suptitle("Scatter Plot with Facet Grid (Pitch Name)", y=1.02)
plt.show()

# %%
# Seaborn uses `kdeplot` for 2D density; FacetGrid is for faceting.
g = sns.FacetGrid(ryu, col="pitch_name", row="stand", height=4, aspect=1)
g.map(sns.kdeplot, "plate_x", "plate_z", fill=True, levels=5, cmap="Reds")
g.set_titles(col_template="{col_name}", row_template="{row_name}")
plt.suptitle("2D Density Plot with Facet Grid", y=1.02)
plt.show()

# %%
# Conditional plot for 4-Seam Fastball and Changeup
ryu_filtered = ryu[ryu["pitch_name"].isin(["4-Seam Fastball", "Changeup"])]

# %%
# (p + geom_density2df() + geom_rect(...) + facet_grid(x="stand", y="pitch_name") + coord_fixed() + guides(fill="none"))
g = sns.FacetGrid(ryu_filtered, col="stand", row="pitch_name", height=4, aspect=1)
g.map(sns.kdeplot, "plate_x", "plate_z", fill=True, levels=5, cmap="Reds")
g.set_titles(col_template="{col_name}", row_template="{row_name}")

# %%
# To add geom_rect, we use Matplotlib's patches.Rectangle on each axes
from matplotlib.patches import Rectangle
for ax in g.axes.flat:
    # Adding a white dashed rectangle (representing a typical strike zone)
    ax.add_patch(
        Rectangle(
            xy=(-1, 1), # xmin, ymin
            width=2, # xmax - xmin = 1 - (-1)
            height=2, # ymax - ymin = 3 - 1
            color="white",
            alpha=0.1,
            fill=False,
            linestyle="--"
        )
    )
plt.suptitle("2D Density Plot with Strike Zone Rectangle", y=1.02)
plt.show()

# %%
# ggplot(batting, aes(x="avg", y="obp", shape="throw_bat")) + geom_point()
plt.figure(figsize=(8, 5))
sns.scatterplot(
    data=batting,
    x="avg",
    y="obp",
    style="throw_bat" # 'shape' is 'style' in Seaborn
)
plt.title("Scatter Plot of AVG vs OBP, shaped by throw_bat")
plt.show()

# %%
# p = ggplot(ryu, aes(x="release_speed")) + geom_density(color="gray")
plt.figure(figsize=(8, 5))
# Density Plot in Seaborn
sns.kdeplot(data=ryu, x="release_speed", color="gray", linewidth=2)
plt.title("Density Plot of Release Speed")
plt.show()

# p + facet_grid(y="pitch_name")
g = sns.FacetGrid(ryu, row="pitch_name", height=2, aspect=4)
g.map(sns.kdeplot, "release_speed", color="gray", linewidth=2)
g.set_titles(row_template="{row_name}")
plt.suptitle("Density Plot with Facet Grid (Pitch Name)", y=1.02)
plt.show()

# %%
# p + facet_grid(y="pitch_name", y_order=1)
# Note: Seaborn's FacetGrid/AxesSubplot does not have a direct `y_order` parameter for density plots.
# The order is determined by the categorical column's internal order (e.g., in the DataFrame/Series).
# You'd need to explicitly set the order for the categorical variable in the DataFrame before plotting.
pitch_order = ryu["pitch_name"].unique()[::-1] # Reverse the order for example

g = sns.FacetGrid(ryu, row="pitch_name", height=2, aspect=4, row_order=pitch_order)
g.map(sns.kdeplot, "release_speed", color="gray", linewidth=2)
g.set_titles(row_template="{row_name}")
plt.suptitle("Density Plot with Facet Grid (Ordered)", y=1.02)
plt.show()

# %%
# Create the Pandas DataFrame
df = pd.DataFrame({"x": list(range(-5, 6))})

# %%
# Define the normal distribution function (dnorm)
# Function definition is the same since it relies on scipy.stats

# p = ggplot(df, aes(x="x")) + geom_function(fun=dnorm)
# Seaborn/Matplotlib approach is to calculate y values and plot a line
x_values = np.linspace(df['x'].min(), df['x'].max(), 500)
y_values = norm.pdf(x_values)

# %%
plt.figure(figsize=(8, 5))
sns.lineplot(x=x_values, y=y_values, label="dnorm(x)")
plt.title("Line Plot of a Function (dnorm)")
plt.xlabel("x")
plt.ylabel("Probability Density")
plt.legend()
plt.show()

# %%
