import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

# Load environment variables from .env file
load_dotenv()

# Database configuration loaded from .env file
db_config = {
    "user": os.getenv("MYSQL_USER"),
    "password": "    ",
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),  # Default to 3306 if not specified
}

# Name of the database to create
database_name = os.getenv("MYSQL_DATABASE", "DBA")  # Default database name

# SQL statements for table creation
create_tables = {
    "Person": """
        CREATE TABLE Person (
            person_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            description TEXT,
            image_url VARCHAR(2083)
        );
    """,
    "JobCategory": """
        CREATE TABLE JobCategory (
            job_category_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        );
    """,
    "PersonJobCategory": """
        CREATE TABLE PersonJobCategory (
            person_id INT NOT NULL,
            job_category_id INT NOT NULL,
            PRIMARY KEY (person_id, job_category_id),
            FOREIGN KEY (person_id) REFERENCES Person(person_id),
            FOREIGN KEY (job_category_id) REFERENCES JobCategory(job_category_id)
        );
    """,
    "BookGroup": """
        CREATE TABLE BookGroup (
            book_group_id INT AUTO_INCREMENT PRIMARY KEY
        );
    """,
    "BookCategory": """
        CREATE TABLE BookCategory (
            book_category_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        );
    """,
    "Book": """
        CREATE TABLE Book (
            book_id INT AUTO_INCREMENT PRIMARY KEY,
            book_group_id INT NOT NULL,
            book_category_id INT NOT NULL,
            language VARCHAR(50),
            title VARCHAR(255),
            description TEXT,
            publication_year YEAR,
            image_url VARCHAR(2083),
            reference_book_id INT,
            FOREIGN KEY (book_group_id) REFERENCES BookGroup(book_group_id),
            FOREIGN KEY (book_category_id) REFERENCES BookCategory(book_category_id),
            FOREIGN KEY (reference_book_id) REFERENCES Book(book_id)
        );
    """,
    "Recommendation": """
        CREATE TABLE Recommendation (
            recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
            person_id INT NOT NULL,
            book_group_id INT NOT NULL,
            reason TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE (person_id, book_group_id),
            FOREIGN KEY (person_id) REFERENCES Person(person_id),
            FOREIGN KEY (book_group_id) REFERENCES BookGroup(book_group_id)
        );
    """,
}


# Function to create database
def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")


# Function to create tables
def create_database_tables():
    try:
        # Connect to the MySQL server
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Create the database if it doesn't exist
        create_database(cursor)

        # Select the database
        conn.database = database_name

        # Iterate through table creation statements
        for table_name, create_stmt in create_tables.items():
            try:
                cursor.execute(create_stmt)
                print(f"Table {table_name} created successfully.")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print(f"Table {table_name} already exists.")
                else:
                    print(f"Error creating table {table_name}: {err}")

        # Close cursor and connection
        cursor.close()
        conn.close()
        print("Database setup completed successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")


# Call the function to create tables
if __name__ == "__main__":
    create_database_tables()
