from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_wordcloud(text, font_path):
    wordcloud = WordCloud(font_path=font_path, width=800, height=800, 
                          background_color='white', 
                          min_font_size=10).generate(text)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# 파일 경로 및 폰트 파일 경로 설정
text_file_path = r'C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_1_Relevance-between-news-topics-and-trading-volume\pro1_데이터 활용\LDA-중복_워드클라우드.txt'
font_path = r'C:\Users\HOME\Desktop\새싹_교육\GitHub_CHOI\project_1_Relevance-between-news-topics-and-trading-volume\pro1_데이터 활용\NanumGothic.ttf'

text_data = read_text_file(text_file_path)

create_wordcloud(text_data, font_path=font_path)
