# -*- coding: utf-8 -*-
"""
把 brain.ask_ai 变成一个 HTTP 接口。

跑法（在 ai-companion 目录下）：
    D:\python\python.exe -m uvicorn server:app --reload
然后浏览器打开：
    http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from pydantic import BaseModel
import brain
import db_memory as memory
from fastapi import HTTPException

app = FastAPI()

sessions = {}
CRISIS_WORDS = [ "自杀", "想死", "不想活", "活不下去", "不想活着",
    "结束生命", "轻生", "一了百了", "不想醒来",
    "自残", "割腕", "跳楼", "吃安眠药", "烧炭",
    "消失就好了", "不想存在", "我是累赘",
    "没有未来了", "活着没意义",]
WEAK_WORDS = [
    "撑不住", "好累", "没意义", "熬不下去", "不想麻烦",
    "没人在乎", "一个人扛", "看不到希望",
]
CRISIS_REPLY = """听你这么说，我很担心你。

现在的痛苦是真的，但你不用一个人扛着。请打 12356（全国心理援助热线，24 小时），
或者现在就告诉一个你信得过的人。如果情况紧急，直接打 120。

我在这儿，但我能做的有限，你需要真人的帮助。
"""

class ChatIn(BaseModel):
    """定义"进来的数据长什么样"。前端必须按这个形状发，否则 422。"""
    user_id:str
    message: str

@app.post("/chat")
def chat(data: ChatIn):
    # 这一行看不懂没关系，它只是告诉 FastAPI：
    #   "这个方法处理 POST /chat，收到的数据是 ChatIn 形状"
    # TODO 1：把 data.message 组成 messages 列表
    #         形状跟你 chat_v2.py 里一样：[{"role":"system",...}, {"role":"user",...}]
    history = sessions.get(data.user_id)
    if history is None:
        history = memory.load(data.user_id)[-20:]
        sessions[data.user_id] = history
    history.append({"role": "user", "content": data.message})
    if any(w in data.message for w in CRISIS_WORDS):
        reply = CRISIS_REPLY
        history.append({"role":"assistant", "content":reply})
        memory.save(data.user_id,"user",data.message)
        memory.save(data.user_id,"assistant",reply)
        sessions[data.user_id] = history[-20:]
        return {"reply": reply,"crisis":True}
    system_now = brain.SYSTEM
    if any(w in data.message for w in WEAK_WORDS):
        system_now = brain.SYSTEM + "（注意：用户情绪可能很危险，这一轮不要追问细节，先确认他此刻是否安全。）"
    try:
        reply = brain.ask_ai([{"role": "system", "content": system_now}] + history[-10:])
    except Exception:
        history.pop()
        raise HTTPException(status_code=503, detail="小星暂时不在，稍后再试")

    history.append({"role": "assistant", "content": reply})
    memory.save(data.user_id, "user", data.message)
    memory.save(data.user_id, "assistant", reply)
    sessions[data.user_id] = history[-20:]
    # TODO 2：调 brain.ask_ai(上面那个列表)，拿回复

    # TODO 3：return 一个字典，形如 {"reply": 回复内容}
    return {"reply":reply}
