import os
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

# List of tables in the database in reverse dependency order
tables = [
    "PersonJobCategory",  # This table has foreign keys referencing Person and JobCategory
    "Recommendation",  # This table has foreign keys referencing Person and BookGroup
    "Book",  # This table has foreign keys referencing BookGroup and BookCategory
    "BookCategory",  # This table can be deleted safely after Book
    "BookGroup",  # This table can be deleted safely after Book
    "JobCategory",  # This table can be deleted safely after PersonJobCategory
    "Person",  # Base table
]


# Function to reset database tables
def reset_database():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Temporarily disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # Truncate each table
        for table in tables:
            cursor.execute(f"TRUNCATE TABLE {table};")
            print(f"Table {table} has been reset.")

        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        # Commit changes and close the connection
        connection.commit()
        connection.close()
        print("Database reset completed successfully.")
    except mysql.connector.Error as err:
        print(f"Database reset error: {err}")


if __name__ == "__main__":
    reset_database()
