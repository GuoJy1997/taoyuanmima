import re

with open(r'D:\桃园密码\工作区\第50章\02_正文初稿.md', 'r', encoding='utf-8') as f:
    content = f.read()

parts = content.split('---')
body = '---'.join(parts[2:]) if len(parts) > 2 else content

chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', body))
total_non_space = len(re.findall(r'\S', body))

print("="*60)
print(f"1. 字数统计:")
print(f"   正文纯汉字数: {chinese_chars} (要求: 1800 ~ 2500)")
print(f"   总非空白字符数: {total_non_space}")
assert 1800 <= chinese_chars <= 2500, f"字数不合规: {chinese_chars}"
print("   --> 字数合规: PASS!")

print("="*60)
print("2. 禁词检测:")
banned_words = [
    '一死生', '齐彭殇', '虚诞', '妄作',
    '宛如', '仿佛在诉说着', '在这一刻时间凝固',
    '不仅如此', '更重要的是', '殊不知',
    '嘴角勾起一抹弧度', '倒吸一口凉气', '眼神中闪烁着坚定的光芒',
    '仿佛'
]
found = []
for bw in banned_words:
    if bw in body:
        found.append(bw)
print(f"   发现禁词: {found}")
assert len(found) == 0, f"包含禁词: {found}"
print("   --> 禁词检测: PASS (零容忍通过)!")

print("="*60)
print("3. 对话密度检测 (连续无对白不超过150字):")
quotes = list(re.finditer(r'[“"][^”"]*[”"]', body))
print(f"   对话总次数: {len(quotes)}")

max_gap = 0
prev_end = 0
for i, m in enumerate(quotes):
    start, end = m.span()
    gap_text = body[prev_end:start]
    gap_chars = len(re.findall(r'[\u4e00-\u9fa5]', gap_text))
    if gap_chars > max_gap:
        max_gap = gap_chars
    prev_end = end

tail_text = body[prev_end:]
tail_chars = len(re.findall(r'[\u4e00-\u9fa5]', tail_text))
if tail_chars > max_gap:
    max_gap = tail_chars

print(f"   最大无对话间隙(汉字数): {max_gap} (红线: 150)")
assert max_gap <= 150, f"对话密度超标: {max_gap}"
print("   --> 对话密度检测: PASS!")

print("="*60)
print("4. 核心情节关键锚点检测:")
keywords = {
    "一锤定音【归朝堂】": "【归朝堂】",
    "崇德太后临朝称制": "崇德太后",
    "桓温长刀收鞘": "咔哒",
    "蚕茧纸《兰亭集序》": "兰亭集序",
    "时空排斥力": "排斥力",
    "转交王献之": "王献之",
    "替后人收好它": "替后人……收好它",
    "秽物化灰散尽": "化成灰",
    "生门洞开": "生门",
    "秦华断后": "我来断后",
    "兰亭回望绝杀": "永和九年"
}
for k, v in keywords.items():
    exists = v in body
    print(f"   - {k}: {'PASS' if exists else 'FAIL'}")
    assert exists, f"缺少关键情节锚点: {k}"

print("="*60)
print("全部严格质检项 100% 通过！")
