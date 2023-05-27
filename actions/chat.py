#coding=utf8

from models import get_llm

from stands.message import *
from stands.prompt import get_prompt

from utils import net

class chat:
    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.llm = get_llm.llm()

    #必须实现
    def run(self):
        return self.llm.llmchat(self.data_dict)
