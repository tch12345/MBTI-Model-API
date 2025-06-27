import os
import re
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
import json
import nltk

def extract_top_10_words_all_users(txt_file, input_dir="clean data"):
    
    nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))

    base_name = os.path.splitext(os.path.basename(txt_file))[0]
    pattern = re.compile(rf"{re.escape(base_name)}_user\d+_part1_clean\.csv")

    results = {}

    for filename in os.listdir(input_dir):
        if pattern.match(filename):
            user_id = filename.replace("_part1_clean.csv", "")
            csv_path = os.path.join(input_dir, filename)
            print(f"🔍 正在处理用户：{user_id}")

            df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
            if 'message_text' not in df.columns:
                print(f"⚠️ 跳过 {filename}，未找到 'message_text' 列。")
                continue
            
            all_text = ' '.join(df['message_text'].dropna().astype(str)).lower()
            all_text = re.sub(r'<[^>]+>', '', all_text)
            words = re.findall(r'\b[a-z]{2,}\b', all_text)
            filtered_words = [w for w in words if w not in stop_words]

            counter = Counter(filtered_words)
            top10 = counter.most_common(10)

            result_json = {word: count for word, count in top10}
            user_short = user_id.split("_user")[-1]
            results[f"user{user_short}"] = result_json

    print("\n📝 所有用户前10常用有意义英文单词（仅用 NLTK 英文 stopwords 过滤）：")
    for user_id, word_dict in results.items():
        print(f"{user_id}: {word_dict}")

    return results



if __name__ == "__main__":
     print(extract_top_10_words_all_users("afa6286898d511c5ee7bd9058df46b1e.txt"))