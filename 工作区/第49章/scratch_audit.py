import re

def main():
    with open('D:/桃园密码/工作区/第49章/03_去AI味润色稿.md', 'r', encoding='utf-8') as f:
        text = f.read()

    body = text.split('---', 2)[2] if '---' in text else text

    # 1. 汉字字数
    hanzi = re.findall(r'[\u4e00-\u9fa5]', body)
    no_space = re.sub(r'\s', '', body)
    print(f'正文纯汉字数: {len(hanzi)}')
    print(f'正文去空白总字符数(含标点): {len(no_space)}')

    # 2. 禁词检查
    banned = [
        '一死生', '齐彭殇', '虚诞', '妄作',
        '宛如', '仿佛在诉说着', '在这一刻时间静止', '在这一刻时间凝固',
        '不仅如此', '更重要的是', '殊不知', '嘴角勾起一抹弧度',
        '嘴角勾起', '倒吸一口凉气', '倒吸凉气', '眼神中闪烁着坚定的光芒'
    ]
    banned_hits = [b for b in banned if b in body]
    print(f'命中禁词列表: {banned_hits}')

    # 3. 连续非对白字数 (无引号)
    # 匹配中文引号 “...”
    dialogues = re.findall(r'“[^”]*”', body)
    blocks = re.split(r'“[^”]*”', body)
    over_150 = []
    over_200 = []
    max_len = 0
    for i, block in enumerate(blocks):
        clean = re.sub(r'\s', '', block)
        if len(clean) > max_len:
            max_len = len(clean)
        if len(clean) > 150:
            over_150.append((i, len(clean), clean[:40]))
        if len(clean) > 200:
            over_200.append((i, len(clean), clean[:40]))

    print(f'总对白句数: {len(dialogues)}')
    print(f'最大连续非对白字符数: {max_len}')
    print(f'超过150字无对白区块数: {len(over_150)}')
    for item in over_150:
        print(f'  [>150] 块 {item[0]}: 长度 {item[1]}, 开头: {item[2]}')
    print(f'超过200字无对白区块数: {len(over_200)}')

    # 4. 关键要素核验
    elements = {
        "桓温卸容": ["紫石棱", "猬毛磔", "桓温", "大司马"],
        "传国玉玺": ["方圆四寸", "五龙", "黄金", "受命于天，既寿永昌"],
        "招魂召令": ["招魂召令", "终极裁决者", "因果"],
        "路线碰撞": ["十万", "收复中原", "朝堂", "国祚", "你怎么选"],
        "队友表现": ["秦华", "张洋", "白艺", "苏晚晴", "老莫"],
        "章末落点": ["决定天下走向的筹码", "三个历史巨头"]
    }

    print("\n关键剧情要素匹配统计:")
    for cat, kws in elements.items():
        print(f"[{cat}]")
        for kw in kws:
            print(f"  {kw}: {body.count(kw)} 次")

    # 5. 逐段分析大纲与知情边界
    # 检查是否有顾君透视他人心理
    # 检查是否有秦华可疑行为

if __name__ == '__main__':
    main()
