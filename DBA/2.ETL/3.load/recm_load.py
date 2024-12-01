import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}

# File paths
experts_file = "./experts.csv"
recm_file = "./recm.csv"


# Function to load CSVs
def load_csv(file_path):
    return pd.read_csv(file_path).where(pd.notnull(pd.read_csv(file_path)), None)


# Function to process and insert recommendations
def process_and_insert_recommendations(experts_df, recm_df, connection):
    try:
        cursor = connection.cursor()

        # Map name_en to name_kr using experts.csv
        name_en_to_kr = {
            row["Name_en"]: row["Name_kr"] for _, row in experts_df.iterrows()
        }
        print(f"Mapped {len(name_en_to_kr)} name_en to name_kr.")

        # Fetch person_id using name_kr
        cursor.execute("SELECT person_id, name FROM Person")
        person_mapping = {row["name"]: row["person_id"] for row in cursor.fetchall()}
        print(f"Fetched {len(person_mapping)} person_id mappings.")

        # Fetch book_group_id using book title
        cursor.execute(
            "SELECT book_group_id, title FROM Book WHERE language = 'English'"
        )
        book_mapping = {row["title"]: row["book_group_id"] for row in cursor.fetchall()}
        print(f"Fetched {len(book_mapping)} book_group_id mappings.")

        successful_inserts = 0
        for _, row in recm_df.iterrows():
            try:
                # Map name_en to name_kr, then find person_id
                name_en = row["Person"]
                name_kr = name_en_to_kr.get(name_en)
                person_id = person_mapping.get(name_kr)

                if not person_id:
                    print(f"No person_id found for name_kr '{name_kr}'")
                    continue

                # Find book_group_id using Book Title
                book_title = row["Book Title_en"]
                book_group_id = book_mapping.get(book_title)

                if not book_group_id:
                    print(f"No book_group_id found for title '{book_title}'")
                    continue

                # Insert into Recommendation table
                reason = row["Recommendation Description"]
                cursor.execute(
                    """
                    INSERT INTO Recommendation (person_id, book_group_id, reason)
                    VALUES (%s, %s, %s)
                    """,
                    (person_id, book_group_id, reason),
                )
                successful_inserts += 1

            except Exception as e:
                print(f"Error processing row {row}: {e}")

        connection.commit()
        print(f"{successful_inserts} recommendations inserted successfully.")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()


# Main function
def main():
    try:
        # Connect to the database
        print("Connecting to the database...")
        connection = mysql.connector.connect(**db_config)
        print("Database connection established.")

        # Load CSVs
        print("Loading experts.csv and recm.csv...")
        experts_df = load_csv(experts_file)
        recm_df = load_csv(recm_file)

        # Process and insert recommendations
        print("\n--- Processing Recommendations ---")
        process_and_insert_recommendations(experts_df, recm_df, connection)

        # Close the connection
        connection.close()
        print("Database connection closed.")
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")


if __name__ == "__main__":
    main()
