
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()


def Tongyi():
    return ChatOpenAI(
        model="qwen-max",
        api_key=os.environ.get("DASHSCOPE_API_KEY"),  # 自行搞定  你的秘钥
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )