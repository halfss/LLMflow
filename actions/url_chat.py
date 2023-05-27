#coding=utf8
import os
import asyncio

from langchain.document_loaders import PlaywrightURLLoader
from langchain.document_loaders import SeleniumURLLoader
from langchain.document_loaders import UnstructuredURLLoader


from stands.message import *
from models import get_llm
from utils import net

from configs import model_config

class url_chat:
    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.llm = get_llm.llm()

    #必须实现
    def run(self):

        urls = self.data_dict['data']['urls']

        loader = UnstructuredURLLoader(urls=urls)
        data = loader.load()

        data = "\n".join([doc.page_content for doc in data])

        input_data = {
                "type": "web_chat",
                "args": {"context": "context", "question": "question"},
                "data": {"context": data, "question": self.data_dict['data']['user_input']},
                "run_type": "frontend"
                }

        message = self.llm.llmchat(input_data)

        return message
