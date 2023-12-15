import requests
from bs4 import BeautifulSoup
import pandas as pd

# 주식의 종목 코드를 입력 받기
keyword = input("찾는 주식의 종목코드를 알려주세요: ")

# 리스트 생성
data_list = []

for page_url in range(1, 10):
    # range(x, y) x부터 y까지 페이지 변경한다. 필요한만큼 변경

    url = f'https://finance.naver.com/item/sise_day.naver?code={keyword}&page={page_url}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)

    page_content = response.text
    soup = BeautifulSoup(page_content, 'html.parser')

    for data in soup.select('table.type2 tr'):
        if len(data.select('td')) >= 7:
            date = data.select('td')[0].text
            stock_price_open = data.select('td')[1].text
            stock_volume = data.select('td')[6].text  # 추가~

            data_list.append([date, stock_price_open, stock_volume])

# 결과를 DataFrame으로 넣는다.
result = pd.DataFrame(data_list, columns=['Date', 'Stock_Price_Open', 'Stock_Volume'])

# 데이터만 뽑을 경우.
df = pd.DataFrame(result)
print(df)

# CSV로 만들 경우.
# df.to_csv(f'{keyword}_data.csv', index=False)

# 하나만 출력해야 잘 된다.