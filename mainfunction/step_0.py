import io
import os
import re

def check_file_size(file):
    file.seek(0, os.SEEK_END)  # 移动到文件末尾
    size = file.tell()         # 获取当前位置（即文件大小）
    file.seek(0)               # 重置文件指针
    print(f"📄 文件大小: {size} 字节")
    if size < 2 * 1024 * 1024:
        print("✅ 文件小于2MB")
        return True
    else:
        print("❌ 文件超过2MB")
        return False
    return size < 2 * 1024 * 1024  # 小于 2MB

def clean_invisible_chars(text):
    return ''.join(c for c in text if c.isprintable() or c in '\n\r\t')

def validate_and_save_file(file, filename, save_dir="txt data"):
    """检查前 5 行是否包含 WhatsApp 聊天格式，若有匹配则保存文件"""

    content = file.read().decode('utf-8', errors='ignore')
    lines = content.splitlines()

    # 和 process_whatsapp_txt 保持一致
    pattern1 = re.compile(r'(\d{4}/\d{1,2}/\d{1,2})\s(\d{1,2}:\d{2})\s[-–]\s.*?:\s(.*)')
    msg_start_pattern_1 = re.compile(r'(\d{4}/\d{1,2}/\d{1,2})\s(\d{1,2}:\d{2})\s*[-–]?\s*(.*)')
    msg_start_pattern_2 = re.compile(r'\[?(\d{2}/\d{2}/\d{4}),\s*(\d{1,2}:\d{2}(?::\d{2})?\s?[aApP][mM])\]?\s*[-–]?\s*(.*)')

    for i in range(min(20, len(lines))):
        line = clean_invisible_chars(lines[i]).strip()
        if not line:
            continue

        # 跟主函数一致的判断流程
        if pattern1.match(line):
            msg_start_pattern = msg_start_pattern_1
        else:
            msg_start_pattern = msg_start_pattern_2

        if msg_start_pattern.match(line):
            if not filename.lower().endswith('.txt'):
                filename += '.txt'
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 第 {i+1} 行格式有效，已保存：{save_path}")
            return True

    print("❌ 前5行都不是 WhatsApp 聊天格式，未保存")
    return False


    

if __name__ =="__main__":
     with open("txt data/chat8.txt", "rb") as f:
        file_obj = io.BytesIO(f.read())  # 转成 BytesIO 模拟上传文件
        check_file_size(file_obj)
        validate_and_save_file(file_obj,"chat7.txt")