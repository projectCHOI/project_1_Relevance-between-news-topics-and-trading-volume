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

df.head(2)

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
stop_word = [# 기타 이슈
"교육","마지막","연속","유해","최종","월더스","예측","올해","결전","파트너",
"기능","스마트","적용","인재","관리","설치","운영","지능","팩토리","생태계",
"지역","제로","처리","케이","비즈","씨아이","택티엔","네트","필로","스케",
"파인","에스","원스","시스","에이","테크","효성","했습니다","일간","연관",
"전일","살펴보면","디스","비스","트론","아이","맥스","리퍼블릭","엠투엠","코콤",
"하이","플러스","스페이스","에어로","에프","일리","한화","필드","테라","홀딩스",
"올라","사상","전인","사랑","범위","입성","일정","시기","검색","응시",
"배송","였던","미만","대행","보였다","어려움","유안","이었던","특정","하이닉스",
"제주도","바람","연기","스윙","여러분","탈취","대다수","계단","하루","반전",
"파이오링크","받지","한파","서재","밀리","금제","아이즈","유플러스","휴가","실행",
"가입자","지니","기부","뮤직","정랙","출시","슬림","학과","가온","텔레캅",
"본사","서구","조사","몰아","대원","줬다는","문자","파일","기승","광역시",
"몰아주기","모씨","해양","대우조선","가중","신정","무시","연대","결성","영진",
"열사","변가","관사","몸값","토종","포기","적정","대기","몰라주기","어려울",
"리지","부율","출격","문구점","자의","전형","오스","우대","경력","기능올림픽",
"일자리","신입","공체","학력","출근","합격자","면접","신입사원","칩스","유니",
"식스","오전", "호실", "모친상", "장인상","남편", "춘천", "탈락", "서울", "과장",
"프롭", "부상", "안양", "세브란스병원", "수료", "동아", "회선", "본선", "오후","원주",
"미보", "창모", "강원도","텔레","퀘스트","라이언스","콘덴서","유비","인포","룩스",
"픽셀","팅크","록스","삼화","켐트","모터","모르","양사","나타났다","전체",
"멘토링","연구소","각별","건수","자격","귀중","복구","워드","등급","이데일리",
"교육과정","엠게임","안티","동향","인턴","다날","보고서","주연테크","중기","김호준",
"언스","사자","합동","파워텔","타이밍","잡립","삼다수","마스터","상무","승진",
"사무소","부사","지켰다","인사","노컷뉴스","스티커","부문","발굴","정신","세트",
"홍보","리더십","노컷","달라진","계정","문서","서버","난방","매니저","중앙",
"커뮤니케이션","린지","근무","방지","스팩","하단","반출","엑스","메시지", "체험",
"저장", "서나", "어디", "직원", "이메일", "공략","세아","스케이","넷째","자이크",
"변조","타임즈","소액","셀프","프렌들리","안면","무게","개통","통제","등록",
"논스톱","선반","이뤄진다","보급","모션","휴대폰","입장","결합","에어컨","봉사활동",
"유공","포항","발열","포항시","경북","화상","트럭","의심","도움","고문",
"착용","강원","여름","동아일본","모임","주택","모주","시초","초가","열기",
"단위","간사","돌입","알려졌습니다","거듭","생방송","집결","제작", "동참", "부금",
"친환경", "달력", "적십자사", "환경보호", "헌혈","구입", "성경제", "성금", "공헌", "푸른",
"만든", "적십자", "라이온", "머니투데이", "약속","이웃", "이윤차", "박진", "오프", "새해",
"출결", "냉장고", "원아", "보낼","카드","인포섹","미세먼지","디지털타임스","겸임","무제",
"온실가스","탄소","연료","감축","충전","배출량","일진","배출","듀얼","스코프",
"피엔","조선","공항","녹색","국민일보","헤럴드경제","스맥","스터디","창원","리서치",
"파크","신원","쓰래기","과중","즐길","음원","알려","기물","터널","린다",
"다이노스","텔레콤","청호컴넷","웨이브","쿠팡","아마존","넷플릭스","이마트","헬로비전","세븐일레븐",
"제일모직","대우건설","핀더", "현대", "모비스","한섬", "고려아연", "유한양행","리츠","해태",
"크라운","브로드밴드","포스코","스퀘어",
# 스포츠이슈
"시즌","대회","투어","우승","스퀘어",
"상장","선수","골프","대상","지원",
"활동","탐지","가구","소상","차량",
"계층","실무","출전","타이틀","보기",
"열린","훈련","순위","무대","후원",
"획득","트로피","승부","아마추어","스포츠",
"후반","국가대표","성적","경쟁률","골퍼",
"하나 마이크론","후보자","경기장","플레이","티비",
"선수단","펜싱","관람","프로야구"]

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
