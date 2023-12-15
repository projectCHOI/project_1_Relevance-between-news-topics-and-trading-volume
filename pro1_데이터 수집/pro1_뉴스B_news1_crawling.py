import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_news(url):
    headers = {
        "Cookie": "NNB=OURWEDJJKXKGI; nx_ssl=2; _naver_usersession_=+VdPHYAMq5W53YOSu5ttbQ==; page_uid=ieZzndprvmsssdTDFjRssssssah-332673"
    }
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    try:
        # 일반 뉴스
        title = soup.select_one("h2#title_area").text
        date = soup.select_one("div.media_end_head_info_datestamp span")["data-date-time"].split(" ")[0]
        media = soup.select_one("a.media_end_head_top_logo img")["title"]
        content = soup.select_one('div#newsct_article')

    except:
        try:
            # 연예 뉴스
            title = soup.select_one('h2.end_tit').text.strip()
            date = soup.select_one('span.author em').text
            media = soup.select_one('div.press_logo img')['alt']
            content = soup.select_one('div#articeBody')

        except:
            # 스포츠 뉴스
            try:
                title = soup.select_one('h4.title').text
                date = soup.select_one('div.info span').text.split(' ')[1:]
                media = soup.select_one('span.logo img')['alt']
                content = soup.select_one('div#newsEndContents')

            except:
                print(url)

    return (title, date, media, content, url)

def get_news_list(keyword, start_date, end_date):
    news = []

    for date in pd.date_range(start_date, end_date):
        str_date = date.strftime("%Y.%m.%d")
        print("date: ", str_date)

        page = 1
        while True:
            strdate = str_date.replace(".", "")

            start = (page - 1) * 10 + 1

            headers = {"Cookie": "NNB=OURWEDJJKXKGI; nx_ssl=2; _naver_usersession_=+VdPHYAMq5W53YOSu5ttbQ==; page_uid=ieZzndprvmsssdTDFjRssssssah-332673"}
            URL = f"https://search.naver.com/search.naver?where=news&sm=tab_pge&query={keyword}&sort=2&photo=0&field=0&pd=3&ds={str_date}&de={str_date}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{strdate}to{strdate},a:all&start={start}"
            res = requests.get(URL, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")

            if soup.select_one("div.not_found02") is not None:
                break

            print("page: ", page)

            page += 1

            for li in soup.select("ul.list_news li"):
                if len(li.select("div.info_group a")) > 1:
                    news.append(get_news(li.select("div.info_group a")[-1]["href"]))

    News = pd.DataFrame(news, columns=["제목", "날짜", "매체명", "본문", "URL"])

    st_d = start_date.replace('.', '_')
    e_d = end_date.split('.')[-1]

    News.to_csv(f"{st_d}" + "_" + f'{e_d}' + '.csv', mode="w")

    return News

# 예시로 "에스원" 키워드로 2020년 12월 10일부터 2020년 12월 31일까지의 뉴스를 검색합니다.
print(get_news_list("에스원", "2020.12.10", "2020.12.31"))