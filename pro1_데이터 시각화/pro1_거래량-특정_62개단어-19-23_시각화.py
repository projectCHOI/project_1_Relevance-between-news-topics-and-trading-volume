import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import matplotlib.font_manager as fm

# 데이터 파일과 폰트 파일의 경로 설정
data_file_path = 'pro1_거래량-62키워드.csv'
font_file_path = 'NanumGothic.ttf'

# NanumGothic 폰트 설정
font_prop = fm.FontProperties(fname=font_file_path)
plt.rcParams['font.family'] = font_prop.get_name()

# CSV 파일 로드
df_full = pd.read_csv(data_file_path)
df_full['Date'] = pd.to_datetime(df_full['Date'])
df_full['Stock_Volume'] = df_full['Stock_Volume'].str.replace(',', '').astype(int)

# 시각화
fig, ax1 = plt.subplots(figsize=(12, 6))

# 주식 거래량 - 검은색 막대 그래프
ax1.bar(df_full['Date'], df_full['Stock_Volume'], color='black')
ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Volume', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.xaxis.set_major_locator(MaxNLocator(nbins=10))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# 키워드 추세 - 빨간색 꺾은선 그래프
ax2 = ax1.twinx()
for keyword in df_full.columns[2:]:
    ax2.plot(df_full['Date'], df_full[keyword], color='red', alpha=0.3)

ax2.set_ylabel('Keyword Frequency', color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# 날짜 레이블 회전
plt.xticks(rotation=45)

plt.title('Stock Volume and Keyword Trends Over Time')
plt.tight_layout()
plt.show()
