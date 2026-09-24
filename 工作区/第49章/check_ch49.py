import re
import sys

def audit(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]

    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', body))
    no_space_chars = len(re.sub(r'\s', '', body))
    
    print(f"=== 字数统计 ===")
    print(f"正文纯汉字数: {chinese_chars}")
    print(f"正文去空白字符总数(含标点): {no_space_chars}")
    if 1800 <= chinese_chars <= 2500:
        print("PASSED: 纯汉字数在 1800 ~ 2500 范围内。")
    else:
        print(f"FAILED: 纯汉字数 {chinese_chars} 不在 1800 ~ 2500 范围内！")

    # Banned words
    banned = [
        "一死生", "齐彭殇", "虚诞", "妄作",
        "宛如", "仿佛在诉说着", "在这一刻时间静止", "在这一刻时间凝固", "在这一刻",
        "不仅如此", "更重要的是", "殊不知",
        "嘴角勾起一抹弧度", "嘴角勾起", "倒吸一口凉气", "倒吸凉气"
    ]
    print(f"\n=== 违禁词检测 ===")
    found_banned = []
    for b in banned:
        if b in body:
            found_banned.append(b)
    if found_banned:
        print(f"FAILED: 发现违禁词: {found_banned}")
    else:
        print("PASSED: 未发现任何违禁词。")

    # Dialogue density check (< 200 chars non-dialogue)
    print(f"\n=== 对话密度红线检测 (连续非对白严禁超过200字) ===")
    non_dialogue_blocks = re.split(r'“[^”]*”', body)
    max_block_len = 0
    over_blocks = []
    for idx, block in enumerate(non_dialogue_blocks):
        clean_b = re.sub(r'\s', '', block)
        if len(clean_b) > max_block_len:
            max_block_len = len(clean_b)
        if len(clean_b) > 120:
            print(f"  区块 {idx} 长度: {len(clean_b)} -> {clean_b[:30]}...")
        if len(clean_b) > 200:
            over_blocks.append((idx, len(clean_b), clean_b[:30] + '...'))

    print(f"最大连续非对白长度: {max_block_len} 字")
    if over_blocks:
        print(f"FAILED: 发现 {len(over_blocks)} 处超过 200 字无对白区间:")
        for idx, l, snippet in over_blocks:
            print(f"  块 {idx}: {l} 字 -> {snippet}")
    else:
        print("PASSED: 所有非对白区间均严格低于 200 字！")

    # Physical descriptions
    print(f"\n=== 五大冷硬物理白描检测 ===")
    physical_items = {
        "微苦杏仁油脂气": any(k in body for k in ["苦", "杏仁", "油脂"]),
        "紫色眼棱凶光": any(k in body for k in ["紫", "棱"]) and any(k in body for k in ["凶光", "冷厉", "灯火", "火光"]),
        "竹叶震脱沙沙声": any(k in body for k in ["竹叶", "声波", "脱落", "震"]) and "沙沙" in body,
        "玉笏泛白喀吧声": any(k in body for k in ["玉笏", "指关节", "泛白"]) and "喀吧" in body,
        "心脏撞击胸骨沉闷轰响": any(k in body for k in ["心脏", "胸骨", "轰响", "沉闷"])
    }
    all_phys_passed = True
    for k, v in physical_items.items():
        print(f"  {k}: {'PASSED' if v else 'FAILED'}")
        if not v:
            all_phys_passed = False

    return len(found_banned) == 0 and len(over_blocks) == 0 and 1800 <= chinese_chars <= 2500 and all_phys_passed

if __name__ == '__main__':
    res = audit(sys.argv[1])
    sys.exit(0 if res else 1)
