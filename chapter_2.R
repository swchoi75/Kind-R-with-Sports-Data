# %%
library(dplyr)

# %%
mtcars[sample(1:nrow(mtcars), 10), ]

# %%
# mtcars %>%
#   sample_n()

# %%
# install.packages('tidyverse')

library('tidyverse')

# %%
# install.packages('pacman')

pacman::p_load(tidyverse, tidymodels)

# %%
batting <- read_csv('kbo_batting_qualified.csv')
batting

# %%
batting <- read_csv(
  'kbo_batting_qualified.csv',
  locale = locale('ko', encoding = 'utf-8'),
  show_col_types = FALSE
)
glimpse(batting)

# %%
batting

# %%
class(batting)

# %%
batting <- read.csv('kbo_batting_qualified.csv')

# %%
batting <- as_tibble(batting)

# %%
class(batting)

# %%
df1 <- data.frame(x = c(1, 2, 3), y = c(4, 5, 6))
df1

# %%
df2 <- tribble(
  ~x ,
  ~y ,
   #---|---
  1 ,
   4 ,
   2 ,
   5 ,
   3 ,
   6
)
df2

# %%
df2 <- read.csv(textConnection(
  "
x, y
1, 4
2, 5
3, 6
"
))
df2

# %%
1:10 %>% sum()

# %%
batting %>%
  print(n = 20)

# %%
'kbo_batting_qualified.csv' %>%
  read.csv() %>%
  as_tibble() -> batting
batting

# %%
