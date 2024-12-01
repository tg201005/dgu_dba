from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import csv
import time


# Set the output file name

input_file = "expertsLink.csv"
output_file = "expertsRecmBooks.csv"

# Setup the working directory based on the script's current location
base_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_directory)

# Load the experts list using pandas
experts_df = pd.read_csv(os.path.join(base_directory, input_file))

# Setup WebDriver
driver = webdriver.Chrome()




# Extract and save book data
def extract_books(expert_name, expert_url):
    driver.get(expert_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.styles_book-recommended-book-container__nJMaP")
        )
    )

    # Locate all book containers on the page
    book_containers = driver.find_elements(
        By.CSS_SELECTOR, "div.styles_book-recommended-book-container__nJMaP"
    )
    books = []

    for book in book_containers:
        title = book.find_element(By.TAG_NAME, "h3").text
        subtitle = book.find_element(By.TAG_NAME, "h4").text
        author = book.find_element(By.TAG_NAME, "h5").text
        image_url = book.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        amazon_link = book.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        recommendation_source = book.find_element(By.CSS_SELECTOR, "p").text
        recommenders = []

        recommender_links = driver.find_elements(
            By.CSS_SELECTOR, 'a[data-category="ShowRecommenders"]'
        )

        recommenders = []

        # Extract only the name of each recommender
        for link in recommender_links:
            name = link.text
            if name:  # Ensure there is a name before appending
                recommenders.append(name)  # Append only the name

        # print(f"recommeneders: {recommenders}")
        # Append book data to list
        books.append(
            {
                "Expert": expert_name,
                "Book Title": title,
                "Subtitle": subtitle,
                "Author": author,
                "Book Image URL": image_url,
                "Amazon Link": amazon_link,
                "Recommendation Source": recommendation_source,
                "Recommenders": ", ".join(recommenders),
            }
        )

    # Write to CSV
    csv_path = os.path.join(base_directory, output_file)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        if os.stat(csv_path).st_size == 0:  # check if file is empty to write header
            writer.writeheader()
        for book in books:
            writer.writerow(book)


def fill_empty_csv(file_path, field_names):
    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it and write the header
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()


# Fill empty CSV file
fill_empty_csv(
    output_file,
    [
        "Expert",
        "Book Title",
        "Subtitle",
        "Author",
        "Book Image URL",
        "Amazon Link",
        "Recommendation Source",
        "Recommenders",
    ],
)


# Iterate over each expert and extract book data

total_experts = len(experts_df)

flag = False
for index, row in experts_df.iterrows():
    if row["Name"] == "Sara Haines":
        flag = True

    if flag:
        full_url = row["Link"]

        import traceback

        try:
            extract_books(row["Name"], full_url)

        except Exception as e:
            # Log the error information to errorlog.txt
            with open("errorlog.txt", "a") as error_file:
                error_file.write(f"Error for expert {row["Name"]}: {str(e)}\n")
                traceback.print_exc(file=error_file)

    progress = ((index + 1) / total_experts) * 100
    print(
        f"Processing {index + 1}/{total_experts} ({progress:.2f}% complete): Expert {row['Name']}"
    )

    import random

    time.sleep(random.randrange(0, 1))  # Short delay to mimic human interaction

# Close the WebDriver
driver.quit()
print("All data has been extracted and saved.")
