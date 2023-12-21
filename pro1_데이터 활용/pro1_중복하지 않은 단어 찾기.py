from collections import Counter

words = ["시즌", "대회", "투어",
         "시즌", "대회", "투어",
         "윤석", "웍스", "바람"]

print(f"주어진 단어 목록의 총 개수: {len(words)}")

# 단어의 빈도수를 세고, 1회만 나타난 단어들을 찾기
word_counts = Counter(words)
unique_words = {word: count for word, count in word_counts.items() if count == 1}


if not unique_words:
    print("1회만 나타난 단어가 없습니다.")
else:
    print(unique_words)
