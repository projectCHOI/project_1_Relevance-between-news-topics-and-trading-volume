# pip install pandas matplotlib seaborn

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import seaborn as sns

# 파일 경로를 자신의 시스템에 맞게 수정하세요
file_path = 'path_to_your_excel_file.xlsx'

# Excel 파일 읽기
excel_data = pd.read_excel(file_path)

# 'Stock_Volume'을 숫자형으로 변환
excel_data['Stock_Volume'] = pd.to_numeric(excel_data['Stock_Volume'], errors='coerce')

# 날짜형으로 변환
excel_data['Date'] = pd.to_datetime(excel_data['Date'])

# 시각화 시작
fig, ax1 = plt.subplots(figsize=(12, 6))

# 주식 거래량 그래프 그리기
sns.lineplot(x='Date', y='Stock_Volume', data=excel_data, ax=ax1, color='black', label='Stock Volume')

# x축 설정
ax1.xaxis.set_major_locator(mdates.WeekdayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# 라벨과 제목 설정
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Volume', color='black')

# News 데이터를 위한 보조 y축 추가
ax2 = ax1.twinx()
sns.lineplot(x='Date', y='News', data=excel_data, ax=ax2, color='red', label='News')

# News y축 범위 설정
ax2.set_ylim(0, 10)
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
ax2.set_ylabel('News', color='red')

# 범례 추가
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

# 그래프 표시
plt.title('Stock Volume and News Over Time')
plt.show()
