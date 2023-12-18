# 라이브러리 설치 확인
# pip install pandas yfinance
# python keyword_analysis.py
# !pip install yfinance pandas

import pandas as pd

# 데이터 로드 (경로 확인 필요)
data = pd.read_csv('news.csv')  # 로컬 파일 경로로 수정
data['date'] = pd.to_datetime(data['date'])  # 날짜 형식 변환

# 제공된 키워드 리스트
keywords = ["에스원", "추가"]

# 지정된 기간 설정
start_date = '2019-01-01'
end_date = '2023-10-24'
filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# 결과를 저장할 빈 DataFrame 생성 및 초기화
date_range = pd.date_range(start=start_date, end=end_date)
result_df = pd.DataFrame(index=date_range, columns=keywords + ['기사 합산'])
result_df = result_df.fillna(0)  # 모든 값을 0으로 초기화

# 각 날짜와 키워드 조합에 대해 포함된 기사의 개수를 확인
for date in date_range:
    daily_data = filtered_data[filtered_data['date'] == date]
    for keyword in keywords:
        count = daily_data['title'].str.contains(keyword, case=False, na=False).sum()
        result_df.at[date, keyword] = count
    result_df.at[date, '기사 합산'] = result_df.loc[date, keywords].sum()

# 결과 출력
print(result_df)
result_df