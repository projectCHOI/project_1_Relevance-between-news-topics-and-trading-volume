## project 주제
- 논문은 비즈니스 뉴스에서 고품질 주제(토픽)를 추출하여, 비정상적인 주식시장 변동성(거래량)을 설명하는 내용이다.
- project1은 논문을 기반으로 기업 '에스원'의 변동성에 대한 토픽분석을 수행하는 것이 목표이다.
- 목표 달성을 위해 '에스원'의 뉴스를 수집하고, 거래량 변동 원인을 비교하기 위한 경쟁사(KT텔레캅, SK 쉴더스, 아이디스)의 데이터를 수집해 토픽화 한다. 그리고 모빅 분포와 거래량을 비교한다.
## project 사용언어 
- python(VScode, google colab)
## 수집 대상
- 형식 : 한국의 포털, 네이버에서 발행 된 뉴스만을 사용한다.
- 기간 : 2019.01.01 ~ 2024.10.24
- 수집 대상 : 에스원 거래량 및 뉴스 and 경쟁사(KT텔레캅, SK 쉴더스, 아이디스)
- 뉴스 수집 내용 : 제목, 일자, 본문
- 거래량 수집 내용 : 기업 '에스원'의 거래량 2019.01~ 2023.10
## Framework(프레임워크)
- 크롤링 > LDA 토큰화 > 데이터 표준화 > LASSO > FVE > FPE
## 시각화
- pyLDAvis
- Jupyter Notebook
- ppt
