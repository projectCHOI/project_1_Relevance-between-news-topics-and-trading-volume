import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = 'NanumGothic.ttf'  # 폰트 파일 경로
font_prop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = font_prop.get_name()

file_path = '특정_62개 단어.csv'
data = pd.read_csv(file_path)

data_for_plot = data.iloc[:, 1:-1]  # 첫 번째 열(날짜)과 마지막 열 제외
dates = pd.to_datetime(data['날짜'])  # '날짜' 열을 datetime으로 변환

# 그래프 그리기
plt.figure(figsize=(15, 10))
for column in data_for_plot.columns:
    plt.plot(dates, data_for_plot[column], marker='.', linestyle='-', label=column)

plt.xlabel('날짜')
plt.ylabel('빈도수')
plt.title('특정 단어들에 대한 날짜별 빈도수')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
