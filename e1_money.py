# -*- coding: utf-8 -*-
"""
复习题 E1 · 简易记账本（重建版）

背景：原来的 review.py 没跟过来，所以这题不是"改三行"，是"从头写一遍"。
      交接文档里记着：你的逻辑没问题，卡在 read_total() 忘了遍历文件。
      这次从头写，正好验证是真会了还是只记住了当时那几行。

【需求】（读三遍，然后按"四步翻译法"圈名词圈动词，别急着敲代码）
1. 程序启动时：先从 money.txt 读出历史上每一笔金额，累加，打印「当前总额：XX」
2. 然后进入循环：每次输入一个金额（比如 50），把这一笔追加写进 money.txt
   文件里每行格式：日期+金额   → 例如  2026-10-26+50
3. 输入「退出」结束，最后打印「最终总额：XX」

【验收标准】（这个必须过，否则不算通关）
   先记 50 → 再记 30 → 输入 退出
   关掉程序，重新运行
   一启动就要显示「当前总额：80.0」
   再记一笔 20，退出，再运行一次 → 显示 100.0

【规矩】
- 不许去网上抄，也不许把整段需求丢给 AI 让它写全
- 写完自己先跑，把**真实输出**贴给我（我不要"应该没问题"，我要看数字）
"""

import os
from datetime import datetime

FILE = "money.txt"


def write_one(amount):
    """把一笔金额追加写入文件。amount 是已经转好的 float，这里不用管转换。"""
    # TODO 1：用 "a" 模式打开 FILE（记得 encoding="utf-8"）
    #         往里写一行：日期 + "+" + 金额 + 换行
    #         日期用 datetime.now().strftime("%Y-%m-%d") 拿
    #         提示：写进文件的永远是字符串，即使 amount 是数字
    with open("money.txt","a",encoding = "utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d")
        f.write(f"{now}+{amount}\n")

def read_total():
    """从文件读出所有金额并累加，返回总和（float）。文件不存在时返回 0。"""
    # TODO 2：文件不存在怎么办？（Day 9 学的 os.path.exists）先挡掉，直接返回 0
    # TODO 3：total = 0 该写在 for 循环之前，还是 for 里面？
    #         这个"位置"你 Day 4 踩过坑（count = 0），想清楚再写
    #         注意：真正的死线是"for 之前"，不是"with 之前"——Python 没有块级作用域
    # TODO 4：with open(...) as f:  然后 遍历每一行
    #         每一行长这样：2026-10-26+50
    #         你要做的是：从里面切出 "50" → 转成数字 → 累加到 total
    #         ★ 提示：D2 你已经写对过 "for line in f + 一行行处理" 的结构，
    #                 这一题是同一个骨架，唯一变化是：
    #                 原来每读到一行就 count +1，现在每读到一行就 total += 金额
    # TODO 5：把总和 return 出去（注意：不是 print）
    if not os.path.exists("money.txt"):
        return 0
    else:
        with open("money.txt", "r", encoding="utf-8") as f:
            total = 0
            for line in f:
                parts = line.split("+")
                if len(parts) < 2:
                    continue
                total = total + float(parts[1])

            return total

def main():
    # TODO 6：程序一启动，先拿历史总额，打印「当前总额：XX」
    #         顺便打印一句「读到 N 条记录」——这句能让你一眼看出文件到底读到没
    # TODO 7：while True 循环
    #           input 要 .strip()（Day 5 学过的那个坑）
    #           "退出" → 结束循环（注意 print「最终总额」该写在循环里还是外面）
    #           否则 → 用户输进来的是一串字符，得先转 float
    #                 转不了怎么办？（try/except，Day 6 用过）
    #                 → 写进文件
    #                 → 总额加上这一笔，打印最新的总额
    total = read_total()
    print(f"当前总额：{total}元")
    while True:
        n = input("输入金额").strip()
        if n == "退出":
            break
        try:
            money = float(n)
        except:
            ValueError
            print("类型不对,重新输入")
            continue
        write_one(money)
        total = money+total
        print(f"当前总额：{total}元")
    print(f"总金额{total}元")

if __name__ == "__main__":
    main()



