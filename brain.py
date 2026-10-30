from openai import OpenAI
import config

client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
SYSTEM = "你是小星，说话短、口语，回复不超过五句话不说我理解你的感受这种套话，不列1234点建议。能先接住情绪，再问一句具体的事。如果用户表达自伤或轻生倾向，不要顺着聊，直接表达担心，并建议找身边的人或专业热线。"

def ask_ai(messages):
    """输入：用户说的一句话（字符串）　输出：AI 回的一句话（字符串）"""

    # TODO 1：让 client 发一次请求。
    #         必须告诉它两样：用哪个模型（config.MODEL）、说了什么话。
    #         看提示：client.chat.completions.create(...)
    #         「说了什么话」不是随便一个字符串，是一个列表，列表里装"消息"
    #         每一条消息是字典，两个键：role 和 content
    #         这次只有一个角色够了——那个"设定 AI 怎么说话"的角色
    response = client.chat.completions.create(
        model = config.MODEL,
        messages = messages,
    )
    # TODO 2：把上面那次请求的结果接住，起个名字叫 response
    return response.choices[0].message.content
    # TODO 3：AI 的回话藏在 response 里，取出来 return
    #         路径是：response.choices[0].message.content
