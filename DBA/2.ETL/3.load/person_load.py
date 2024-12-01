import os
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

# Set environment variables for database configuration
os.environ["DB_USERNAME"] = "root"
os.environ["DB_PASSWORD"] = "    "
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "3306"
os.environ["DB_NAME"] = "DBA"

# Database configuration
db_config = {
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
}

# File path to the CSV file
input_file = "/Users/leetaekwon/Desktop/DBA/2.ETL/3.load/experts.csv"


# Function to clean and split job categories
def clean_and_split_jobs(field):
    if pd.isna(field):
        return []
    # Split by comma, strip whitespace, and remove duplicates
    jobs = [job.strip() for job in field.split(",")]
    print(f"Cleaned jobs: {jobs}")  # 디버깅용 출력
    return list(set(jobs))


# Function to insert Job Categories into the database
def insert_job_categories(df, connection):
    try:
        print("Extracting unique job categories...")
        # Extract unique job categories from Field_kr
        job_categories = set()
        for field in df["Field_kr"].dropna():
            job_categories.update(clean_and_split_jobs(field))

        print(f"Unique job categories extracted: {job_categories}")

        # Insert unique job categories into the database
        cursor = connection.cursor()
        for job in job_categories:
            cursor.execute("INSERT IGNORE INTO JobCategory (name) VALUES (%s)", (job,))
        connection.commit()
        print("JobCategory table populated successfully.")
    except Exception as e:
        print(f"Error inserting into JobCategory: {e}")


# Function to map Person to JobCategory in PersonJobCategory table
def insert_person_job_relationships(df, connection):
    try:
        cursor = connection.cursor()

        # Map Person names (KR) to IDs
        print("Fetching Person table data...")
        cursor.execute("SELECT person_id, name FROM Person")
        person_map = {name: person_id for person_id, name in cursor.fetchall()}
        print(f"Person map (KR): {person_map}")

        # Map JobCategory names to IDs
        print("Fetching JobCategory table data...")
        cursor.execute("SELECT job_category_id, name FROM JobCategory")
        job_category_map = {
            name: job_category_id for job_category_id, name in cursor.fetchall()
        }
        print(f"JobCategory map: {job_category_map}")

        # Debugging: Print matched relationships
        matched_relationships = []
        unmatched_jobs = set()

        print("Mapping Person to JobCategory...")
        # Insert relationships into PersonJobCategory
        for _, row in df.iterrows():
            person_id = person_map.get(row["Name_kr"])
            if person_id is None:
                print(f"Skipping {row['Name_kr']}: No matching Person found.")
                continue  # Skip if person is not found

            if pd.notna(row["Field_kr"]):
                job_categories = clean_and_split_jobs(row["Field_kr"])
                for job in job_categories:
                    job_category_id = job_category_map.get(job)
                    if job_category_id:
                        # Insert into PersonJobCategory
                        cursor.execute(
                            "INSERT IGNORE INTO PersonJobCategory (person_id, job_category_id) VALUES (%s, %s)",
                            (person_id, job_category_id),
                        )
                        matched_relationships.append(
                            (person_id, row["Name_kr"], job_category_id, job)
                        )
                    else:
                        unmatched_jobs.add(job)

        connection.commit()

        # Print matched relationships
        print(
            "Matched Relationships (person_id, Name_kr, job_category_id, JobCategory):"
        )
        for relationship in matched_relationships:
            print(relationship)

        # Print unmatched jobs
        if unmatched_jobs:
            print("Unmatched Job Categories:")
            print(unmatched_jobs)

        print("PersonJobCategory table populated successfully.")
    except Exception as e:
        print(f"Error inserting into PersonJobCategory: {e}")


# Main function
def main():
    try:
        print("Connecting to the database...")
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        print("Database connection established.")

        # Load the CSV file
        print(f"Loading CSV file from {input_file}...")
        df = pd.read_csv(input_file)
        print("CSV file loaded successfully.")
        print(df.head())

        # Insert Job Categories
        print("\n--- Starting JobCategory Insertion ---")
        insert_job_categories(df, connection)

        # Insert Person-Job Relationships
        print("\n--- Starting PersonJobCategory Insertion ---")
        insert_person_job_relationships(df, connection)

        # Close the connection
        connection.close()
        print("Database connection closed.")
        print("Data successfully loaded into JobCategory and PersonJobCategory tables.")
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")


if __name__ == "__main__":
    main()
