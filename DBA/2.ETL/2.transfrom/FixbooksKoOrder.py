import pandas as pd
import os

# booksKo의 column 매칭이 잘못되어 수정한 코드

# 작업 디렉토리 설정
base_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_directory)

# 데이터 파일 읽기
input_csv = "booksKo.csv"  # 이 부분을 실제 파일 이름으로 변경하세요.
output_csv = "booksKoWithId.csv"  # 이 부분을 실제 파일 이름으로 변경하세요.
data = pd.read_csv(input_csv)
# open("filtered_data.csv", "w").write(data.to_csv())

# print(data["Page URL"].str.contains("https://geni.us/", na=False))

# "Page URL"에 "https://geni.us/" 포함된 행 추출
filtered_data = data[data["Categories"].str.contains("https://geni.us/", na=False)]


filtered_data[["Author", "Original Title"]] = filtered_data[
    ["Original Title", "Author"]
]

# swap Intro Bottom, Image column
filtered_data[["Intro Bottom", "Image"]] = filtered_data[["Image", "Intro Bottom"]]

# swap Categories, Page URL column
filtered_data[["Categories", "Page URL"]] = filtered_data[["Page URL", "Categories"]]

filtered_data[["Original Title"]] = filtered_data[["Prod Title"]]
# print(filtered_data)

data.loc[filtered_data.index] = filtered_data

# data = data.drop(data.columns[0], axis=1)
# data = data.rename(columns={data.columns[0]: "Id"})
data.insert(0, "ID", range(1, len(data) + 1))

open(output_csv, "w").write(data.to_csv(index=False))
# # 결과 출력

print(filtered_data)
