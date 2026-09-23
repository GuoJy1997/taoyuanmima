import re
import sys

def check():
    with open('D:/桃园密码/工作区/第40章/03_去AI味润色稿.md', 'r', encoding='utf-8') as f:
        content = f.read()

    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]

    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', body))
    no_space_chars = len(re.sub(r'\s', '', body))
    print(f"Chinese chars: {chinese_chars}")
    print(f"Non-space chars: {no_space_chars}")

    banned = [
        "一死生", "齐彭殇", "虚诞", "妄作", "传国玉玺",
        "宛如", "仿佛在诉说着", "在这一刻时间凝固", "在这一刻时间静止",
        "不仅如此", "更重要的是", "殊不知",
        "嘴角勾起一抹弧度", "倒吸一口凉气", "眼神中闪烁着坚定的光芒"
    ]
    found_banned = []
    for b in banned:
        if b in body:
            found_banned.append(b)
    print("Found banned words:", found_banned)

    # dialogue density check
    blocks = re.split(r'“[^”]*”', body)
    max_len = 0
    over_150 = []
    over_200 = []
    for i, block in enumerate(blocks):
        clean = re.sub(r'\s', '', block)
        if len(clean) > max_len:
            max_len = len(clean)
        if len(clean) > 150:
            over_150.append((i, len(clean), clean[:50]))
        if len(clean) > 200:
            over_200.append((i, len(clean), clean[:50]))

    print(f"Max non-dialogue block length: {max_len}")
    print(f"Blocks > 150: {len(over_150)}")
    for item in over_150:
        print("  ", item)
    print(f"Blocks > 200: {len(over_200)}")

if __name__ == '__main__':
    check()
