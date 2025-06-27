import os
import pandas as pd
import glob

def summarize_single_file(file_path):
    df = pd.read_csv(file_path)

    if df.empty:
        print(f"⚠️ 文件 {file_path} 为空，跳过。")
        return None

    # 计算平均特征
    mean_features = df[[
        "word_count", "emoji_count", "punctuation_count", "avg_word_length",
        "first_person_count", "second_person_count", "sentiment_score",
        "is_question", "is_exclamation", "group_word_count",
        "period_0", "period_1", "period_2", "period_3",
        "period_4", "period_5", "period_6", "period_7"
    ]].mean()

    mean_features["message_count"] = len(df)

    # 提取 user_id
    filename = os.path.basename(file_path).replace("_clean_features.csv", "")
    mean_features["user_id"] = filename.split("_part")[0]  # 去掉 part1

    final_df = pd.DataFrame([mean_features])
    final_df = final_df[["user_id"] + [col for col in final_df.columns if col != "user_id"]]
    return final_df

def process_individual_outputs(txt_file):
    chat_id = os.path.splitext(os.path.basename(txt_file))[0]  # chat8.txt -> chat8
    pattern = f"features/{chat_id}_user*_part1_clean_features.csv"
    matching_files = glob.glob(pattern)

    if not matching_files:
        print(f"❌ 未找到匹配文件：{pattern}")
        return

    print(f"🔍 发现 {len(matching_files)} 个 part1 文件，开始处理...")

    all_rows = []

    for file_path in matching_files:
        row_df = summarize_single_file(file_path)
        if row_df is not None:
            all_rows.append(row_df)

    if all_rows:
        final_df = pd.concat(all_rows, ignore_index=True)
        output_file = f"owndata/{chat_id}_user.csv"
        os.makedirs("owndata", exist_ok=True)
        final_df.to_csv(output_file, index=False)
        print(f"✅ 所有结果已合并保存到 {output_file}")
    else:
        print("⚠️ 没有任何有效数据写入。")

if __name__ == "__main__":
    # 测试用例，替换成你的文件路径
    file_path = "chat8.txt"
    process_individual_outputs(file_path)
