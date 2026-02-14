# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: ipynb,R:percent
#     text_representation:
#       extension: .R
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: R
#     language: R
#     name: ir
# ---

# %%
pacman::p_load(tidyverse, tidymodels)
set.seed(1234)

# %%
dt(x = 0, df = 1)

# %%
'19_20_uefa_big_5.csv' %>% 
  read.csv() %>% 
  as_tibble -> uefa_big5_match_results

# %%
uefa_big5_match_results %>%
  mutate(
    장소 = 장소 %>% fct_relevel('안방', '방문'),
    시기 = 시기 %>% fct_relevel('BC', 'AC')
  ) -> uefa_big5_match_results

# %%
uefa_big5_match_results %>% 
  filter(장소 == '안방' & 리그 != '리그1') -> uefa_big5_match_results_period  

# %%
uefa_big5_match_results_period %>% 
  group_by(팀, 시기) %>% 
  summarise(승률 = mean(승리), .groups = 'drop') -> uefa_big5_results_period

# %%
uefa_big5_results_period %>% 
  group_by(시기) %>% 
  summarise(승률 = mean(승률), .groups = 'drop') 

# %%
uefa_big5_results_period %>% 
  t_test(formula =  승률  ~  시기,
         order = c('AC', 'BC'),
         alternative = 'less')

# %%
uefa_big5_results_period %>% 
  t_test(formula =  승률  ~  시기,
         order = c('AC', 'BC'),
         alternative = 'less',
         var.equal = TRUE)

# %%
uefa_big5_results_period  %>% 
  group_by(시기) %>% 
  tally()

# %%
uefa_big5_results_period %>% 
  group_by(시기) %>% 
  summarise(평균승률 = mean(승률), 
            분산 = var(승률),
            개수 = n(),
            .groups = 'drop')

# %%
uefa_big5_results_period %>% 
  t_test(formula =  승률  ~  시기,
         order = c('AC', 'BC'),
         alternative = 'less')

# %%
(.421 - .439) / sqrt(.07697/78 + .0337/78)

# %%
(.4213370 - .4388944) / sqrt(.07693693/78 + .03368264/78)

# %%
uefa_big5_results_period %>% 
 specify(승률 ~ 시기) %>%
 hypothesize(null = 'independence') %>%
 generate(reps = 1000, type = 'permute') %>%
 calculate(stat = 'diff in means',
           order = c('AC', 'BC'))

# %%
uefa_big5_results_period %>% 
  specify(승률 ~ 시기) %>%
  hypothesize(null = 'independence') %>%
  calculate(stat = 't',
            order = c('AC', 'BC')) -> uefa_big5_results_period_null_theoretical

# %%
uefa_big5_results_period_null_theoretical

# %%
uefa_big5_results_period_null_theoretical %>% 
  visualize(method = 'theoretical')

# %%
uefa_big5_results_period_null_theoretical %>% 
  visualize(method = 'theoretical') +
  shade_p_value(obs_stat = -.466, direction = 'less')

# %%
uefa_big5_results_period %>% 
  specify(승률 ~ 시기) %>%
  calculate(stat = 't',
            order = c('AC', 'BC')) 

# %%
uefa_big5_results_period %>% 
  specify(승률 ~ 시기) %>%
  hypothesize(null = 'independence') %>%
  generate(reps = 1000, type = 'permute') %>%
  calculate(stat = 't',
            order = c('AC', 'BC')) %>% 
  visualize(method = 'both') +
  shade_p_value(obs_stat = -.466, direction = 'less')

# %%
uefa_big5_results_period %>%
  # Pivot to wide format to create a 'difference' column
  tidyr::pivot_wider(names_from = 시기, values_from = 승률) %>%
  mutate(diff = AC - BC) %>%
  # Now run a one-sample t-test on the difference
  t_test(response = diff, mu = 0, alternative = "less")

# %%
uefa_big5_results_period %>% 
  pivot_wider(names_from='시기', values_from='승률') %>% 
  mutate(차이 = AC - BC) %>% 
  summarise(차이_평균 = mean(차이),
            차이_표준편차 = sd(차이),
            차이_표준오차 = 차이_표준편차 / sqrt(78))     

# %%
-.0176 / .0286

# %%
uefa_big5_results_period %>% 
  specify(승률 ~ 시기) %>%
  hypothesize(null = 'point', mu = 0) %>%
  calculate(stat = 't',
            order = c('AC', 'BC')) %>% 
  visualize(method = 'theoretical') +
  shade_p_value(obs_stat = -.615, direction = 'less')

# %%
'19_20_nba.csv' %>% 
  read.csv() %>% 
  as_tibble -> nba_match_results

# %%
nba_match_results %>% 
  names()

# %%
nba_match_results %>% 
  mutate(
    장소 = 장소 %>% fct_relevel('안방', '방문'),
    시기 = 시기 %>% fct_relevel('BC', 'AC'),
    리그 = 리그 %>% fct_relevel('정규리그', '플레이오프')
  ) -> nba_match_results

# %%
nba_match_results %>%
  filter(리그 != '플레이오프') %>% 
  group_by(팀, 장소, 시기) %>%
  summarise(승률  = mean(승리), .groups = 'drop') %>%
  ggplot(aes(x = 장소, y = 승률)) +
  geom_boxplot() +
  facet_grid(. ~ 시기)

# %%
nba_match_results %>%
  filter(리그 != '플레이오프', 장소 == '안방') %>% 
  group_by(팀, 시기) %>%
  summarise(승률 = mean(승리), .groups = 'drop') %>%
  pivot_wider(names_from = 시기, values_from = 승률) %>%
  # Filter out teams that don't have data for both periods
  drop_na(BC, AC) %>% 
  mutate(diff = BC - AC) %>%
  t_test(response = diff, mu = 0)

# %%
nba_match_results %>%
  filter(리그 != '플레이오프') %>% 
  group_by(팀, 장소, 시기) %>%
  filter(장소 == '안방') %>% 
  summarise(승률  = mean(승리), .groups = 'drop') %>% 
  pivot_wider(names_from = '시기', values_from = '승률') %>% 
  drop_na()

# %%
nba_match_results %>%
  filter(리그 != '플레이오프', 장소 == '안방') %>% 
  group_by(팀, 시기) %>%
  summarise(승률 = mean(승리), .groups = 'drop') %>% 
  pivot_wider(names_from = 시기, values_from = 승률) %>% 
  drop_na(BC, AC) %>% 
  # 1. Create the difference column
  mutate(diff = BC - AC) %>% 
  # 2. Test if the mean difference is significantly different from 0
  t_test(response = diff, mu = 0)

# %%
nba_match_results %>%
  filter(시기 == 'BC') %>% 
  group_by(팀, 장소) %>%
  summarise(승률  = mean(승리), .groups = 'drop') %>% 
  specify(승률 ~ 장소) %>% 
  hypothesize(null = 'independence') %>%
  generate(reps = 1000, type = 'permute') %>%
  calculate(stat = 'diff in means',
            order = c('안방', '방문')) %>%
  select(stat) %>% 
  mutate(type = 'h0') -> nba_simulation_h0

# %%
nba_simulation_h0 %>%
  summarise(low = quantile(stat, .95))

# %%
nba_match_results %>%
  filter(시기 == 'BC') %>% 
  group_by(팀, 장소) %>%
  summarise(승률 = mean(승리),
            .groups = 'drop')  %>% 
  pivot_wider(names_from = '장소',
              values_from = '승률') %>% 
  mutate(차이 = 안방 - 방문) %>% 
  rep_sample_n(reps = 1000, size = 30, replace = TRUE) %>% 
  group_by(replicate) %>% 
  summarise(stat = mean(차이), .groups = 'drop') %>% 
  select(stat) %>% 
  mutate(type = 'h1') -> nba_simulation_h1

# %%
bind_rows(
  nba_simulation_h0,
  nba_simulation_h1
) %>% 
  ggplot(aes(x=stat, fill = type)) +
  geom_histogram(color = 'white',  
                 binwidth = .01, alpha = .5,
                 position = 'identity') +
  geom_vline(xintercept = .0747,
             linetype = 'dashed', lwd=1)

# %%
nba_simulation_h1 %>% 
  filter(stat > .0747) %>% 
  tally()

# %%
nba_match_results %>%
  filter(시기 == 'BC') %>% 
  group_by(팀, 장소) %>% 
  summarise(승률 = mean(승리), .groups = 'drop') %>% 
  # 1. Move '안방' and '방문' into their own columns
  tidyr::pivot_wider(names_from = 장소, values_from = 승률) %>% 
  # 2. Remove teams that don't have both Home and Away data (if any)
  tidyr::drop_na(안방, 방문) %>% 
  # 3. Calculate the difference
  mutate(diff = 안방 - 방문) %>% 
  # 4. Use the one-sample t_test on the difference
  t_test(response = diff, mu = 0)

# %%
pacman::p_load(pwr)

args(power.t.test)

# %%
nba_match_results %>%
  filter(시기 == 'BC') %>%
  group_by(팀, 장소) %>%
  summarise(승률 = mean(승리), .groups = 'drop') %>%
  group_by(장소) %>%
  summarise(승률 = mean(승률), .groups = 'drop')

# %%
nba_match_results %>%
  filter(시기 == 'BC') %>%
  group_by(팀, 장소) %>%
  summarise(승률 = mean(승리), .groups = 'drop') %>%
  pivot_wider(names_from = '장소', values_from = '승률') %>%
  mutate(차이 = 안방 - 방문) %>%
  summarise(sd = sd(차이))

# %%
power.t.test(delta = .106, sd = .158,
             sig.level = .05,
             power = .8,
             type = 'paired',
             alternative = 'one.sided')

# %%
