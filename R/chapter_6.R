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
# ---

# %%
rm(list=ls())

# %%
pacman::p_load(tidyverse)

# %%
tribble(
  ~연도, ~이름, ~홈런, ~팀,
  2003, '이승엽', 56, '삼성',
  1999, '이승엽', 54, '삼성',
  2003, '심정수', 53, '현대',
  2015, '박병호', 53, '넥센',
  2014, '박병호', 52, '넥센',
  2015, '나바로', 48, '삼성',
  2002, '이승엽', 47, '삼성',
  2015, '테임즈', 47, 'NC',
  2020, '로하스', 47, 'KT',
  2002, '심정수', 46, '현대',
) -> 홈런

# %%
tribble(
  ~팀, ~애칭,
  '넥센', '히어로즈',
  '두산', '베어스',
  '롯데', '자이언츠',
  '삼성', '라이온즈',
  '한화', '이글스',
  'KIA', '타이거즈',
  'KT', '위즈',
  'LG', '트윈스',
  'NC', '다이노스',
  'SK', '와이번스'
) -> 팀

# %%
홈런 %>% inner_join(팀)

# %%
홈런 %>% left_join(팀)

# %%
홈런 %>% right_join(팀)

# %%
홈런 %>% full_join(팀)

# %%
홈런 %>% semi_join(팀)

# %%
홈런 %>% anti_join(팀)

# %%
tribble(
  ~구단, ~애칭,
  '넥센', '히어로즈',
  '두산', '베어스',
  '롯데', '자이언츠',
  '삼성', '라이온즈',
  '한화', '이글스',
  'KIA', '타이거즈',
  'KT', '위즈',
  'LG', '트윈스',
  'NC', '다이노스',
  'SK', '와이번스'
) -> 팀

# %%
홈런 %>% left_join(팀, by = c('팀' = '구단'))

# %%
'international_soccer_matches_results.csv' %>% 
  read.csv() %>% 
  as_tibble() -> results

results

# %%
results %>% 
  glimpse()  

# %%
results %>%
  select(
    date,
    team = away_team,
    opponent = home_team,
    team_score = away_score,
    opponent_score = home_score,
    tournament:last_col()
  ) -> results_away

results_away

# %%
tribble(
  ~a, ~b, ~c,
  1, 2, 3,
) -> tbl1

tbl1

# %%
tribble(
  ~a, ~b, ~c,
  4, 5, 6
) -> tbl2

tbl2

# %%
tbl1 %>% 
  bind_rows(tbl2)

# %%
results %>%
  rename(
    team = home_team,
    opponent = away_team,
    team_score = home_score,
    opponent_score = away_score
  ) %>%
  bind_rows(results_away) -> results

results

# %%
results %>%
  mutate(
    win = ifelse(team_score > opponent_score, 1, 0),
    draw = ifelse(team_score == opponent_score, 1, 0),
    lose = ifelse(team_score < opponent_score, 1, 0)
  ) %>%
  group_by(team) %>%
  summarise(
    wins = sum(win),
    draws = sum(draw),
    loses = sum(lose),
    matches = wins + draws + loses,
    win_percent = wins / matches,
    .groups = 'drop'
  ) %>%
  arrange(-wins)

# %%
results %>%
  mutate(
    win = ifelse(team_score > opponent_score, 1, 0),
    draw = ifelse(team_score == opponent_score, 1, 0),
    lose = ifelse(team_score < opponent_score, 1, 0)
  ) %>%
  group_by(team) %>%
  summarise(
    wins = sum(win),
    draws = sum(draw),
    loses = sum(lose),
    matches = wins + draws + loses,
    win_percent = wins / matches,
    .groups = 'drop'
  ) %>%
  arrange(-win_percent)

# %%
results %>%
  mutate(
    win = ifelse(team_score > opponent_score, 1, 0),
    draw = ifelse(team_score == opponent_score, 1, 0),
    lose = ifelse(team_score < opponent_score, 1, 0)
  ) %>%
  group_by(team, opponent) %>%
  summarise(
    wins = sum(win),
    draws = sum(draw),
    loses = sum(lose),
    matches = wins + draws + loses,
    win_percent = wins / matches,
    .groups = 'drop'
  ) %>%
  arrange(-wins)

# %%
results %>%
  mutate(
    win = ifelse(team_score > opponent_score, 1, 0),
    draw = ifelse(team_score == opponent_score, 1, 0),
    lose = ifelse(team_score < opponent_score, 1, 0)
  ) %>%
  group_by(team, opponent) %>%
  summarise(
    wins = sum(win),
    draws = sum(draw),
    loses = sum(lose),
    matches = wins + draws + loses,
    win_percent = wins / matches,
    .groups = 'drop'
  ) %>%
  filter(team == 'South Korea') %>%
  arrange(-wins)

# %%
'fifa_ranking.csv' %>% 
  read.csv() %>% 
  as_tibble() -> fifa_ranking

# %%
fifa_ranking %>% 
  glimpse()

# %%
fifa_ranking %>% 
  filter(country_full == 'South Korea')

# %%
fifa_ranking %>% 
  filter(country_full == 'Korea Republic')

# %%
results %>%
  filter(date >= '1993-08-08') %>%
  select(team) %>%
  distinct() -> results_countries

results_countries

# %%
fifa_ranking %>%
  select(country_full, country_abrv) %>%
  distinct() -> fifa_ranking_countries

fifa_ranking_countries

# %%
results_countries %>%
  left_join(fifa_ranking_countries,
            by = c('team' = 'country_full')) %>%
  filter(is.na(country_abrv) == TRUE) -> countries_to_match

countries_to_match

# %%
pacman::p_load(countrycode)

# %%
c('South Korea', 'Korea Republic') %>%
  countrycode(origin = 'country.name',
              destination = 'iso3c')

# %%
tribble(
  ~x, ~y, ~z,
  8, 1, 6,
  3, 5, 7,
  4, 9, 2,
) %>% 
  mutate(sum = sum(x, y, z))

# %%
tribble(
  ~x, ~y, ~z,
  8, 1, 6,
  3, 5, 7,
  4, 9, 2,
) %>% 
  rowwise() %>%
  mutate(sum = sum(x, y, z))

countries_to_match %>%
  rowwise() %>%
  mutate(country_abrv =
           countrycode(team,
                       origin = 'country.name',
                       destination = 'iso3c')) -> country_codes_result

# %%
results_countries %>%
  left_join(fifa_ranking_countries,
            by = c('team' = 'country_full')) %>% 
  bind_rows(country_codes_result) %>% 
  drop_na() -> country_code_result

country_code_result

# %%
results %>% 
  filter(date >= '1993-08-08') %>%
  left_join(country_code_result) %>% 
  left_join(fifa_ranking,
            by = c('country_abrv', 'date' = 'rank_date')) %>% 
  select(id:last_col())

# %%
results %>% 
  filter(date >= '1993-08-08') %>%
  left_join(country_code_result) %>% 
  left_join(fifa_ranking,
            by = c('country_abrv', 'date' = 'rank_date')) %>% 
  drop_na()

# %%
results %>%
  filter(date >= '1993-08-08') %>%
  left_join(country_code_result) %>%
  rename(team_abrv = country_abrv) %>%
  left_join(country_code_result,
            by = c('opponent' = 'team')) %>%
  rename(opponent_abrv = country_abrv)

# %%
results %>%
  filter(date > '1993-08-08') %>%
  left_join(country_code_result) %>%
  rename(team_abrv = country_abrv) %>%
  left_join(country_code_result,
            by = c('opponent' = 'team')) %>%
  rename(opponent_abrv = country_abrv) %>%
  drop_na() %>%
  write.csv('soccer_matches_results_in_progress.csv')

# %%
