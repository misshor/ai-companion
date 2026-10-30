# -*- coding: utf-8 -*-
"""
第一个 Agent 项目的第 1 步：让 AI 回一句话。

目标（今晚只做这个）：
    终端里跑这句脚本，屏幕上出现一句 AI 回你的话。

你现在只有一件事要做：把 ask_ai() 里的三处 TODO 填上。
别的都不要改。
"""
import brain
import memory


def main():
    history = memory.load()
    while True:
        ask  = input("我：").strip()
        if ask == "退出":
            break
        history.append({"role":"user","content":ask})
        memory.save("user",ask)
        # reply = brain.ask_ai([{"role":"system","content":brain.SYSTEM}] + history[-10:])
        tail = history[-10:]
        if tail and tail[0]["role"] == "assistant":
            tail = tail[1:]
        reply = brain.ask_ai([{"role": "system", "content": brain.SYSTEM}] + tail)
        history.append({"role":"assistant","content":reply})
        memory.save("assistant",reply)
        print("小星:" + reply)

if __name__ == "__main__":
    main()