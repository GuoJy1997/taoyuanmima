import re
import sys

def audit_chapter(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separate YAML frontmatter if present
    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]

    # Metrics
    chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', body))
    no_space_chars = len(re.sub(r'\s', '', body))
    
    print(f"=== 字数统计 ===")
    print(f"正文纯汉字数: {chinese_chars}")
    print(f"正文去空白字符总数(含标点): {no_space_chars}")
    if 1800 <= chinese_chars <= 2500:
        print("PASSED: 字数在 1800 ~ 2500 字之间。")
    else:
        print(f"FAILED: 字数不满足 1800 ~ 2500 要求 (当前: {chinese_chars})")

    # Banned words
    banned = [
        "一死生", "齐彭殇", "虚诞", "妄作", "传国玉玺",
        "宛如", "仿佛在诉说着", "在这一刻时间静止",
        "不仅如此", "更重要的是", "殊不知",
        "嘴角勾起一抹弧度", "倒吸一口凉气"
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

    # Required key phrases
    print(f"\n=== 必须包含金句检测 ===")
    req1 = "这刘弼真够能干的，把桓家那边安排得明明白白——比管家还管家"
    req2_v2 = "裴俭被生生拖出斩杀时，在场没有一个人替他说哪怕半句话。"
    req2_v1 = "裴俭被拖下去时，没有一个人替他说话。"
    passed_req2 = req2_v2 in body or req2_v1 in body
    print(f"张洋金句: {'PASSED' if req1 in body else 'FAILED'}")
    print(f"章末收尾句: {'PASSED' if passed_req2 else 'FAILED'}")

    # Dialogue density check (< 200 chars non-dialogue)
    print(f"\n=== 对话密度红线检测 (连续非对白严禁超过200字) ===")
    non_dialogue_blocks = re.split(r'“[^”]*”', body)
    max_block_len = 0
    over_blocks = []
    for idx, block in enumerate(non_dialogue_blocks):
        clean_b = re.sub(r'\s', '', block)
        if len(clean_b) > max_block_len:
            max_block_len = len(clean_b)
        if len(clean_b) > 200:
            over_blocks.append((idx, len(clean_b), clean_b[:40] + '...'))

    print(f"最大连续非对白长度: {max_block_len} 字")
    if over_blocks:
        print(f"FAILED: 发现 {len(over_blocks)} 处超过 200 字无对白区间:")
        for idx, l, snippet in over_blocks:
            print(f"  块 {idx}: {l} 字 -> {snippet}")
    else:
        print("PASSED: 所有非对白区间均严格低于 200 字！")

    # Plot anchors
    print(f"\n=== 核心情节锚点检测 ===")
    anchors = {
        "张洋摸向马厩车辕区": any(k in body for k in ["马厩", "车辕", "草料"]),
        "刘弼井井有条调度": all(k in body for k in ["刘弼", "调度"]),
        "张洋惊叹比管家还管家": "比管家还管家" in body,
        "秦华老练沉稳接话": "秦华" in body and any(k in body for k in ["人才", "防务", "井井有条"]),
        "荆州精锐甲士突袭": any(k in body for k in ["荆州", "甲士", "重甲"]),
        "裴俭被擒拿定罪": "裴俭" in body and any(k in body for k in ["拿办", "暗通", "勾结", "拿下"]),
        "剥除裴俭冠带": any(k in body for k in ["冠带", "高冠", "头冠"]),
        "名士冷漠无一人说话": any(k in body for k in ["没有一个人", "冷眼", "避嫌", "视若无睹"])
    }
    for name, passed in anchors.items():
        print(f"  {name}: {'PASSED' if passed else 'FAILED'}")

if __name__ == '__main__':
    audit_chapter(sys.argv[1])
