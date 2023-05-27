import os
import requests
import json

from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


from stands import prompt as stand_prompt

from stands.message import *

prompt_data = stand_prompt.prompt_data()

os.environ["OPENAI_API_KEY"] =  "EMPTY"
os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"


class openai_api():
    def __init__(self):
        pass

    def llmchat(self, user_input_data):
        model = "vicuna-7b-v1.1"

        streaming = False
        if user_input_data.get('run_type', 'backend') == 'frontend':
            streaming = True
    
        _prompt = prompt_data[user_input_data['type']]
    
        prompt = PromptTemplate(template=_prompt['template'], 
                input_variables=_prompt['input'])
    
        real_input_argvs = {}
        for show_input_argv in _prompt['input']:
            #获取到prompt中需要输入的键与用户的那个输入对应
            data_key = user_input_data['args'].get(show_input_argv, '')
    
            #通过对应的键,获取到真正的输入
            real_input_argv = user_input_data['data'][data_key]
            real_input_argvs[show_input_argv]=real_input_argv
    
        llm = OpenAI(model_name=model, 
                streaming=streaming)


        real_prompt = prompt.format_prompt(**real_input_argvs)

        #全部响应值
        responses = ''

        #use langchain openai wrapper
        #there problem at streaming
        #llm_chain = LLMChain(prompt=prompt, llm=llm)
        #result = llm_chain.run(**real_input_argvs)

        #for response in result:
        #    sendsse_sse_message(response)
        #    responses += response


        host = "http://localhost:8000"

        real_prompt_str = real_prompt.to_string()

        max_input = 1536

        for str_i in range(0, len(real_prompt_str)+1, max_input):
            _real_prompt_str = real_prompt_str[str_i:str_i+max_input]

            data = {
                  "model": "vicuna-7b-v1.1",
                  "prompt": _real_prompt_str,
                  "max_tokens":512,
                  "temperature": 0.1,
                  "stream": streaming
                }


            llm_r = requests.post('%s/v1/completions' % host, json=data, stream=streaming)
            over = False
            for line in llm_r.iter_lines(decode_unicode=True):
                if "data: " in line:
                    resp = json.loads(line[6:])
                    response = resp['choices'][0]['text']
                    over = resp['choices'][0]['finish_reason']

                    responses += response
                    sendsse_sse_message(response)

                if over:
                    break

        message = ChatMessage(
            question='',
            response=responses,
            history=[],
            source_documents=[],
        )

        return message.dict()
