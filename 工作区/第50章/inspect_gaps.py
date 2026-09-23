import re

with open(r'D:\桃园密码\工作区\第50章\02_正文初稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('---')
body = '---'.join(parts[2:]) if len(parts) > 2 else content

quotes = list(re.finditer(r'[“"][^”"]*[”"]', body))

prev_end = 0
for i, m in enumerate(quotes):
    start, end = m.span()
    gap_text = body[prev_end:start]
    gap_chars = len(re.findall(r'[\u4e00-\u9fa5]', gap_text))
    if gap_chars > 120:
        print(f"Index {i} (before dialogue: {m.group()[:15]}...): chars = {gap_chars}")
        print(gap_text.strip())
        print("="*50)
    prev_end = end
