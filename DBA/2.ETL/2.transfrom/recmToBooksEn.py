# mostrecommendedbooks.com/expertsRecmBooks.csv to booksEn.csv

import pandas as pd

import os

# Set the working directory
base_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_directory)


# File paths
input_csv = "../expertsRecmBooks.csv"
output_csv = "booksEn.csv"

# Read input CSV file
df = pd.read_csv(input_csv)

# Select desired columns
selected_columns = [
    "Book Title",
    "Subtitle",
    "Author",
    "Book Image URL",
    "Amazon Link",
    "Recommenders",
]
df_selected = df[selected_columns]

# Drop duplicates based on "Book Title" column
df_unique = df_selected.drop_duplicates(subset=["Book Title"])

# Save to output CSV file
df_unique.to_csv(output_csv, index=False)
