import polars as pl
from pyprojroot.here import here

# Path
path = here()


# File names
input_file = path / "data" / "kbo_team_slash_untidy.xlsx"
output_file = path / "data" / "kbo_team_slash_untidy.csv"

# Read Excel file
df = pl.read_excel(input_file)

# Process DataFrame

# Write combined Parquet file
df.write_csv(output_file)
print(f"A file is created: {output_file}")
