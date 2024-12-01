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
books_en_file = "/Users/leetaekwon/Desktop/DBA/2.ETL/3.load/books_en.csv"
books_kr_file = "/Users/leetaekwon/Desktop/DBA/2.ETL/3.load/books_kr.csv"


# Function to insert English books
def insert_english_books(df, connection):
    """Insert English books into the database."""
    try:
        cursor = connection.cursor()

        # Clean NaN values
        df = df.where(pd.notnull(df), None)

        for _, row in df.iterrows():
            # Insert into BookGroup to create a new group ID
            cursor.execute("INSERT INTO BookGroup () VALUES ()")
            book_group_id = cursor.lastrowid  # Get the generated book_group_id

            # Insert into Book table
            cursor.execute(
                """
                INSERT INTO Book (book_group_id, book_category_id, language, title, description, image_url, author)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    book_group_id,  # Book group ID
                    1,  # Default category ID
                    "English",  # Language
                    row["Title"],  # Book title
                    row["Subtitle"],  # Book description
                    row["Image"],  # Book image URL
                    row["Author"],  # Book author
                ),
            )
        connection.commit()
        print(f"{len(df)} English books inserted successfully.")
    except mysql.connector.Error as e:
        print(f"Error inserting English books: {e}")
    finally:
        cursor.close()


# Function to insert Korean books
def insert_korean_books(df, connection):
    """Insert Korean books into Book table by matching Original Title with English books."""
    try:
        cursor = connection.cursor()

        # Fetch existing English books and their group IDs
        print("Fetching English books from the database...")
        cursor.execute(
            "SELECT book_group_id, title FROM Book WHERE language = 'English'"
        )
        english_books = {
            title.strip(): group_id for group_id, title in cursor.fetchall()
        }
        print(f"Loaded {len(english_books)} English book titles for matching.")

        unmatched_books = []
        successful_inserts = 0

        print("Starting to match and insert Korean books...")
        for _, row in df.iterrows():
            try:
                original_title = (
                    row["Original Title"].strip()
                    if pd.notnull(row["Original Title"])
                    else None
                )

                if original_title in english_books:
                    book_group_id = english_books[original_title]
                    print(
                        f"Match found: '{original_title}' -> book_group_id {book_group_id}"
                    )

                    # Insert Korean book into Book table
                    cursor.execute(
                        """
                        INSERT INTO Book (book_group_id, book_category_id, language, title, description, image_url, author)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            book_group_id,  # Matched group ID
                            1,  # Default category ID
                            "Korean",  # Language
                            row["Prod Title"],  # Book title in Korean
                            row["Prod Desc"],  # Description in Korean
                            row["Image"],  # Book image URL
                            row["Author"],  # Book author
                        ),
                    )
                    successful_inserts += 1
                else:
                    unmatched_books.append(original_title)
                    print(f"No match found for: '{original_title}'")

            except Exception as e:
                # Log the error and continue with the next record
                print(
                    f"Error inserting record for Original Title '{original_title}': {e}"
                )

        connection.commit()
        print(f"{successful_inserts} Korean books inserted successfully.")

        if unmatched_books:
            print(
                f"{len(unmatched_books)} Korean books could not be matched to an English book:"
            )
            print(unmatched_books)

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        cursor.close()


# Main function for inserting books
def main():
    try:
        # Connect to the database
        print("Connecting to the database...")
        connection = mysql.connector.connect(**db_config)
        print("Database connection established.")

        # Load English books CSV
        print(f"Loading English books from {books_en_file}...")
        books_en = pd.read_csv(books_en_file)
        print(f"English books loaded successfully. Total records: {len(books_en)}")

        print("\n--- Inserting English Books ---")
        insert_english_books(books_en, connection)

        # Load Korean books CSV
        print(f"Loading Korean books from {books_kr_file}...")
        books_kr = pd.read_csv(books_kr_file)
        print(f"Korean books loaded successfully. Total records: {len(books_kr)}")

        print("\n--- Inserting Korean Books ---")
        insert_korean_books(books_kr, connection)

        # Close the connection
        connection.close()
        print("Database connection closed.")
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")


if __name__ == "__main__":
    main()
