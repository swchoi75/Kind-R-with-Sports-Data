pacman::p_load(tidyverse, tidymodels)

set.seed(1234)

'19_20_uefa_big_5.csv' %>% 
  read.csv() %>% 
  as_tibble -> uefa_big5_match_results

uefa_big5_match_results %>% 
  glimpse()

uefa_big5_match_results %>%
  mutate(
    장소 = 장소 %>% fct_relevel('안방', '방문'),
    시기 = 시기 %>% fct_relevel('BC', 'AC')
  ) -> uefa_big5_match_results

uefa_big5_match_results %>%
  group_by(팀, 장소) %>%
  summarise(승률 = mean(승리), .groups = 'drop') -> uefa_big5_results

uefa_big5_results %>%
  ggplot(aes(x = 장소, y = 승률)) +
  geom_boxplot()

uefa_big5_results %>%
  group_by(장소) %>%
  summarise(승률 = mean(승률), .groups = 'drop')

sample(100, 10)

tibble(
  x = 1:6
) %>% 
  mutate(rest = x %% 2)

uefa_big5_results %>%
  rowwise() %>%
  mutate(난수 = sample(nrow(.), 1),
         랜덤_장소 = if_else(난수 %% 2 == 0, '안방', '방문')
  ) -> uefa_big5_results_permutated

uefa_big5_results_permutated

uefa_big5_results_permutated %>%
  pivot_longer(cols = c('장소', '랜덤_장소'),
               names_to = '구분',
               values_to = '장소') %>%
  group_by(팀, 구분, 장소) %>%
  summarise(승률 = mean(승률), .groups = 'drop') %>%
  ggplot(aes(x = 장소 %>% fct_relevel('안방', '방문'),
             y = 승률)) +
  geom_boxplot() +
  facet_grid(~구분)

uefa_big5_results_permutated %>%
  group_by(랜덤_장소) %>%
  summarise(승률 = mean(승률), .groups = 'drop')

uefa_big5_results %>%
  specify(response = 승률, explanatory = 장소)

uefa_big5_results %>%
  specify(formula = 승률 ~ 장소)

uefa_big5_results %>%
  specify(승률 ~ 장소) %>%
  hypothesize(null = 'independence')

uefa_big5_results %>%
  specify(승률 ~ 장소) %>%
  hypothesize(null = 'independence') %>%
  generate(reps=1000, type='permute')

uefa_big5_results %>%
  specify(승률 ~ 장소) %>%
  hypothesize(null = 'independence') %>%
  generate(reps = 1000, type = 'permute') %>%
  calculate(stat = 'diff in means',
            order = c('안방', '방문')) -> uefa_big5_results_null

uefa_big5_results_null %>%
  visualize()

uefa_big5_results_null %>%
  visualize() +
  geom_vline(xintercept = .128,
             color = '#53bfd4',
             lwd = 1)

uefa_big5_results_null %>%
  visualize() +
  geom_vline(xintercept = .05,
             color = '#53bfd4',
             lwd = 1)

uefa_big5_results_null %>%
  filter(stat >= .05)

uefa_big5_results %>%
  specify(formula = 승률 ~ 장소) %>%
  calculate(stat = 'diff in means',
            order=c('안방', '방문'))

uefa_big5_results_null %>%
  get_p_value(obs_stat = .128,
              direction = 'two-sided')

uefa_big5_results_null %>%
  visualize() +
  shade_p_value(obs_stat = .042,
                direction = 'two-sided')

uefa_big5_results_null %>%
  visualize() +
  shade_p_value(obs_stat = .128,
                direction = 'greater')

uefa_big5_results_null %>%
  visualize(fill = 'gray75') +
  shade_p_value(obs_stat = .05,
                direction = ‘two-sided’,
                fill = '#53bfd4', color = '#53bfd4')

uefa_big5_results_null %>%
  get_confidence_interval() -> uefa_big5_ci_endpoints

uefa_big5_results_null %>%
  visualize() +
  shade_p_value(obs_stat = .128,
                direction = 'greater') +
  shade_confidence_interval(endpoints = uefa_big5_ci_endpoints)

uefa_big5_match_results %>%
  filter(장소 == '안방' & 리그 != '리그1') -> uefa_big5_match_results_period

uefa_big5_match_results_period %>%
  group_by(팀, 시기) %>%
  summarise(승률 = mean(승리), .groups = 'drop') -> uefa_big5_results_period

uefa_big5_results_period %>%
  ggplot(aes(x = 시기, y = 승률)) +
  geom_boxplot()

uefa_big5_results_period %>%
  group_by(시기) %>%
  summarise(승률 = mean(승률), .groups = 'drop')

uefa_big5_results_period %>%
  specify(승률 ~ 시기) %>%
  hypothesize(null = 'independence') %>%
  generate(reps = 1000, type = 'permute') %>%
  calculate(stat = 'diff in means',
            order = c('AC', 'BC')) -> uefa_big5_results_period_null

uefa_big5_results_period_null %>%
  visualize() +
  shade_p_value(obs_stat = -.018,
                direction = 'less')

uefa_big5_results_period_null %>%
  get_p_value(obs_stat = -.018, direction = 'less')

uefa_big5_results_period %>%
  t_test(formula = 승률 ~ 시기,
         order = c('AC', 'BC'),
         alternative = 'less')