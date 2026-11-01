import os.path

from datetime import datetime

def save(user_id,role,content):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("chat_log.txt","a",encoding="utf-8") as f:
        f.write(f"{now}|{user_id}|{role}|{content}\n")

def load(user_id):
    x = []
    if os.path.exists("chat_log.txt"):
        with open("chat_log.txt","r",encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if parts[1] != user_id:
                    continue
                x.append({"role":parts[2], "content":parts[3]})
            return x
    else:
        return [ ]
if __name__ == "__main__":
    save("alice", "user", "我叫小明")
    save("bob", "user", "我叫什么名字")
    print("alice:", load("alice"))
    print("bob:", load("bob"))

