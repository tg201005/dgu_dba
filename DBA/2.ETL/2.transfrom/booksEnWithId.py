import pandas as pd
import os

# 경로 설로
os.chdir(os.path.dirname(os.path.abspath(__file__)))

input = "booksEn.csv"
output = "booksEnWithId.csv"


def add_id_to_books(csv_file):
    # CSV 파일을 읽어 DataFrame으로 변환합니다.
    df = pd.read_csv(csv_file)

    # 'Book Title'을 기준으로 고유 ID 생성
    # 여기서는 'Book Title'의 순서대로 1부터 시작하는 ID를 부여합니다.
    # DataFrame의 맨 앞에 ID 컬럼을 추가합니다.
    df.insert(0, "ID", range(1, len(df) + 1))

    # ID가 추가된 DataFrame을 새로운 CSV 파일로 저장합니다.
    df.to_csv((output), index=False)

    return df


# 사용 예:

add_id_to_books(input)
