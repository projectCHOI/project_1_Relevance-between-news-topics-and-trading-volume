import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_news_list(keyword, startdate, enddate, max_pages=50):
    li = []
    h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

    for d in pd.date_range(startdate, enddate):
        str_d = d.strftime("%Y.%m.%d")
        page = 1
        print(str_d)

        while True:
            start = (page - 1) * 10 + 1
            print(page)
            URL = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={0}&sort=2&photo=0&field=0&pd=3&ds={1}&de={2}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{3}to{4},a:all&start={5}".format(keyword, startdate, enddate, startdate.replace(".", ""), enddate.replace(".", ""), start)

            res = requests.get(URL, headers=h)
            soup = BeautifulSoup(res.text, "html.parser")

            if soup.select_one(".api_noresult_wrap") or page > max_pages:
                break

            news_list = soup.select("ul.list_news li")

            for item in news_list:
                if len(item.select("div.info_group a")) >= 2:
                    title = item.select_one("a.news_tit").text
                    date = item.select_one("span.info").text
                    media = item.select_one("a.info.press").text
                    content = item.select_one("div.news_dsc").text
                    url = item.select_one("a.news_tit")['href']
                    li.append({'title': title, 'date': date, 'media': media, 'content': content, 'URL': url})
            page = page + 1

    return pd.DataFrame(li, columns=['title', 'date', 'media', 'content', 'URL'])


# 사용자 입력 받기
keyword = input("찾는 keyword를 알려주세요: ")
startdate = input("시작하는 날을 알려주세요 ex) 2020.12.12: ")
enddate = input("끝나는 날을 알려주세요 ex) 2020.12.12: ")
max_pages = int(input("끝나는 페이지는 몇으로 할까요?: "))

# 함수 호출 결과를 데이터프레임으로 바로 반환
result = get_news_list(keyword, startdate, enddate, max_pages=max_pages)

# 데이터프레임 출력
print(result)