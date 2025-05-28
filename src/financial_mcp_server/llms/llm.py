import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

class OpenAiCompatibleClient:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.client = self._get_client()

    def _get_client(self)->OpenAI:
        load_dotenv()
        client = OpenAI(
            #api_key=os.getenv("DASHSCOPE_API_KEY"),
            #base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        return client

    def send_messages(self, messages):
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
        )
        return response