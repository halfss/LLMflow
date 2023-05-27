#coding=utf8
from langchain.utilities import BingSearchAPIWrapper
from configs.model_config import BING_SEARCH_URL, BING_SUBSCRIPTION_KEY

from stands.message import *

from utils import net

class bing_search:
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def run(self):
        if not (BING_SEARCH_URL and BING_SUBSCRIPTION_KEY):
            response = {"snippet": "please set BING_SUBSCRIPTION_KEY and BING_SEARCH_URL in os ENV",
                    "title": "env inof not fould",
                    "link": "https://python.langchain.com/en/latest/modules/agents/tools/examples/bing_search.html"}
        else:
            search = BingSearchAPIWrapper(bing_subscription_key=BING_SUBSCRIPTION_KEY,
                                          bing_search_url=BING_SEARCH_URL)
            response = search.results(self.data_dict['data']['user_input'], num_results=3)

        message = ChatMessage(
                question=self.data_dict['data']['user_input'],
                response=str(response),
                history=[],
                source_documents=[])
        net.send_sse_message(message.dict())
        return message.dict()
