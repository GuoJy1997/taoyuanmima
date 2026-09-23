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
    req1 = "军队进场！名士带刀！合着千古风流全是给阎王爷打前站"
    req2 = "不在名单上的，未必都是敌人。但名单外的每一个人，都值得再看一眼。"
    print(f"张洋金句: {'PASSED' if req1 in body else 'FAILED'}")
    print(f"老莫收尾金句: {'PASSED' if req2 in body else 'FAILED'}")

    # Dialogue density check (< 200 chars non-dialogue)
    print(f"\n=== 对话密度红线检测 (连续非对白严禁超过200字) ===")
    # Find all text outside “...”
    non_dialogue_blocks = re.split(r'“[^”]*”', body)
    max_block_len = 0
    over_blocks = []
    for idx, block in enumerate(non_dialogue_blocks):
        clean_b = re.sub(r'\s', '', block)
        if len(clean_b) > max_block_len:
            max_block_len = len(clean_b)
        if len(clean_b) > 100:
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

    # Plot anchors
    print(f"\n=== 核心情节锚点检测 ===")
    anchors = {
        "石桥洞六人聚齐/秦华包扎": any(k in body for k in ["包扎", "秦叔", "秦华"]),
        "苏晚晴发现浸油镇灵符": all(k in body for k in ["镇灵符", "桐油"]),
        "药效时差分析": any(k in body for k in ["时差", "距离", "拖延", "发作"]),
        "老莫42人名单": any(k in body for k in ["四十二人", "42人"]),
        "管家刘弼": "刘弼" in body,
        "老仆杜子恭": "杜子恭" in body,
        "杂役韩卓": "韩卓" in body,
        "清谈客裴俭": "裴俭" in body,
        "王绥之叫不出房份": "王绥之" in body and "房份" in body,
        "建立可疑名单/阵营分层": any(k in body for k in ["名单", "同心圆", "暗桩"])
    }
    for name, passed in anchors.items():
        print(f"  {name}: {'PASSED' if passed else 'FAILED'}")

if __name__ == '__main__':
    audit_chapter(sys.argv[1])
