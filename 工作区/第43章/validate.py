# -*- coding: utf-8 -*-
import re
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'D:\桃园密码\工作区\第43章\03_去AI味润色稿.md', 'r', encoding='utf-8') as f:
    full_text = f.read()

# 拆分 Frontmatter 和正文
parts = full_text.split('---', 2)
frontmatter = parts[1] if len(parts) > 2 else ''
body = parts[2] if len(parts) > 2 else full_text

# 1. 统计正文中文字数
chinese_chars = re.findall(r'[\u4e00-\u9fa5]', body)
word_count = len(chinese_chars)
print(f"[1] 正文中文字数: {word_count}")
assert 1800 <= word_count <= 2500, f"字数不合规: {word_count} (必须在 1800-2500 之间)"

# 2. 检查禁忌词
taboos = ['一死生', '齐彭殇', '虚诞', '妄作', '传国玉玺']
found_taboos = [t for t in taboos if t in body]
print(f"[2] 禁忌词检查: {found_taboos if found_taboos else 'PASSED (零违规)'}")
assert len(found_taboos) == 0, f"发现禁忌词: {found_taboos}"

# 3. 检查 AI 套路词
ai_patterns = [
    '宛如', '仿佛在诉说着', '在这一刻', '不仅如此', '更重要的是', 
    '殊不知', '嘴角勾起一抹弧度', '倒吸一口凉气', '心中暗道', 
    '眼神中闪过一丝', '宛若', '犹如', '仿佛'
]
found_ai = [w for w in ai_patterns if w in body]
print(f"[3] AI 套路词检查: {found_ai if found_ai else 'PASSED (零违规)'}")
assert len(found_ai) == 0, f"发现 AI 套路词: {found_ai}"

# 4. 对白密度检查（严禁连续 150 字无对白引号）
body_clean = re.sub(r'#.*', '', body)
quotes = list(re.finditer(r'“[^”]*”', body_clean))
print(f"[4] 对白引号出现次数: {len(quotes)}")

last_end = 0
max_non_dialogue = 0
worst_segment = ''
for q in quotes:
    seg = body_clean[last_end:q.start()]
    c_len = len(re.findall(r'[\u4e00-\u9fa5]', seg))
    if c_len > max_non_dialogue:
        max_non_dialogue = c_len
        worst_segment = seg.strip()
    last_end = q.end()

# 最后一段
tail_seg = body_clean[last_end:]
tail_len = len(re.findall(r'[\u4e00-\u9fa5]', tail_seg))
if tail_len > max_non_dialogue:
    max_non_dialogue = tail_len
    worst_segment = tail_seg.strip()

print(f"[4] 最大连续无对白字数: {max_non_dialogue} 字")
if max_non_dialogue > 150:
    print(f"FAILED: 超过 150 字红线！最长段落：\n{worst_segment}")
    sys.exit(1)
else:
    print("PASSED: 严格满足 <= 150 字红线！")

# 5. 检查核心关键细节与收束
key_details = [
    ('万千钢针扎入骨髓钻心绞痛', '粗钢针'),
    ('双膝被地心引力重重砸烂泥', '双膝'),
    ('冰冷空气生硬呛进气管', '气管'),
    ('恶尸后颈骨反折暴突死眼', '反折'),
    ('秦华割喉劈颅白汽', '白汽'),
    ('方寸黑油布包前燕符牌', '白狼衔日'),
    ('王羲之肃穆整冠深深长揖及地', '长揖'),
    ('章末精准收束', '朝廷……欠下了诸位一个人情。')
]

for label, keyword in key_details:
    if keyword in body:
        print(f"[5] 核心细节检测 - {label}: 存在 [OK]")
    else:
        print(f"[5] 核心细节检测 - {label}: 缺失 [FAIL]")
        sys.exit(1)

print("\n=== 全部自动化质检全部通过！ ===")
