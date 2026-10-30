import os.path

from datetime import datetime

def save(role,content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("chat_log.txt","a",encoding="utf-8") as f:
        f.write(f"{now}|{role}|{content}\n")

def load():
    x = []
    if os.path.exists("chat_log.txt"):
        with open("chat_log.txt","r",encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                x.append({"role":parts[1], "content":parts[2]})
            return x
    else:
        return [ ]


