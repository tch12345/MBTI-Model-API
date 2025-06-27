import os
import re
import pandas as pd
import emoji
import string
from .dictionary import emoji_to_word,code_patterns,manglish_dict,variations

from nrclex import NRCLex
from langdetect import detect
from googletrans import Translator
from functools import lru_cache

translator = Translator()



def remove_gmail(message):
    gmail_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    if re.fullmatch(gmail_pattern, message):
        return None  # Remove row if it's only a Gmail
    return re.sub(gmail_pattern, "<gmail>", message)

def remove_links(message):
    url_pattern = r"(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9.-]+\.(com|net|org|edu|gov|my|io|ai|co|info|biz|me|tv|us|uk|cn|ru|jp|de|fr|au|in|xyz|ly|cc|to)(/[^\s]*)?)"
    if re.fullmatch(url_pattern, message):
        return None  # Remove row if it's only a link
    return re.sub(url_pattern, "<website>", message)

def remove_long_message(message):
    if isinstance(message, str):
        word_count = len(message.split())
        if word_count > 50:
            return None  # Remove row if message is too long
    return message

def remove_system_message(message):
    system_patterns = [
    r"^Messages and calls are end-to-end encrypted", 
    r"^消息和通话都会进行端到端加密。对话之外的任何人，甚至包含 WhatsApp 都无法读取或收听。点击了解更多。",
    r"^Mesej dan panggilan ini disulitkan secara menyeluruh", 

    r"^[^:]+ added [^:]+$",  # 添加成员
    r"^[^:]+ removed [^:]+$",  # 移除成员
    r"^[^:]+ left$",  # 退群
    r"^[^:]+ changed the subject to .*$",  # 群名修改
    r"^[^:]+ changed this group's icon$",  # 群图标修改
    r"^[^:]+ changed their phone number to a new number. Tap to message or add the new number",
    r"^[^:]+ created this group$",  # 创建群

    r"^[^:]+创建了群组.*$",  # 中文创建
    r"^[^:]+添加了你$",  # 中文添加
    r"^[^:]+退出了群组$",  # 中文退出
    r"你已被[^:]+移出群组$",  # 中文移出
    r"群组名称已由[^:]+更改为.*$",  # 中文群名修改
    r"[^:]+更改了群组图标$",  # 中文图标
    r"[^:]+将自己的电话号码更改为新号码。点击以发送消息或添加新号码。$",  # 中文更换号码
    r"[^:]+这条消息已经过编辑$",
    

    r"^[^:]+ telah menukar subjek kepada .*$",  # 马来文群名修改
    r"^[^:]+ telah menukar ikon kumpulan$",  # 马来文群图标
    r"^[^:]+ telah mencipta kumpulan ini$",  # 马来文创建群
    r"^[^:]+ telah menambah anda$",  # 马来文你被加入群
    r"^[^:]+ telah menambah [^:]+$",  # 马来文添加别人
    r"^[^:]+ telah meninggalkan kumpulan$",  # 马来文退出
    r"^[^:]+ telah menukar nombor telefon mereka kepada nombor baharu.*",  # 马来文换号提示

    # 🖼️ 媒体省略
    r"^<Media omitted>$",
    r"^<image omitted>$",
    r"^image omitted$",
    r"^<sticker omitted>$",
    r"^sticker omitted$",
    r"^<GIF omitted>$",
    r"^GIF omitted$",
    r"^<省略媒体文件>$",
    r"^媒体文件省略$",
    r"^图片省略$",
    r"^贴图省略$",
    r"^GIF 动图省略$",
    r"^Imej tidak disertakan$",  # 马来文图像
    r"^GIF tidak disertakan$",  # 马来文GIF

    r"^This message was deleted$",  # 别人撤回的消息
    r"^This message was deleted.$",  # 别人撤回的消息
    r"^You were added$",  # 你被加入群
    r"^this message was delete\.$",
    r"^You deleted this message$",
    r"^你删除了这条消息$",
    r"^此消息已删除$",
    r"^这条消息已删除$",
    r"^Mesej ini telah dipadam$",  # 马来文删除
    r"^Anda telah memadam mesej ini$",  # 马来文你删除

    r"^Missed voice call$",
    r"^Missed video call$",
    r"^[^:]+ missed a call$",
    r"未接来电$",
    r"未接语音通话$",
    r"未接视频通话$",
    r"Panggilan suara tidak dijawab$",  # 马来文语音
    r"Panggilan video tidak dijawab$",  # 马来文视频
    r"[^:]+ terlepas panggilan$"  # 马来文 missed call
]

    for pattern in system_patterns:
        if re.match(pattern, message.strip()):
            return None  # 识别为系统消息，删除该行

    return message  # 不是系统消息，保留

def remove_edited_message(message):
    message = message.replace("<This message was edited>", "").strip()
    return message if message else None  # 如果删除后为空，删除该行

def remove_sensitive(message):
    sensitive_pattern = r"\b(password|login|account|user|pass|key|code|credential|token)\b"
    if re.search(sensitive_pattern, message, re.IGNORECASE):
        return None
    return message

def replace_emoji_with_word(message):
    result_message = []

    # 遍历消息中的每个字符
    for char in message:
        # 检查是否为 emoji
        if char in emoji.EMOJI_DATA:
            # 如果是 emoji，先看映射表是否有对应的词汇
            if char in emoji_to_word:
                result_message.append(emoji_to_word[char])  # 替换为映射的词汇
            else:
                # 如果没有映射，使用 NRCLex 分析情感并替代
                nrc = NRCLex(char)
                emotions = nrc.raw_emotion_scores
                # 获取最强的情感
              
                dominant_emotion = max(emotions, key=emotions.get, default="neutral")
                result_message.append("<"+dominant_emotion+">")  # 用情感标签替代 emoji
        else:
            # 如果不是 emoji，保持原字符
            result_message.append(char)

    # 将处理后的字符合并成新的消息
    return ''.join(result_message)

def normalize_repeated_chars(message):
    return re.sub(r'(.)\1{2,}', r'\1\1', message)

def normalize_repeated_words(message):
     return re.sub(r'\b((ha|he|ho|hi|hoho|haha|hehe|hihi|lol|lmao|rofl|omg){2,})\b', lambda m: m.group(2), message, flags=re.IGNORECASE)

def remove_mentions(message):
    """移除 @ 提及"""
    return re.sub(r'@\w+', '', message)

def remove_if_only_numbers(message):
    # Check if the message consists only of digits, or has a valid sign (+ or -) followed by digits
    if (message.lstrip("+-").isdigit()) and (message.count('+') <= 1 and message.count('-') <= 1):
        return None  # Return None if the message is a valid number (with optional + or -)
    return message  # Otherwise, return the original message


def remove_non_alphanumeric(message):
    return re.sub(r'[^a-zA-Z0-9\s.,!?<>]', '', message)

def to_lowercase(message):
    """转换大小写为小写"""
    return message.lower()

def remove_messages_with_code(message):
    """如果消息包含代码模式，则返回 None，否则返回原消息"""
    for pattern in code_patterns:
        if re.search(pattern, message):
            return None  # 直接删除包含代码的消息
    return message

def protect_tags(message):
    """用占位符保护 < > 标记，避免误删"""
    return re.sub(r'(<[^<>]+?>)', r'<<keepword\1keepword>>', message)

def restore_tags(message):
    """还原 < > 标记"""
    message=message.replace("<< keepword", "").replace("keepword >>", "")
    return message.replace("<<keepword", "").replace("keepword>>", "")

@lru_cache(maxsize=1000)  
def translate_to_english(text):
    # 如果文本为空或无内容，直接返回原始文本
    if not text.strip():
        return text
    # 如果文本包含 @ 或者只有数字，视为无效文本，跳过翻译
    if '@' in text or text.isdigit():
        return text
    if all(char in string.punctuation for char in text):
        return text

    if re.fullmatch(r'[\d\:\.\-\s]+', text.strip()):
        return text
    if all(char in string.punctuation + "！？。，、；：「」‘’“”（）…—～·" for char in text):
        return text
    try:
        # 自动检测语言并翻译成英文
        lang = detect(text.strip().lower())
        if lang in ['ms', 'id', 'zh-cn', 'zh-tw']:  # 马来文或印尼文
            trans=translator.translate(text, src= 'auto', dest='en').text
            return trans
        else:
            return text  # 如果已经是英文，返回原始文本
    except Exception as e:
        # 如果发生任何错误，返回原始文本
        
        print(f"Translation error: {e} : {text}")
        return text


def generate_expanded_dict():
    expanded_dict = {}
    for word, replacement in manglish_dict.items():
        if word in variations:
            for variant in variations[word]:
                expanded_dict[variant] = replacement
        else:
            expanded_dict[word] = replacement
    return expanded_dict

# 替换 Manglish 词汇
expanded_dict = generate_expanded_dict()
def replace_manglish(message):
    for word, replacement in expanded_dict.items():
        message = re.sub(rf'\b{word}\b', replacement, message, flags=re.IGNORECASE)
    return message

def clean_message(message):
    # 依次调用处理函数
    functions = [
        remove_messages_with_code,
        remove_gmail,
        remove_links,
        remove_system_message,
        remove_edited_message,
        remove_sensitive,
        remove_mentions,
        remove_long_message,
        remove_if_only_numbers,
        to_lowercase,
        replace_emoji_with_word,
        protect_tags,
        normalize_repeated_chars,
        normalize_repeated_words,
        replace_manglish,
        translate_to_english,#only certain sentance
        remove_non_alphanumeric,
        to_lowercase,
        restore_tags,
    ]

    for func in functions:
        message = func(message)
        if message is None or message.strip() == "":  # If message becomes invalid, return None
            return None

    return message

def clean_chat_file(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    pattern = re.compile(rf"{re.escape(base_name)}_user(\d+)_part1\.csv")
    
    output_dir = "clean data"
    input_dir = "user data"
    for filename in os.listdir(input_dir):
        if pattern.match(filename):
            csv_path = os.path.join(input_dir, filename)
            print(f"Processing: {csv_path}")

            df = pd.read_csv(csv_path, encoding='utf-8', on_bad_lines='skip')
            df['message_text'] = df['message_text'].apply(
                lambda x: clean_message(str(x)) if pd.notnull(x) else x
            )

            df_cleaned = df.dropna(subset=['message_text']).drop_duplicates()

            output_path = os.path.join(output_dir, filename.replace('.csv', '_clean.csv'))
            df_cleaned.to_csv(output_path, index=False)
            print(f"Saved: {output_path}")

if __name__ == "__main__":
    df = pd.read_csv("user data/chat9_user2_part1.csv", encoding='utf-8', on_bad_lines='skip')
    df['message_text'] = df['message_text'].apply(lambda x: clean_message(str(x)) if pd.notnull(x) else x)
    df_cleaned = df.dropna(subset=['message_text'])
    df_cleaned = df_cleaned.drop_duplicates()
    output_file = "clean data/chat9_user2_part1_clean.csv"
    df_cleaned.to_csv(output_file, index=False)

