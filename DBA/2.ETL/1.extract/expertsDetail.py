from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import random
import csv
import os
from bs4 import BeautifulSoup

# Get the absolute path to the directory where the script is running
base_directory = os.path.dirname(os.path.abspath(__file__))

# Set the current working directory to the script's directory
os.chdir(base_directory)

# Load the experts list using pandas
experts_df = pd.read_csv("expertsLink.csv")

# Chrome WebDriver setup and execution
chrome_options = Options()
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
)
driver = webdriver.Chrome(options=chrome_options)


def extract_and_append_to_csv(soup, person_name):
    # Parse the HTML content

    # Extract the name and book recommendation count from the <h1> tag

    # Extract description and optional Wikipedia link
    description_paragraph = soup.find("p")
    description = (
        description_paragraph.text.split(".")[0] + "."
    )  # Simplified description extraction
    wikipedia_link = (
        description_paragraph.find("a", class_="styles_wikipedia-link__t4vA2")["href"]
        if description_paragraph.find("a", class_="styles_wikipedia-link__t4vA2")
        else ""
    )

    # Initialize social media links
    social_media = {"Instagram": "", "Twitter": "", "Youtube": "", "Homepage": ""}

    # Extract social media links
    social_media_div = soup.find("div", class_="styles_social-handles__D2jqN")
    if social_media_div:
        for a in social_media_div.find_all("a", href=True):
            href = a["href"]
            if "twitter.com" in href:
                social_media["Twitter"] = href
            elif "instagram.com" in href:
                social_media["Instagram"] = href
            elif "youtube.com" in href:
                social_media["Youtube"] = href
            elif "gatesnotes.com" in href:
                social_media["Homepage"] = href

    # Open the CSV file to append data
    csv_filename = "expertsDetail.csv"
    with open(csv_filename, "a", newline="", encoding="utf-8") as csv_file:
        fieldnames = [
            "Person Name",
            "Description",
            "Wikipedia Link",
            "Instagram",
            "Twitter",
            "Youtube",
            "Homepage",
        ]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Check if the file is empty to write the header
        csv_file.seek(0, os.SEEK_END)
        if csv_file.tell() == 0:
            csv_writer.writeheader()

        # Prepare data row as a dictionary to match the header
        data_row = {
            "Person Name": person_name,
            "Description": description,
            "Wikipedia Link": wikipedia_link,
            "Instagram": social_media["Instagram"],
            "Twitter": social_media["Twitter"],
            "Youtube": social_media["Youtube"],
            "Homepage": social_media["Homepage"],
        }

        # Write the data row
        csv_writer.writerow(data_row)


# Start processing from a specific expert
start_name = "Rand Paul"
start_processing = True

# Iterate over expert URLs and collect information
for index, row in experts_df.iterrows():
    if row["Name"] == start_name:
        start_processing = True

    if start_processing:
        print(
            f"Processing {row['Name']}..."
        )  # Print which expert is currently being processed
        full_url = row["Link"]
        driver.get(full_url)

        # Random delay to mimic human behavior
        time.sleep(random.uniform(0, 1))

        # Use WebDriverWait to ensure the page has loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "lxml")
        extract_and_append_to_csv(soup, row["Name"])

# Close the driver after task completion
driver.quit()
print("Data extraction complete.")
