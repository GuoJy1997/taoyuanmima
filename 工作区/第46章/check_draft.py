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
        "假孙绰煽动围攻桓伟": any(k in body for k in ["韩卓此贼", "桓温野心勃勃", "借刀杀人", "夷其三族"]),
        "桓伟惨白辩解": any(k in body for k in ["休得血口喷人", "家兄", "何曾"]),
        "周彦咬出司药": "司药" in body and "周彦" in body,
        "苏晚晴鉴古兰亭诗": any(k in body for k in ["游", "仙"]) and any(k in body for k in ["回锋", "露怯", "顿挫", "顿滞"]),
        "老莫辨佛理破神仙腔": any(k in body for k in ["支道林", "支遁"]) and any(k in body for k in ["般若", "道贤论"]) and any(k in body for k in ["尸解", "神仙"]),
        "秦华指出肌肉如弓与逃遁破绽": any(k in body for k in ["紧绷", "弓"]) and any(k in body for k in ["抓地", "扣地"]) and any(k in body for k in ["退路", "竹林"]),
        "谢万暴烈按人厉喝": any(k in body for k in ["拿贼", "按实"]),
        "认知喊风骨最响者是下毒元凶": any(k in body for k in ["风骨", "投毒", "下毒"]),
        "章末假面蹭破露出蜡黄陌生皮肤": any(k in body for k in ["蹭", "卷", "破"]) and any(k in body for k in ["蜡黄", "陌生"])
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
