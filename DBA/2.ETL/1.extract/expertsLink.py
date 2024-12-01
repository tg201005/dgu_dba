import csv
import os
import requests
from bs4 import BeautifulSoup

# Get the absolute path to the directory where the script is running
base_directory = os.path.dirname(os.path.abspath(__file__))

# Set the current working directory to the script's directory
os.chdir(base_directory)

# URL of the page to scrape
target_url = "https://www.mostrecommendedbooks.com/people"

# Make an HTTP GET request to the specified URL
response = requests.get(target_url)
if response.status_code != 200:
    print("Failed to retrieve the page")
    exit()

# Use the content of the response to create a BeautifulSoup object
soup = BeautifulSoup(response.content, "lxml")

# Open a CSV file to write the data, specifying the path using the base directory
csv_file_path = os.path.join(base_directory, "expertsLink.csv")
with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Name", "Link", "Number of Books", "Image URL"])

    # Parse the HTML
    for anchor in soup.find_all("a", href=True):
        list_item = anchor.find("li")
        print(list_item)
        print(f"-----------------")
        if list_item:
            person_name = (
                list_item.find("h3").text if list_item.find("h3") else "No Name"
            )
            person_link = "https://www.mostrecommendedbooks.com" + anchor["href"]
            #
            try:
                print(list_item.find("p").text.split(" ")[1])
                book_count = (
                    list_item.find("p").text.split(" ")[1]
                    if list_item.find("p")
                    else "0"
                )
            except:
                print(f"Error in book count for {person_name}")
            image_tag = list_item.find("img")
            image_url = image_tag["src"] if image_tag else ""

            # Write to CSV
            csv_writer.writerow([person_name, person_link, book_count, image_url])

print("Data extraction complete.")

# -------
# above code is to extract the data from the URL
# below code is download image from the URL

# import csv
# import os
# import requests
# from bs4 import BeautifulSoup

# # URL of the page to scrape
# target_url = "https://www.mostrecommendedbooks.com/people"

# # Make an HTTP GET request to the specified URL
# response = requests.get(target_url)
# if response.status_code != 200:
#     print("Failed to retrieve the page")
#     exit()

# # Use the content of the response to create a BeautifulSoup object
# soup = BeautifulSoup(response.content, "lxml")

# # Ensure the directory for images exists
# os.makedirs("expert_images", exist_ok=True)

# # Open a CSV file to write the data
# with open("experts.csv", "w", newline="", encoding="utf-8") as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(["Name", "Link", "Number of Books", "Image Filename"])

#     # Parse the HTML
#     for anchor in soup.find_all("a", href=True):
#         list_item = anchor.find("li")
#         if list_item:
#             person_name = (
#                 list_item.find("h3").text if list_item.find("h3") else "No Name"
#             )
#             person_link = anchor["href"]
#             book_count = (
#                 list_item.find("p").text.split(" ")[0] if list_item.find("p") else "0"
#             )
#             image_tag = list_item.find("img")
#             image_src = image_tag["src"] if image_tag else ""
#             image_alt = (
#                 image_tag["alt"] if image_tag and image_tag.has_attr("alt") else "image"
#             )

#             # Save image
#             image_filename = f"expert_{image_alt.replace(' ', '_')}.jpg"
#             image_path = os.path.join("expert_images", image_filename)
#             if image_src:
#                 image_response = requests.get(image_src)
#                 if image_response.status_code == 200:
#                     with open(image_path, "wb") as image_file:
#                         image_file.write(image_response.content)
#                 else:
#                     print(f"Failed to download image from {image_src}")

#             # Write to CSV
#             csv_writer.writerow([person_name, person_link, book_count, image_filename])

# print("Data extraction and image download complete.")
