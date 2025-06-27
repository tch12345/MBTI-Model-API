import pandas as pd
from joblib import load

def predict_mbti(file_txt):
    # 提取编号（如 chat8）
    chat_id = file_txt.replace('.txt', '')
    merged_csv = f'owndata/{chat_id}_user.csv'
    print(f"📂 读取数据: {merged_csv}")
    
    # 读取 CSV
    df = pd.read_csv(merged_csv)
    user_ids = df['user_id']
    X = df.drop(columns=['user_id', 'message_count'])

    # 模型路径和标签映射（0→原始字母，1→相对字母）
    model_paths = {
        'I': 'model/xgb_model_I.pkl',
        'N': 'model/xgb_model_N.pkl',
        'T': 'model/xgb_model_T.pkl',
        'J': 'model/xgb_model_J.pkl'
    }

    label_map = {
        'I': {1: 'I', 0: 'E'},
        'N': {1: 'N', 0: 'S'},
        'T': {1: 'T', 0: 'F'},
        'J': {1: 'J', 0: 'P'}
    }

    # 初始化预测结果为每个用户对应的空字符串
    predictions = {uid: '' for uid in user_ids}

    # 循环每个模型进行预测
    for trait, model_path in model_paths.items():
        print(f"🤖 使用模型: {model_path}")
        model = load(model_path)
        y_pred = model.predict(X)

        for uid, pred in zip(user_ids, y_pred):
            predictions[uid] += label_map[trait][int(pred)]

    # 打印最终 MBTI 类型
    print("\n🧠 MBTI 预测结果:")
    for uid in user_ids: 
        print(f"{uid}: {predictions[uid]}")

    data = [{"user": uid, "mbti": predictions[uid]} for uid in user_ids]
    return data

# 示例调用
if __name__ == '__main__':
    print(predict_mbti("chat.txt"))
