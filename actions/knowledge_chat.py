#coding=utf8
import os

from stands.message import *

from models import get_llm
from utils import net
from chains.local_doc_qa import LocalDocQA

from configs import model_config

class knowledge_chat:
    def __init__(self, data_dict):
        self.data_dict = data_dict
        self.llm = get_llm.llm()


        self.local_doc_qa = LocalDocQA()
        self.local_doc_qa.init_cfg(
            llm_model=get_llm.llm(),
            embedding_model=model_config.EMBEDDING_MODEL,
            embedding_device=model_config.EMBEDDING_DEVICE,
            top_k=model_config.VECTOR_SEARCH_TOP_K,
        )

    #必须实现
    def run(self):
        
        question = self.data_dict['data']['user_input']
        vs_path = os.path.join(model_config.VS_ROOT_PATH, self.data_dict['data']['knowledge_base_id'])

        responses_message = self.local_doc_qa.get_knowledge_based_answer(
                query=question, vs_path=vs_path, chat_history=self.data_dict['data'].get('history') or [])

        
        if self.data_dict['data'].get('history'):
            history.append([question, responses_message.response])
        responses_message['question'] = question

        return responses_message
