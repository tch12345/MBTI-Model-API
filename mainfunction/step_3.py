import os
import re
import glob
import pandas as pd


# 语法分析与情感分析库
from textblob import TextBlob

def parse_hour(time_str):
    for fmt in ['%I:%M%p', '%H:%M', '%I:%M:%S%p']:
        try:
            dt = pd.to_datetime(time_str, format=fmt)
            return dt.hour
        except:
            continue
    return -1  # 解析失败返回-1
def hour_to_active_period(h):
    if h < 0:
        return -1
    return h // 3

def add_active_period_cols(df):
    df['hour'] = df['time'].apply(parse_hour)
    df['active_period'] = df['hour'].apply(hour_to_active_period)

    # 初始化8个时段列为0
    for i in range(8):
        col_name = f'period_{i}'
        df[col_name] = 0

    # 对应时段列置1
    df.loc[df['active_period'].between(0,7), ['period_' + str(i) for i in range(8)]] = 0  # 确保先全0
    for i in range(8):
        df.loc[df['active_period'] == i, f'period_{i}'] = 1

    return df

def extract_features(text):
    words = re.findall(r'\b\w+\b', text) #
    word_count = len(words)
    emoji_count = len(re.findall(r'<[^<>]+>', text))
    punctuation_count = len(re.findall(r'[,.!?…]', text))
    avg_word_length = sum(len(w) for w in words) / word_count if word_count else 0

    first_person_count = sum(1 for w in words if w.lower() in {"i", "me", "my","mine","myself"})
    second_person_count = sum(1 for w in words if w.lower() in {"you", "your","yours","yourself","yourselves"})
    group_word_count = sum(1 for w in words if w.lower() in {"we", "us", "our", "ours", "ourselves", "everyone", "all", "team"})
    
    sentiment_score = TextBlob(text).sentiment.polarity
    
    is_question = int("?" in text)
    is_exclamation = int("!" in text)
    return [
        word_count, emoji_count, punctuation_count, avg_word_length,
        first_person_count, second_person_count,
        sentiment_score, is_question, is_exclamation,
        group_word_count
    ]

def extract_features_users(txt_filename):
    base_name = os.path.splitext(os.path.basename(txt_filename))[0]
    input_folder = "clean data"
    output_folder = "features"
    os.makedirs(output_folder, exist_ok=True)

    # ✅ 只选取 part1 的 CSV 文件
    pattern = os.path.join(input_folder, f"{base_name}_user*_part1_clean.csv")
    file_list = glob.glob(pattern)

    if not file_list:
        print(f"❌ 没有找到任何 part1 的清洗文件: {pattern}")
        return

    print(f"📦 准备处理 {len(file_list)} 个 part1 文件")
    for file_path in file_list:
        print(f"🔍 处理: {file_path}")
        try:
            df = pd.read_csv(file_path, names=["date", "time", "user_label", "message_text"], skiprows=1)
            df["message_text"] = df["message_text"].fillna("").astype(str)

            df[[
                "word_count", "emoji_count", "punctuation_count", "avg_word_length",
                "first_person_count", "second_person_count",
                "sentiment_score", "is_question", "is_exclamation",
                "group_word_count"
            ]] = df["message_text"].apply(lambda x: pd.Series(extract_features(x)))

            df = add_active_period_cols(df)

            counts = df["user_label"].value_counts()
            valid_users = counts[counts > 15].index
            df = df[df["user_label"].isin(valid_users)]

            out_name = os.path.splitext(os.path.basename(file_path))[0] + "_features.csv"
            out_path = os.path.join(output_folder, out_name)
            df.to_csv(out_path, index=False)
            print(f"✅ 已保存: {out_path}")
        except Exception as e:
            print(f"❌ 错误: {file_path} - {e}")


if __name__ =="__main__":
    extract_features_users('chat9.txt')





