import pandas as pd

# Input file path
input_file = "/Users/leetaekwon/Desktop/DBA/2.ETL/3.load/experts.csv"
# Output file path for missing values
output_file_missing_values = (
    "/Users/leetaekwon/Desktop/DBA/2.ETL/3.load/missing_values.csv"
)

# Load the CSV file
df = pd.read_csv(input_file)

# Check for rows with missing values
missing_values_df = df[df.isna().any(axis=1)]

# Save the rows with missing values to a new file
missing_values_df.to_csv(output_file_missing_values, index=False)

print(f"Rows with missing values have been saved to {output_file_missing_values}")
