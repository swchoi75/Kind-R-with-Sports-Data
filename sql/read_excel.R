library(readxl)
library(readr)
library(here)

# Path & File names
input_file <- here("data", "kbo_team_slash_untidy.xlsx")
output_file <- here("data", "kbo_team_slash_untidy.csv")

# Read Excel file
df <- read_excel(input_file)

# Process DataFrame (필요 시 전처리 코드 작성)

# Write CSV file
write_csv(df, output_file)

cat(sprintf("A file is created: %s\n", output_file))