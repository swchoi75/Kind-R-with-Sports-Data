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
import polars as pl
from lets_plot import *
from pyprojroot.here import here

# %%
# Path
path = here("Kind_R_with_Sports_data")

# %%
# Plot
LetsPlot.setup_html()

# %% [markdown]
# ## Histogram

# %%
batting = pl.read_csv("kbo_batting_qualified.csv")

# %%
ggplot(data=batting)

# %%
p = ggplot(data=batting, mapping=aes(x="avg"))

# %%
p + geom_histogram()

# %%
p + geom_histogram(binwidth=0.001)

# %%
p + geom_histogram(bins=30, fill="gray", color="red")

# %%
p + geom_histogram(bins=30, fill="rgb(0, 0, 255)", color="white")

# %%
p + geom_histogram(bins=30, fill="#53BFD4", color="white")

# %% [markdown]
# ## Bar

# %%
ggplot(batting, aes("throw_bat")) + geom_bar()

# %%
ggplot(batting, aes("throw_bat")) + geom_bar(stat="count")  # default

# %%
ggplot(batting, aes("throw_bat")) + geom_bar(stat="identity")  # average

# %%
ggplot(batting, aes(x="throw_bat", y="..count..")) + geom_bar()

# %%
bar_example = pl.DataFrame(
    {
        "throw_bat": ["우양", "우우", "우좌", "좌좌"],
        "count": [30, 1001, 155, 435],
    }
)

# %%
ggplot(bar_example, aes(x="throw_bat", y="count")) + geom_bar(stat="identity")

# %%
ggplot(bar_example, aes("throw_bat", "count")) + geom_bar(stat="identity")

# %%
ggplot(
    bar_example, aes(x=as_discrete("throw_bat", order_by="count", order=-1), y="count")
) + geom_bar(stat="identity")

# %% [markdown]
# ## Line

# %%
batting

# %%
batting_rank_1 = batting.filter(pl.col("rank") == 1)

# %%
p = ggplot(batting.filter(pl.col("rank") == 1), aes(x="year", y="avg"))

# %%
p + geom_line()

# %%
p + geom_line(size="1")

# %%
p + geom_line(linetype="dashed")

# %%
p + geom_line(linetype=2)

# %% [markdown]
# ## Point

# %%
ryu = pl.read_csv("2020_ryu.csv")
ryu.shape

# %%
ryu.columns

# %%
p = ggplot(
    ryu,
    aes(
        x=as_discrete("pitch_name", order_by="release_speed", order=1),
        y="release_speed",
    ),
)

# %%
p + geom_point()

# %%
p + geom_jitter()

# %%
p + geom_violin() + geom_jitter(alpha=0.2)

# %%
p + geom_boxplot()

# %%
p = ggplot(ryu, aes(x="plate_x", y="plate_z"))

# %%
p + geom_point()

# %%
p + geom_point() + facet_grid(x="pitch_name") + coord_fixed()

# %%
(
    p
    + geom_density2df()
    + facet_grid(x="pitch_name", y="stand")
    + coord_fixed()
    + guides(fill="none")
)

# %%
p = ggplot(
    ryu.filter(pl.col("pitch_name").is_in(["4-Seam Fastball", "Changeup"])),
    aes(x="plate_x", y="plate_z"),
)

# %%
(
    p
    + geom_density2df()
    + geom_rect(
        xmin=1, xmax=-1, ymin=1, ymax=3, color="white", alpha=0.1, linetype="dashed"
    )
    + facet_grid(x="stand", y="pitch_name")
    + coord_fixed()
    + guides(fill="none")
)

# %%
ggplot(batting, aes(x="avg", y="obp", shape="throw_bat")) + geom_point()

# %%
p = ggplot(ryu, aes(x="release_speed")) + geom_density(color="gray")

# %%
p

# %%
p + facet_grid(y="pitch_name")

# %%
p + facet_grid(y="pitch_name", y_order=1)

# %%
