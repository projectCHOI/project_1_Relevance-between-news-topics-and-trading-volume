# pip install pandas 판다스 설치(필요하면)
import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def count_keyword_occurrences(df, keyword):
    return df[df["content"].str.contains(keyword, na=False)].shape[0]
    # na=False를 추가하여 NaN 값을 무시하고 검색

def main():
    # 경로를 환경애 맞게 변경
    file_path = "s1_news.csv"

    try:
        df = load_data(file_path)

        # 키워드 정의
        keyword = "에스원"

        # 키워드 발생 건수 계산
        count = count_keyword_occurrences(df, keyword)

        # 결과 출력
        print(f"{keyword} 키워드가 포함된 기사 건수: {count}")

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    main()