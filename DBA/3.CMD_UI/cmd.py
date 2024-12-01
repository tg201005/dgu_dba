import os
import pymysql
from dotenv import load_dotenv
from prettytable import PrettyTable
from collections import defaultdict

# .env 파일 로드
load_dotenv()

# 데이터베이스 설정
db_config = {
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}


# 데이터베이스 연결
def connect_db():
    return pymysql.connect(
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        database=db_config["database"],
        port=db_config["port"],
    )


# 결과를 페이지 네비게이션 방식으로 출력
def display_paginated_results(results, field_names):
    page_size = 15
    total_pages = (len(results) + page_size - 1) // page_size
    current_page = 0

    while True:
        start = current_page * page_size
        end = start + page_size
        page_results = results[start:end]

        # PrettyTable 출력
        table = PrettyTable()
        table.field_names = field_names
        for row in page_results:
            table.add_row(row)

        print("\n" + table.get_string())
        print(f"Page {current_page + 1} of {total_pages}")

        # 사용자 입력 대기
        print("Navigate: [w] Previous, [s] Next, [q] Quit")
        command = input("Enter command: ").strip().lower()

        if command == "w" and current_page > 0:
            current_page -= 1
        elif command == "s" and current_page < total_pages - 1:
            current_page += 1
        elif command == "q":
            break
        else:
            print("Invalid command. Please try again.")


# 1. 인물별 도서 추천 조회
def get_recommendations_by_person(person_name):
    query = """
    SELECT Person.name, BookGroup.book_group_id, Book.title, 
           CASE 
               WHEN Book.language = 'Korean' THEN 'kyobo'
               WHEN Book.language = 'English' THEN 'amazon'
               ELSE 'other'
           END AS Source,
           Recommendation.reason
    FROM Recommendation
    JOIN Person ON Recommendation.person_id = Person.person_id
    JOIN BookGroup ON Recommendation.book_group_id = BookGroup.book_group_id
    JOIN Book ON Book.book_group_id = BookGroup.book_group_id
    WHERE Person.name LIKE %s
    ORDER BY BookGroup.book_group_id, Book.title
    """
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute(query, (f"%{person_name}%",))
        results = cursor.fetchall()
    connection.close()

    if results:
        # 그룹화하지 않고 페이지 네비게이션만 적용
        display_paginated_results(
            results,
            [
                "Person",
                "Book Group ID",
                "Book Title",
                "Source",
                "Recommendation Reason",
            ],
        )
    else:
        print("No recommendations found for this person.")


# 2. 도서별 추천 인물 조회
def get_recommenders_by_book(book_title):
    query = """
    SELECT BookGroup.book_group_id, Book.title, 
           CASE 
               WHEN Book.language = 'Korean' THEN 'kyobo'
               WHEN Book.language = 'English' THEN 'amazon'
               ELSE 'other'
           END AS Source,
           Person.name, Recommendation.reason
    FROM Recommendation
    JOIN Person ON Recommendation.person_id = Person.person_id
    JOIN BookGroup ON Recommendation.book_group_id = BookGroup.book_group_id
    JOIN Book ON Book.book_group_id = BookGroup.book_group_id
    WHERE Book.title LIKE %s
    ORDER BY BookGroup.book_group_id, Book.title
    """
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute(query, (f"%{book_title}%",))
        results = cursor.fetchall()
    connection.close()

    if results:
        display_paginated_results(
            results,
            [
                "Book Group ID",
                "Book Title",
                "Source",
                "Person",
                "Recommendation Reason",
            ],
        )
    else:
        print("No recommenders found for this book.")


# 3. 직업별 가장 많은 추천을 받은 책 조회
def get_top_books_by_job_category(job_category_name):
    query = """
    SELECT JobCategory.name AS Job_Category, 
           BookGroup.book_group_id, 
           Book.title, 
           CASE 
               WHEN Book.language = 'Korean' THEN 'kyobo'
               WHEN Book.language = 'English' THEN 'amazon'
               ELSE 'other'
           END AS Source,
           COUNT(Recommendation.recommendation_id) AS Recommendation_Count
    FROM Recommendation
    JOIN Person ON Recommendation.person_id = Person.person_id
    JOIN PersonJobCategory ON Person.person_id = PersonJobCategory.person_id
    JOIN JobCategory ON PersonJobCategory.job_category_id = JobCategory.job_category_id
    JOIN BookGroup ON Recommendation.book_group_id = BookGroup.book_group_id
    JOIN Book ON Book.book_group_id = BookGroup.book_group_id
    WHERE JobCategory.name LIKE %s
    GROUP BY JobCategory.name, BookGroup.book_group_id, Book.title, Source
    ORDER BY Recommendation_Count DESC
    """
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute(query, (f"%{job_category_name}%",))
        results = cursor.fetchall()
    connection.close()

    if results:
        display_paginated_results(
            results,
            [
                "Job Category",
                "Book Group ID",
                "Book Title",
                "Source",
                "Recommendation Count",
            ],
        )
    else:
        print("No recommendations found for this job category.")


import os
import pymysql
from dotenv import load_dotenv
from prettytable import PrettyTable

# .env 파일 로드
load_dotenv()

# 데이터베이스 설정
db_config = {
    "user": os.getenv("DB_USERNAME"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3306)),
}


# 데이터베이스 연결
def connect_db():
    return pymysql.connect(
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        database=db_config["database"],
        port=db_config["port"],
    )


# 결과를 페이지 네비게이션 방식으로 출력
def display_paginated_results(results, field_names):
    page_size = 15
    total_pages = (len(results) + page_size - 1) // page_size
    current_page = 0

    while True:
        start = current_page * page_size
        end = start + page_size
        page_results = results[start:end]

        # PrettyTable 출력
        table = PrettyTable()
        table.field_names = field_names
        for row in page_results:
            table.add_row(row)

        print("\n" + table.get_string())
        print(f"Page {current_page + 1} of {total_pages}")

        # 사용자 입력 대기
        print("Navigate: [w] Previous, [s] Next, [q] Quit")
        command = input("Enter command: ").strip().lower()

        if command == "w" and current_page > 0:
            current_page -= 1
        elif command == "s" and current_page < total_pages - 1:
            current_page += 1
        elif command == "q":
            break
        else:
            print("Invalid command. Please try again.")


# 4. 가장 많은 추천을 받은 책들 조회
def get_most_recommended_books():
    query = """
    SELECT Book.title, 
           CASE 
               WHEN Book.language = 'Korean' THEN 'kyobo'
               WHEN Book.language = 'English' THEN 'amazon'
               ELSE 'other'
           END AS Source,
           COUNT(Recommendation.recommendation_id) AS Recommendation_Count
    FROM Recommendation
    JOIN BookGroup ON Recommendation.book_group_id = BookGroup.book_group_id
    JOIN Book ON Book.book_group_id = BookGroup.book_group_id
    GROUP BY Book.title, Source
    ORDER BY Recommendation_Count DESC
    """
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    connection.close()

    if results:
        display_paginated_results(
            results, ["Book Title", "Source", "Recommendation Count"]
        )
    else:
        print("No recommendations found.")


# 5. 가장 많은 추천을 한 인물들 조회
def get_most_active_recommenders():
    query = """
    SELECT Person.name, 
           COUNT(Recommendation.recommendation_id) AS Recommendation_Count
    FROM Recommendation
    JOIN Person ON Recommendation.person_id = Person.person_id
    GROUP BY Person.name
    ORDER BY Recommendation_Count DESC
    """
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    connection.close()

    if results:
        display_paginated_results(results, ["Person", "Recommendation Count"])
    else:
        print("No active recommenders found.")


# 6. 가장 많은 추천을 한 직업들 조회
def get_most_recommendations_by_job():
    query = """
    SELECT JobCategory.name AS Job_Category,
           COUNT(Recommendation.recommendation_id) AS Total_Recommendations,
           COUNT(DISTINCT Person.person_id) AS Total_Persons
    FROM Recommendation
    JOIN Person ON Recommendation.person_id = Person.person_id
    JOIN PersonJobCategory ON Person.person_id = PersonJobCategory.person_id
    JOIN JobCategory ON PersonJobCategory.job_category_id = JobCategory.job_category_id
    GROUP BY JobCategory.name
    ORDER BY Total_Recommendations DESC
    """
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    connection.close()

    if results:
        display_paginated_results(
            results, ["Job Category", "Total Recommendations", "Total Persons"]
        )
    else:
        print("No recommendations found by job category.")


# 명령줄 인터페이스
def main():
    while True:
        print("\nMenu:")
        print("1. 인물별 도서 추천 조회")
        print("2. 도서별 추천 인물 조회")
        print("3. 직업별 가장 많은 추천을 받은 책 조회")
        print("4. 가장 많은 추천을 받은 책들")
        print("5. 가장 많은 추천을 한 인물들")
        print("6. 가장 많은 추천을 한 직업들")
        print("7. 종료")
        choice = input("선택하세요: ")

        if choice == "1":
            person_name = input("인물 이름을 입력하세요: ")
            get_recommendations_by_person(person_name)
        elif choice == "2":
            book_title = input("도서 제목을 입력하세요: ")
            get_recommenders_by_book(book_title)
        elif choice == "3":
            job_category_name = input("직업 이름을 입력하세요: ")
            get_top_books_by_job_category(job_category_name)
        elif choice == "4":
            get_most_recommended_books()
        elif choice == "5":
            get_most_active_recommenders()
        elif choice == "6":
            get_most_recommendations_by_job()
        elif choice == "7":
            print("프로그램을 종료합니다.")
            break
        else:
            print("올바른 선택을 하세요.")


if __name__ == "__main__":
    main()
