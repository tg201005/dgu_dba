import pandas as pd

# File paths
input_file = "/Users/leetaekwon/Desktop/DBA/2.ETL/3.load/experts.csv"
output_file = "/Users/leetaekwon/Desktop/DBA/2.ETL/3.load/job_categories.csv"

# Load the CSV file
df = pd.read_csv(input_file)

# Extract 'Field_kr' column and split jobs by comma
fields = df["Field_kr"].dropna().str.split(",")

# Flatten the list and remove duplicates
unique_jobs = sorted(set([job.strip() for sublist in fields for job in sublist]))

# Create a DataFrame for unique jobs
job_df = pd.DataFrame(unique_jobs, columns=["JobCategory"])

# Save the result to a new CSV file
job_df.to_csv(output_file, index=False)

print(f"Job categories extracted and saved to {output_file}")
