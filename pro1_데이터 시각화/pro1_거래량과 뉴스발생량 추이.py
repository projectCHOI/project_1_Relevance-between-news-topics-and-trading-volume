## 터미널 설치
# pip install pandas matplotlib yfinance
# python stock_analysis.py
# pip install yfinance

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import yfinance as yf

# 기사 데이터 로드
article_data = pd.read_csv('/content/drive/MyDrive/2.project_1_뉴스토픽 거래량 상관관계 구현/0_정리/2_수집1_[3조] s1_news.csv')
article_data['date'] = pd.to_datetime(article_data['date'])

# 일자별 기사 수 계산
daily_article_counts = article_data.groupby('date').size().reset_index(name='Article Count')

# S1 Corporation 주식 데이터 가져오기
symbol = "012750.KS"  # S1 Corporation 주식 심볼
start_date = "2019-01-01"
end_date = "2023-10-24"
try:
    s1_stock_data = yf.download(symbol, start=start_date, end=end_date)
except Exception as e:
    print(f"주식 데이터 다운로드 오류: {e}")
    # 적절하게 오류 처리

# 주식 거래량의 최고점 찾기 (상위 5%)
threshold = s1_stock_data['Volume'].quantile(0.95)
peak_points_stock = s1_stock_data[s1_stock_data['Volume'] >= threshold]

# 플로팅
fig, ax1 = plt.subplots(figsize=(12, 6))

# 기사 수 그래프 (빨간색)
ax1.plot(daily_article_counts['date'], daily_article_counts['Article Count'], color='red', label='Article Count')
ax1.set_xlabel('Date')
ax1.set_ylabel('Article Count', color='red')

# 주식 거래량 그래프 (검은색)
ax2 = ax1.twinx()
ax2.plot(s1_stock_data.index, s1_stock_data['Volume'], color='black', label='S1 Corporation Trading Volume')
ax2.scatter(peak_points_stock.index, peak_points_stock['Volume'], color='black', marker='o', s=20, label='Peak Points (Trading Volume, Top 5%)')
ax2.set_ylabel('Trading Volume', color='black')

# 범례 추가
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
ax1.legend(lines, labels, loc='upper left')

# 제목 설정
plt.title('Article Count and S1 Corporation Trading Volume (2019-01-01 ~ 2023-10-24)')

# 그래프 표시
plt.grid(True)
plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
plt.tight_layout()
plt.show()
