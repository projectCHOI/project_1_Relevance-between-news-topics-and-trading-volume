##LDA

####불러오기
"""

import warnings
from google.colab import drive
drive.mount('/content/drive')

!pip install pandas==1.5.3

import pandas as pd
df = pd.read_csv('/content/drive/MyDrive/2.project_1_뉴스토픽 거래량 상관관계 구현/0_정리/2_수집1_[3조] s1_news.csv')

df.head()

"""##전처리 토큰화
- 형태소 분석 > 정규표현식 > 한글자 제거 > 불용어 처리
- [토큰화 + 토큰리스트] 생성

###형태소 분석
"""

#형태소 분석기를 사용하자.
!pip install konlpy

# Commented out IPython magic to ensure Python compatibility.
#형태소 분석기 Mecab
!git clone https://github.com/SOMJANG/Mecab-ko-for-Google-Colab.git
# %cd Mecab-ko-for-Google-Colab/
!bash ./install_mecab-ko_on_colab_light_220429.sh

#형태소 분석기 Mecab
from konlpy.tag import Mecab
tokenizer = Mecab()

# "POS" 열을 생성하고 형태소 분석 결과 저장
for i, row in df.iterrows():
    content = row['content']
    if isinstance(content, str):
        nouns = ' '.join(tokenizer.nouns(content))
        df.at[i, 'POS'] = nouns

# 데이터프레임의 구조 확인
print(df[['content', 'POS']].head())

"""###정규표현식"""

import re

# 정규 표현식 패턴
regex_pattern = r'\<[^\>]*\>|\&#8203;``【oaicite:0】``&#8203;]*\】|\[[^\)]*\]|\([^\)]*\)|[0-9]*\.[0-9]*?\.[0-9]*|[a-zA-Z]*@[a-zA-Z]*\.[a-zA-Z]*\.?[a-zA-Z]*|Copyright|ⓒ|스포츠서울&sportsseoul.com|제공'

# "RE" 열을 생성하고 정규 표현식을 적용하여 분류된 결과 저장
df['RE'] = df['POS'].apply(lambda text: re.sub(regex_pattern, ' ', text))

# 데이터프레임의 구조 확인
print(df[['POS', 'RE']].head())

df.head(2)

"""###한글자 제거"""

# "RE-1" 열을 생성하고 글자 수 1 이하인 데이터를 제거하여 저장
df['RE-1'] = df['RE'].apply(lambda text: ' '.join(word for word in text.split() if len(word) > 1))

# 데이터프레임의 구조 확인
print(df[['RE', 'RE-1']].head())

df.head(2)

"""###불용어 처리"""

stop_pos = ['Noun', 'Josa', 'Alpha', 'Punctuation', 'Suffix']
stop_word = ['은', '는', '이', '가', '을', '를', '에', '에서', '로', '으로',
'와', '과', '의', '처럼', '1분기', '2분기', '3분기', '4분기', '경제', '분석',
'경기', '상승', '하강', '급등', '급락', '회복', '상장', '공모주', '우승', '태권도',
'금매달', '시장', '기업', '텔레콤', '사업', '가치', '예측', '금융', '은행', '뱅크',
'올해', '증권', '현대', '평가', '지분', '성장', '공격', '랜섬', '웨어', '스퀘어',
'버스', '정보', '스가', '양사', '협약', '입니다', '체계', '차량', '미래', '너스',
'구주', '파트', '박정호', '대회', '철회', '시즌', '골프', '선수', '교육', '여자',
'분기', '매출', '대표', '유해', '스퀘어', '주주', '최종', '쉴더', '영업', '일감',
'사이버', '에너지', '너지', '에너', '이익', '채용', '서구', '발인', '호실', '남편',
'별세', '란스', '세브', '란스', '광주광역시', '병원', '신촌', '부친상', '장인상', '해양',
'부상', '관내', '광주', '조선', '구청장', '대우', '측정기', '용인', '신임', '내청', '이사',
'총회', '주총', '이사', '임원', '는데요', '김철수', '마무리', '경영', '경제', '은', '는',
'이', '가', '을', '를', '에', '에서', '로', '으로', '와', '과', '의', '처럼', '같이',
'만', '까지', '부터', '에게', '한테', '에서', '에서부터', '로부터', '에게로', '에서도',
'에도', '하고', '이나', '나', '라고', '이라고', '며', '라며', '에게는', '에겐', '에',
'께', '랑', '하다', '라서', '에서도', '에도', '라면', '만큼', '마냥', '에는', '엔', '에서만',
'로만', '처럼', '같이', '만으로', '부터', '으로서', '로서', '대로', '에게는', '한테도', '뿐',
'야', '이야', '이요', '이라요', '하죠', '하죠', '으로써', '로써', '이란', '는데', '더라도',
'다가', '이에요', '이면', '이었', '더', '죠', '고', '요', '에다', '에다가', '마저', '마저도',
'잘', '빠르게', '조용히', '무척', '너무', '매우', '아주', '정말', '과연', '전혀', '더', '더욱',
'가장', '반드시', '아직', '그래도', '비로소', '결국', '마침내', '아무튼', '약간', '대략', '대체로',
'이미', '좀', '몇몇', '모두', '갑자기', '뜻밖에', '한동안', '한두 번', '언제나', '이미', '최근',
'또', '바로', '뒤', '앞', '거의', '대개', '끝내', '시작하여', '뒤이어', '따라', '함께', '같이'
'프로','스토어','투자','증시','청약','스토','토어','선두','원스','메타',
'버스','타버','대어','매각','케이','코스피','코스닥','브로드밴드','심사','희망',
'기관','투자','그룹','심사','대상','기록','예비','기사','추진','자금',
'공동','부진','확정','반도체','회사','담당','수익','내년','협력','마지막',
'지원','금리','이번','올해','지난해','계획','이날','진행','공개','업체',
'과정','물리','마켓','합병','증가','투자자','업계','관리','국내','전년',
'외국인','이디스','호컴','맥스','주가','비즈','니스','씨티','비즈]','순매도',
'테마','연관','주일','내역','나무','매매','전일','작성','메인','테라',
'매수','등락','하이트','파인','플러스','효성','전자','홀딩스','에스','자체',
'라운드','수상','순위','협의','가구','연속','출발','스와','랭킹','승부',
'주인공','배임','강원','유입','도전','부정','현지','중앙','조성','응원',
'점수','눈높이','횡령','부장','부족','블록체인','엠투엠','플러스','스원','필로',
'공모','사장','모가','모빌리티','선임','출전','장애','텔레','배당','거래소',
'주관','프로그램','취업','성적','스피커','한네트','시스','거래','기간','시간',
'테크','개발','기자','배당','환원','소각','증권사','매입','배당금','자산',
'솔루션','오전','의혹','본사','하청','격차','장지호','거래','시설','물량',
'투어','시가총액','주행','배송','생각','합계','컬리','부회장','은퇴','제주',
'대비','분위기','커머스','단위','오픈','한국','차지','직무','사회','카드',]  # 이어지는 불용어 리스트

# "PRO" 열을 생성하고 불용어 처리된 결과 저장
def preprocess(text):
  text = str(text).split()
  text = [i for i in text if len(i) > 1]
  text = [i for i in text if i not in stop_pos]
  text = [i for i in text if i not in stop_word]
  return text

df['PRO'] = df['RE-1'].apply(preprocess)

# 데이터프레임의 구조 확인
print(df[['RE-1', 'PRO']].head())

df.head()

"""##토큰화 + 토큰리스트 생성"""

def make_tokens (df):
    for i, row in df.iterrows():
        if i%1000==0:
            print(i, '/',len (df))
        token = preprocess(df ['PRO'][i])
        df['PRO'][i] = ' '.join(token)
    return df
df = make_tokens (df)

"""##Gensim 패키지"""

!pip install gensim
from gensim import corpora
from gensim.models import LdaModel, TfidfModel

tokenized_docs = df['PRO'].apply(lambda x : x.split())

id2word = corpora. Dictionary (tokenized_docs)
corpus_TDM = [id2word.doc2bow (doc) for doc in tokenized_docs]
tfidf = TfidfModel (corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]

n = 50

lda = LdaModel(corpus=corpus_TFIDF,
                id2word=id2word,
                num_topics=n,
                random_state=100)

for t in lda. print_topics():
    print(t)

# df['PRO']

"""##시각화"""

!pip install pyLDAvis==3.4.1

# import pyLDAvis
# import pyLDAvis.gensim
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

pip install "pandas<2.0.0"

tokenized_docs = df['PRO'].apply(lambda x : x.split())

id2word = corpora. Dictionary (tokenized_docs)
corpus_TDM = [id2word.doc2bow (doc) for doc in tokenized_docs]
tfidf = TfidfModel (corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]

n = 50

lda = LdaModel(corpus=corpus_TFIDF,
                id2word=id2word,
                num_topics=n,
                random_state=100)

for t in lda. print_topics():
    print(t)

# df['PRO']

# 토픽 모델링 결과를 pyLDAvis 형식으로 변환
lda_display = gensimvis.prepare(lda, corpus_TFIDF, id2word)
# pyLDAvis 결과 시각화
pyLDAvis.display(lda_display)

# 그래프 이름 : Intertopic Distance Map : 주제간 거리지도
# 단어
# Selected Topic : 토픽지정
# Previous Topic : 이전 주제
# Next Topic : 다음주제
# Clear Topic : 주제 지우기

# Slide to adjust relevance metric :관련성 지표
# Top-30 Most Relevant Terms for Topic X (2.3% of tokens) : 토큰 X에 관련한 가장 연관있는 단어