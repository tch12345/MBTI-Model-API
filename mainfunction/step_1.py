import os
import csv
import re

def clean_invisible_chars(text):
    return ''.join(c for c in text if c.isprintable())

def process_whatsapp_txt(input_file, min_lines=15, max_lines=700):
    input_file = os.path.join("txt data", input_file)
    # Regex patterns
    pattern1 = re.compile(r'(\d{4}/\d{1,2}/\d{1,2})\s(\d{1,2}:\d{2})\s[-–]\s.*?:\s(.*)')
    msg_start_pattern_1 = re.compile(r'(\d{4}/\d{1,2}/\d{1,2})\s(\d{1,2}:\d{2})\s*[-–]?\s*(.*)')
    msg_start_pattern_2 = re.compile(r'\[?(\d{2}/\d{2}/\d{4}),\s*(\d{1,2}:\d{2}(?::\d{2})?\s?[aApP][mM])\]?\s*[-–]?\s*(.*)')
    sender_pattern = re.compile(r'(.+?):\s*(.*)')

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    user_dict = {}
    user_counter = 1
    user_messages = {}

    current_message = ''
    current_user = ''
    current_date = ''
    current_time = ''

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = clean_invisible_chars(line).strip()
            if not line:
                continue

            if pattern1.match(line):
                msg_start_pattern = msg_start_pattern_1
            else:
                msg_start_pattern = msg_start_pattern_2

            msg_start = msg_start_pattern.match(line)
            if msg_start:
                if current_message and current_user:
                    user_messages.setdefault(current_user, []).append(
                        (current_date, current_time, current_message.strip())
                    )

                current_date = msg_start.group(1)
                current_time = msg_start.group(2)
                message = msg_start.group(3)

                sender_match = sender_pattern.match(message)
                if sender_match:
                    sender = sender_match.group(1).lower().strip()
                    message_text = sender_match.group(2)

                    if sender not in user_dict:
                        user_dict[sender] = f'user{user_counter}'
                        user_counter += 1
                    current_user = user_dict[sender]
                    current_message = message_text
                else:
                    current_user = 'system'
                    current_message = message
            else:
                current_message += '\n' + line

        if current_message and current_user:
            user_messages.setdefault(current_user, []).append(
                (current_date, current_time, current_message.strip())
            )

    # Write messages by user
    for user_label, messages in sorted(user_messages.items(), key=lambda x: len(x[1])):
        if len(messages) < min_lines:
            continue

        messages = messages[::-1]
        chunks = [messages[i:i+max_lines] for i in range(0, len(messages), max_lines)]
        # 只保存第一个 chunk
        first_chunk = chunks[0]
        filename = f"user data/{base_name}_{user_label}_part1.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as outfile:
            csv_writer = csv.writer(outfile)
            csv_writer.writerow(['date', 'time', 'user_label', 'message_text'])
            for msg in first_chunk:
                csv_writer.writerow([msg[0], msg[1], user_label, msg[2]])


    print("Processing complete. Output CSVs generated.")

if __name__ == "__main__":
    txt=f"2a037ebe06454837c5edc9d9581f59bd.txt"
    process_whatsapp_txt(txt)

