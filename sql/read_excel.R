library(readxl)
library(readr)
library(here)

# Path & File names
input_file <- here("data", "kbo_team_slash_untidy.xlsx")
output_1 <- here("interim", "kbo_team_slash_untidy.csv")
output_2 <- here("interim", "kbo_team_slash_tidy.csv")

# Read Excel file
df_untidy <- read_excel(input_file)

# Process DataFrame (필요 시 전처리 코드 작성)
df_tidy <- df_untidy %>%
  fill(팀, .direction = 'up') %>%
  pivot_longer(
    cols = `1982`:`2020`,
    names_to = '연도',
    values_to = '기록'
  )


# Write CSV file
write_csv(df_untidy, output_1)
write_csv(df_tidy, output_2)

print("Files are created")