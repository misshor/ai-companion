import os.path

from datetime import datetime

def save(user_id,role,content):
    content = content.replace("\n", "\\n")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("chat_log.txt","a",encoding="utf-8") as f:
        f.write(f"{now}|{user_id}|{role}|{content}\n")

def load(user_id):
    x = []
    if os.path.exists("chat_log.txt"):
        with open("chat_log.txt","r",encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) < 4:
                    continue
                if parts[1] != user_id:  
                    continue
                content = parts[3].replace("\\n", "\n")
                x.append({"role":parts[2], "content":content})
            return x
    else:
        return [ ]


