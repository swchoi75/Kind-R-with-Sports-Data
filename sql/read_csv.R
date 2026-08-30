library(readr)
library(here)


# File names
input_1 <- here("data", "international_soccer_matches_results.csv")
input_2 <- here("data", "soccer_matches_results_in_progress.csv")
input_3 <- here("data", "nba_draft_data.csv")

output_1 <- here("interim", "international_soccer_matches_results.csv")
output_2 <- here("interim", "soccer_matches_results_in_progress.csv")
output_3 <- here("interim", "nba_draft_data.csv")


# Read data (CP949)
my_locale <- locale(encoding = "CP949")

df_1 <- read_csv(input_1, locale = my_locale)
df_2 <- read_csv(input_2, locale = my_locale)
df_3 <- read_csv(input_3, locale = my_locale)


# Write data (UTF-8)
write_csv(df_1, output_1)
write_csv(df_2, output_2)
write_csv(df_3, output_3)