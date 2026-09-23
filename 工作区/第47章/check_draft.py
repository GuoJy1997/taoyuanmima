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
        print("PASSED: 纯汉字数在 1800 ~ 2500 范围内。")
    else:
        print(f"FAILED: 纯汉字数 {chinese_chars} 不在 1800 ~ 2500 范围内！")

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

    # Dialogue density check (< 200 chars non-dialogue)
    print(f"\n=== 对话密度红线检测 (连续非对白严禁超过200字) ===")
    non_dialogue_blocks = re.split(r'“[^”]*”', body)
    max_block_len = 0
    over_blocks = []
    for idx, block in enumerate(non_dialogue_blocks):
        clean_b = re.sub(r'\s', '', block)
        if len(clean_b) > max_block_len:
            max_block_len = len(clean_b)
        if len(clean_b) > 150:
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

    # Key Plot Anchors
    print(f"\n=== 核心情节与对白锚点检测 ===")
    anchors = {
        "杜子恭指出邪阵仍被喂养/生门闭合": any(k in body for k in ["生门", "邪阵", "阴煞", "喂养"]),
        "名士围攻桓伟欲定桓温通敌": any(k in body for k in ["荆州", "通敌", "谋反", "桓温", "国贼"]),
        "王羲之喝止劝解": any(k in body for k in ["右军", "王羲之", "逸少"]) and any(k in body for k in ["住手", "自相残杀", "何苦"]),
        "郗超揭刘弼才是大奸细": "郗超" in body and "刘弼" in body and any(k in body for k in ["管家", "大蠹", "隐匿"]),
        "顾君三重物证(朱砂/名单/配方)": any(k in body for k in ["朱砂", "皂靴"]) and any(k in body for k in ["名册", "四十二人"]) and any(k in body for k in ["配方", "府库", "原料"]),
        "老莫耳语提醒桓温隐匿": "老莫" in body and any(k in body for k in ["若桓温隐匿此间", "没人走得了", "全场皆死"]),
        "顾君政治切割保全众人": any(k in body for k in ["背主", "私自", "并非桓公", "绝非桓公", "借刀杀人"]),
        "解药逆转低期/军阵抹杀4期": any(k in body for k in ["解药", "水雾", "逆转"]) and any(k in body for k in ["死士", "出刀", "军阵", "抹杀"]),
        "杜子恭牺牲遗言": "仪式的源头已经被污染了……无论落入谁手，都不是苍生之福……" in body,
        "刘弼替身斩首": any(k in body for k in ["替身", "呆滞", "傀儡"]) and any(k in body for k in ["断首", "斩首", "人头"]),
        "章末普通护卫微点头": any(k in body for k in ["微点", "点了一下头"]) and any(k in body for k in ["护卫", "铁甲"])
    }
    all_passed = True
    for name, passed in anchors.items():
        status = 'PASSED' if passed else 'FAILED'
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    return len(found_banned) == 0 and len(over_blocks) == 0 and 1800 <= chinese_chars <= 2500 and all_passed

if __name__ == '__main__':
    res = audit_chapter(sys.argv[1])
    sys.exit(0 if res else 1)
