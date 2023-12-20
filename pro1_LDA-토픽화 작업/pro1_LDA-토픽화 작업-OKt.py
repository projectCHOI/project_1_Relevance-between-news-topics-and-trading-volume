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

# 필요한 라이브러리 설치
!pip install tqdm

import warnings
from google.colab import drive
import pandas as pd
from konlpy.tag import Okt
from tqdm import tqdm

# 경고 메시지 무시
warnings.filterwarnings('ignore')

# 형태소 분석기 Okt 초기화
okt = Okt()

# 데이터프레임의 'content' 열을 순회하면서 형태소 분석 수행
for i, row in tqdm(df.iterrows(), total=df.shape[0]):
    content = row['content']
    if isinstance(content, str):
        morphs = okt.pos(content)
        filtered_words = ' '.join([word for word, tag in morphs if tag in ['Noun', 'Verb', 'Pronoun']])
        df.at[i, 'POS'] = filtered_words

# 데이터프레임의 구조 확인
print(df[['content', 'POS']].head())

"""###정규표현식"""

import re

# 수정된 정규 표현식 패턴
regex_pattern = r'\<[^\>]*\>|\[[^\]]*\]|\([^\)]*\)|[0-9]*\.[0-9]*?\.[0-9]*|[a-zA-Z]+@[a-zA-Z]+\.[a-zA-Z]{2,}|Copyright|ⓒ|스포츠서울&sportsseoul.com|제공'

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
stop_word = ['은', '는', '이', '가', '을', '를', '에', '에서']

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
