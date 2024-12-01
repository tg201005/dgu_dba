# # 0. booksEn.csv에서 pandas를 통해 데이터를 불러온다.
# # 1. 각 행을 순회한다.
# # 2. Book Title, Author 두 개의 필드를 불러온다.
# # 3. selinum을 활용하여 교보문고 사이트에 들어간다.
# # 4. 검색창에 "{book title}, {author}"를 입력하고 검색한다.
# # 5. 검색된 책들의 리스트를 가져온다.
# # 6. 그 책들 중 중 [국내도서]가 있는 li 요소가 있다면, 그 링크를 타고 들어간다.
# # 6.1 책 이있다면, Book Title ,Subtitle ,Author Name,Book Description,Book Image,Field,Book Seller Url, ISBN13의 데이터를 가져온다.
# # 6.2 가져온 데이터를 booksEn.csv에 추가한다.


# # 7. 없다면, [서양도서]가 있는 li 요소를 찾는다. li 요소가 있다면, 그 링크를 타고 들어간다.
# # 7.1 책 이있다면, Book Title ,Subtitle ,Author Name,Book Description,Book Image,Field,Book Seller Url, ISBN13의 데이터를 가져온다.
# # 7.2 가져온 데이터를 booksEn.csv에 추가한다.

# # 8. [국내도서]와 [서양도서]가 없다면, 기존 데이터를 booksKo.csv에 추가한다.
# # 9. 반복한다반


# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import os
# import csv

# # Set the working directory
# base_directory = os.path.dirname(os.path.abspath(__file__))
# os.chdir(base_directory)

# # Load data from booksEn.csv
# df = pd.read_csv("booksEn.csv")
# output_file = "booksKo.csv"
# total_books = len(df)

# # Setup Selenium WebDriver
# driver = webdriver.Chrome()

# # Open Kyobo website
# driver.get("https://www.kyobobook.co.kr/")


# def getAndAppendBookData(link):
#     driver.get(link)

#     import time

#     time.sleep(1)
#     # Define locators for the elements you want to wait for
#     # locators = [
#     #     (By.CSS_SELECTOR, ".prod_title"),
#     #     (By.CSS_SELECTOR, ".prod_desc"),
#     #     (By.CSS_SELECTOR, ".author"),
#     #     (By.CSS_SELECTOR, ".intro_bottom"),
#     #     (By.CSS_SELECTOR, ".portrait_img_box img"),
#     #     (By.CSS_SELECTOR, ".category_list_item"),
#     #     (By.CSS_SELECTOR, ".box_top caption-badge"),
#     # ]

#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, ".prod_desc"))
#     )
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, ".author"))
#     )
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, ".portrait_img_box img"))
#     )
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, ".category_list_item"))
#     )

#     # time.sleep(3)
#     try:
#         prod_title = driver.find_element(By.CSS_SELECTOR, ".prod_title").text
#         prod_desc = driver.find_element(By.CSS_SELECTOR, ".prod_desc").text
#         author = driver.find_element(By.CSS_SELECTOR, ".author").text

#         # author_info_btn 클래스를 가진 모든 <a> 태그 찾기
#         author_links = driver.find_elements(By.CLASS_NAME, "author_info_btn")

#         # 각 링크의 href 속성 저장
#         author_hrefs = []
#         for link in author_links:
#             try:
#                 href = link.get_attribute("href")
#                 # href 속성이 없는 경우 빈 문자열을 추가
#                 if href is None:
#                     href = ""
#             except Exception as e:
#                 print(f"Error retrieving href: {e}")
#                 href = ""
#             author_hrefs.append(href)

#         try:
#             intro_bottom = driver.find_element(By.CSS_SELECTOR, ".intro_bottom").text
#         except:
#             intro_bottom = ""
#         image = driver.find_element(
#             By.CSS_SELECTOR, ".portrait_img_box img"
#         ).get_attribute("src")
#         categories = [
#             elem.text
#             for elem in driver.find_elements(By.CSS_SELECTOR, ".category_list_item")
#         ]
#         page_url = driver.current_url
#         rating = driver.find_element(By.CSS_SELECTOR, ".caption-badge").text

#     except Exception as e:
#         print(f"Error for book {prod_title}: {str(e)}")
#         # import traceback

#         with open("errorlog.txt", "a") as error_file:
#             error_file.write(f"Error for book {prod_title}: {str(e)}\n")
#             traceback.print_exc(file=error_file)

#     booksKo = [
#         prod_title,
#         prod_desc,
#         author,
#         author_hrefs,
#         intro_bottom,
#         image,
#         ", ".join(categories),
#         page_url,
#         rating,
#     ]

#     print(f"bookKo: {booksKo}")
#     # Write to CSV

#     with open(output_file, "a", newline="", encoding="utf-8") as f:
#         writer = csv.writer(f, quoting=csv.QUOTE_ALL)

#         # Check if the file is empty to write the header
#         # This part requires checking the file size before opening it.
#         if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
#             pass  # File already exists and has content, do not write headers
#         else:
#             # Write header if the file is new or empty
#             writer.writerow(
#                 [
#                     "Prod Title",
#                     "Prod Desc",
#                     "Author",
#                     "Author Hrefs",
#                     "Intro Bottom",
#                     "Image",
#                     "Page URL",
#                     "Rating",
#                 ]
#             )

#         # Write the data row
#         writer.writerow(booksKo)


# # Example usage:


# # Iterate over each row
# for index, row in df.iterrows():
#     book_title = row["Book Title"]
#     author = row["Author"]

#     try:

#         # Find search input and enter book title and author
#         search_input = driver.find_element(By.CSS_SELECTOR, "#searchKeyword")
#         search_input.clear()
#         search_input.send_keys(f"{book_title}, {author}")
#         search_input.send_keys(Keys.RETURN)

#         # Wait for search results
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".prod_item"))
#         )
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, ".prod_item"))
#         )

#         # Get list of search results
#         search_results = driver.find_elements(By.CSS_SELECTOR, ".prod_item")

#         # Check if there are domestic books

#         notTranslation = True

#         for result in search_results:
#             if "국내도서" in result.text:
#                 notTranslation = False
#                 link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
#                 getAndAppendBookData(link)

#                 # Extract book details
#                 # You need to implement this part

#                 # Append extracted data to booksEn.csv
#                 # You need to implement this part

#                 break  # Exit loop if domestic book found

#         # if there is no domestic book
#         noEnBook = True
#         if notTranslation == True:
#             for result in search_results:
#                 if "서양도서" in result.text:
#                     notTranslation = False
#                     link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
#                     getAndAppendBookData(link)
#                     noEnBook = False

#                     break

#         if noEnBook == True and notTranslation == True:
#             # there is search en books results
#             link = (
#                 search_results[0].find_element(By.TAG_NAME, "a").get_attribute("href")
#             )
#             df.loc[index].to_csv("booksKo.csv", mode="a", header=False, index=False)

#             # Append existing data to booksKo.csv
#             # just copy the row to booksKo.csv

#             # Extract book details
#             # You need to implement this part

#             # Append extracted data to booksEn.csv
#             # You need to implement this part

#     except Exception as e:
#         import traceback

#         with open("errorlog.txt", "a") as error_file:
#             error_file.write(f"Error for expert {book_title}: {str(e)}\n")
#             traceback.print_exc(file=error_file)

#             # Append existing data to booksEn.csv
#             # You need to implement this part

#     # print(
#     #     f"Processed {index + 1}/{total_books} {(index + 1) * 100/total_books}% and book is {book_title} by {author}"
#     # )

# # Close Selenium WebDriver
# driver.quit()

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

# Set the working directory
base_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_directory)

# Load data from booksEn.csv
df = pd.read_csv("booksEn.csv")
output_file = "booksKo.csv"
total_books = len(df)

# Setup Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument(
    "--start-maximized"
)  # Start window maximized to prevent issues with element visibility.
driver = webdriver.Chrome(options=options)

# Open Kyobo website
driver.get("https://www.kyobobook.co.kr/")


def scroll_to_bottom(driver):
    # 페이지 높이 가져오기
    page_height = driver.execute_script("return document.body.scrollHeight")

    # 스크롤 다운을 반복하여 페이지 끝까지 이동
    while True:
        # 페이지 맨 아래까지 스크롤
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        # 페이지 로드 대기를 위해 잠시 대기
        time.sleep(1)
        # search_input = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".prod_item"))
        # )
        # 새로운 페이지 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")
        # 새로운 페이지 높이와 이전 페이지 높이가 같으면 더 이상 스크롤할 내용이 없으므로 반복 중지
        if new_height == page_height:
            break
        page_height = new_height


def getAndAppendBookData(link, type, original_title=""):
    driver.get(link)
    if type == "서양도서":
        # 모든 <li> 요소 가져오기
        li_elements = driver.find_elements(By.CSS_SELECTOR, ".prod_type_item")

        # 각 <li> 요소에서 텍스트와 링크 확인
        for li_element in li_elements:
            # <li> 요소에서 텍스트 가져오기
            text = li_element.text
            # "원서/번역서" 텍스트를 포함하는지 확인
            if "원서/번역서" in text:
                # <a> 요소에서 href 속성 가져오기
                link_element = li_element.find_element(
                    By.CSS_SELECTOR, ".btn_prod_type"
                )
                link = link_element.get_attribute("href")
                driver.get(link)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    " .author, .category_list_item",
                )
            )
        )

        def get_element_text(selector):
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            return elements[0].text if elements else ""

        def get_element_attribute(selector, attribute):
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            return elements[0].get_attribute(attribute) if elements else ""

        def get_rating_value():
            """
            Extracts and returns the rating value from a webpage where the rating is stored within
            a specific HTML structure.

            Args:
            driver (webdriver): Selenium WebDriver used to interact with the web page.

            Returns:
            float: The extracted rating value.
            """
            # Locate the element containing the rating value
            rating_element = driver.find_element(
                By.CSS_SELECTOR, "div.caption span.val"
            )

            # Extract the text from this element
            rating_value = rating_element.text

            # Convert to float and return
            return float(rating_value) if rating_value else 0.0

        # Now applying these helper functions
        prod_title = get_element_text(".prod_title")
        prod_desc = get_element_text(".prod_desc")
        author = get_element_text(".author")

        # Handling author links
        author_links = driver.find_elements(By.CLASS_NAME, "author_info_btn")
        author_hrefs = [
            link.get_attribute("href") if link.get_attribute("href") else ""
            for link in author_links
        ]

        intro_bottom = get_element_text(".intro_bottom")
        image = get_element_attribute(".portrait_img_box img", "src")
        categories = [
            elem.text
            for elem in driver.find_elements(By.CSS_SELECTOR, ".category_list_item")
        ]
        page_url = driver.current_url

        # Now applying these helper functions for the specific XPath you provided
        xpath_for_rating = (
            '//*[@id="ReviewList1"]/div[2]/div[1]/div[1]/div/div[3]/span/span[1]'
        )
        rating = get_rating_value()

        booksKo = [
            prod_title,
            prod_desc,
            original_title,
            author,
            author_hrefs,
            intro_bottom,
            image,
            ", ".join(categories),
            page_url,
            rating,
        ]
        write_to_csv(output_file, booksKo)

    except Exception as e:
        log_error(f"Error for book {prod_title}: {str(e)}")
        return 1  # Return 1 to increment error count
    return 0  # Return 0 if no error occurred


def write_to_csv(file_path, data):
    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        if os.path.getsize(file_path) == 0:
            writer.writerow(
                [
                    "Prod Title",
                    "Prod Desc",
                    "Original Title",
                    "Author",
                    "Author Hrefs",
                    "Intro Bottom",
                    "Image",
                    "Categories",
                    "Page URL",
                    "Rating",
                ]
            )
        writer.writerow(data)


def log_error(message):
    with open("errorlog.txt", "a") as error_file:
        error_file.write(message + "\n")


# Error tracking
import time
from datetime import datetime, timedelta


def update_time_tracking(
    start_time, iteration_start, iteration_times, index, total_books, error_count
):
    """
    Tracks the time per iteration, calculates the average, and prints status updates including
    start time, elapsed time, estimated completion time, and progress metrics.

    Args:
    start_time (float): The time when the process started.
    iteration_start (float): The start time of the current iteration.
    iteration_times (list): List of times taken for each iteration.
    index (int): The current index in the loop.
    total_books (int): Total number of books to process.
    error_count (int): Current count of errors encountered.

    Returns:
    None
    """
    iteration_end = time.time()  # End time of the current iteration
    iteration_duration = iteration_end - iteration_start
    iteration_times.append(iteration_duration)
    average_time_per_iteration = sum(iteration_times) / len(iteration_times)

    elapsed_time = iteration_end - start_time
    estimated_total_time = average_time_per_iteration * (total_books - index)
    estimated_time_remaining = estimated_total_time - elapsed_time

    progress_percentage = ((index + 1) / total_books) * 100
    error_rate = (error_count / (index + 1)) * 100

    # Format the start and estimated finish times
    start_time_formatted = datetime.fromtimestamp(start_time).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    estimated_end_time = datetime.now() + timedelta(seconds=estimated_time_remaining)
    estimated_end_time_formatted = estimated_end_time.strftime("%Y-%m-%d %H:%M:%S")

    print(
        f"--- Status Update ---\n"
        f"Start Time: {start_time_formatted}. \n"
        f"Processed {index + 1}/{total_books} ({progress_percentage:.2f}%) with an error rate of {error_rate:.2f}%. \n"
        f"Elapsed time: {elapsed_time:.2f}s, Estimated time remaining: {estimated_time_remaining:.2f}s, \n"
        f"Estimated end time: {estimated_end_time_formatted}. \n"
        f"Average time per iteration: {average_time_per_iteration:.2f}s.\n"
    )


def transform_and_write_csv(row, output_filepath):
    # Open the input CSV file A
    # Open the output CSV file B
    with open(output_filepath, mode="a", newline="", encoding="utf-8") as outfile:
        fieldnames = [
            "Prod Title",
            "Prod Desc",
            "Original Title",
            "Author",
            "Author Hrefs",
            "Intro Bottom",
            "Image",
            "Categories",
            "Page URL",
            "Rating",
            "Prod Title",
            "Prod Desc",
            "Original Title",
            "Author",
            "Author Hrefs",
            "Intro Bottom",
            "Image",
            "Categories",
            "Page URL",
            "Rating",
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

        # # Write the header to the output file
        # writer.writeheader()

        # Iterate through each row in the input CSV file
        # Transform data from A to B format and write to B
        new_row = {
            "Prod Title": row["Book Title"],
            "Prod Desc": row["Subtitle"],
            "Original Title": row["Book Title"],
            "Author": row["Author"],
            "Image": row["Book Image URL"],
            "Page URL": row["Amazon Link"],
            "Author Hrefs": "",  # Assuming no data available, left as empty string
            "Intro Bottom": "",  # Assuming no data available, left as empty string
            "Categories": "",  # Assuming no data available, left as empty string
            "Rating": "",  # Assuming no data available, left as empty string
        }
        writer.writerow(new_row)


# Example usage of the function would require setting up start_time and other variables
start_time = time.time()
iteration_times = []
error_count = 0
total_books = len(df)


# you are the placebo
last_book = "Preparing for Christmas"
start = False
# Iterate over each row
for index, row in df.iterrows():
    if last_book == "":
        start = True

    if row["Book Title"] == last_book:
        start = True
        continue

    if not start:
        continue

    iteration_start = time.time()  # Start timing this iteration

    book_title = row["Book Title"]
    author = row["Author"]
    subtitle = row["Subtitle"]
    try:
        if "https://mmbr.kyobobook.co.kr/login?" in driver.current_url:
            driver.get("https://www.kyobobook.co.kr")

        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#searchKeyword"))
        )
        search_input.clear()
        search_input.send_keys(f"{book_title}, {author}")
        search_input.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".prod_item"))
        )

        # 애초에 검색 결과가 없는 경우

        for list in driver.find_elements(By.CSS_SELECTOR, ".title_heading"):
            if "혹시 아래 상품을 찾으셨나요?" in list.text:
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#searchKeyword"))
                )
                search_input.clear()

                search_input.send_keys(
                    f"{book_title}, {subtitle if not pd.isnull(subtitle) else author}"
                )
                search_input.send_keys(Keys.RETURN)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".prod_item"))
                )
                break

        noBook = False
        for list in driver.find_elements(By.CSS_SELECTOR, ".title_heading"):
            if "혹시 아래 상품을 찾으셨나요?" in list.text:

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".prod_item"))
                )
                noBook = True
                break

        scroll_to_bottom(driver)

        search_results = driver.find_elements(By.CSS_SELECTOR, ".prod_item")
        domestic_found = False

        # First check for 국내도서
        if not noBook:
            for result in search_results:
                if "국내도서" in result.text:
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                    error_count += getAndAppendBookData(
                        link,
                        type="국내도서",
                        original_title=book_title,
                    )
                    domestic_found = True
                    noBook = False
                    break  # Break after processing 국내도서

        # Check for 서양도서 only if no 국내도서 was found
        if not domestic_found and not noBook:
            for result in search_results:
                if "서양도서" in result.text:
                    link = result.find_element(By.TAG_NAME, "a").get_attribute("href")

                    error_count += getAndAppendBookData(
                        link, type="서양도서", original_title=book_title
                    )
                    noBook = False
                    break

        # If no book was found, write the existing data to the output file
        if noBook:
            transform_and_write_csv(row, output_file)

    except Exception as e:
        log_error(f"Error for book : {book_title},  {index}: {str(e)}")
        error_count += 1

    # Calculate and display progress and error rate
    update_time_tracking(
        start_time, iteration_start, iteration_times, index, total_books, error_count
    )


driver.quit()
