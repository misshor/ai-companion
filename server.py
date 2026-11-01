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
import memory
from fastapi import HTTPException

app = FastAPI()

sessions = {}

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
    try:
        reply = brain.ask_ai([{"role": "system", "content": brain.SYSTEM}] + history[-10:])
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
