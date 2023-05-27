import argparse
import json
import os
import shutil
from typing import List, Optional, Dict, Any
import urllib
import asyncio


import nltk
import pydantic
import uvicorn
from fastapi import Body, FastAPI, File, Form, Query, UploadFile, WebSocket, Response, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing_extensions import Annotated
from starlette.responses import RedirectResponse

from chains.local_doc_qa import LocalDocQA
from configs import model_config
from configs.model_config import (VS_ROOT_PATH, UPLOAD_ROOT_PATH, EMBEDDING_DEVICE, EMBEDDING_MODEL, NLTK_DATA_PATH, VECTOR_SEARCH_TOP_K, LLM_HISTORY_LEN, OPEN_CROSS_DOMAIN)

from stands.message import *
from stands import prompt as stand_prompt

import actions

from utils import net

nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path


app = FastAPI()

class ActionInput(BaseModel):
    action: str
    input: Dict[str, Any]

class ActionOutput(BaseModel):
    output: Optional[Dict[str, Any]] = None

@app.post("/run_action")
async def run_action(action_input: ActionInput) -> ActionOutput:
    # 在这里根据 action 和 input 执行相应的逻辑处理
    if not isinstance(action_input, dict):
        action_input = action_input.dict()
    action = action_input['action']
    input_data = action_input['input']

    # 得到对应的类
    # 在actions目录下,需要有一个和action同名的文件
    # 在这文件中,需要有一个和action同名的类
    # 在这个类里需要有一个run的函数,这个函数将input_data作为输入,进行执行
    _class = getattr(actions, action)
    _class = getattr(_class, action)

    action_class = _class(input_data)

    # 构建返回的上下文输出
    output_data = action_class.run()

    print("output_data")
    print(output_data)

    context_output = ActionOutput(output=output_data)
    return context_output

class ChainInput(BaseModel):
    user_input: str
    chain: List[Dict[str, Any]]

@app.post("/run_chain")
async def run_chain(chain_input: ChainInput) -> ActionOutput:
    # 在这里根据 action 和 input 执行相应的逻辑处理
    user_input = chain_input.user_input
    chain = chain_input.chain

    loop = 0
    action_input = user_input
    for chain_action in chain:
        if chain_action['action'] == 'bing_search':
            _action_input = action_input
        elif chain_action['action'] == 'chat':
            if chain_action['input']['type'] == 'answer':
                _action_input = "基于下面这些内容:\n%s\n回答这个问题:%s" % (action_input, chain_action['input']['data']['user_input'])
            elif chain_action['input']['type'] == 'summary':
                _action_input = action_input
            elif chain_action['input']['type'] == 'problem':
                _action_input = action_input

        chain_action['input']['data']['user_input'] = _action_input
        
        loop += 1
        sendsse_sse_message("\n第%s/%s步开始执行...\n" % (loop, len(chain)))
        action_return = await run_action(chain_action)

        sendsse_sse_message("\n第%s/%s步执行结束\n" % (loop, len(chain)))

        action_input = action_return.output['response']

    return action_return


@app.get("/prompts")
async def prompts() -> ActionOutput:
    prompts = stand_prompt.prompt_data()
    context_output = ActionOutput(output=prompts)
    return context_output


def get_folder_path(local_doc_id: str):
    return os.path.join(UPLOAD_ROOT_PATH, local_doc_id)

def get_vs_path(local_doc_id: str):
    return os.path.join(VS_ROOT_PATH, local_doc_id)


def get_file_path(local_doc_id: str, doc_name: str):
    return os.path.join(UPLOAD_ROOT_PATH, local_doc_id, doc_name)


async def upload_file(
        file: UploadFile = File(description="A single binary file"),
        knowledge_base_id: str = Form(..., description="Knowledge Base Name", example="kb1"),
):
    saved_path = get_folder_path(knowledge_base_id)
    if not os.path.exists(saved_path):
        os.makedirs(saved_path)

    file_content = await file.read()  # 读取上传文件的内容

    file_path = os.path.join(saved_path, file.filename)
    if os.path.exists(file_path) and os.path.getsize(file_path) == len(file_content):
        file_status = f"文件 {file.filename} 已存在。"
        return BaseResponse(code=200, msg=file_status)

    with open(file_path, "wb") as f:
        f.write(file_content)

    vs_path = get_vs_path(knowledge_base_id)
    vs_path, loaded_files = local_doc_qa.init_knowledge_vector_store([file_path], vs_path)
    if len(loaded_files) > 0:
        file_status = f"文件 {file.filename} 已上传至新的知识库，并已加载知识库，请开始提问。"
        return BaseResponse(code=200, msg=file_status)
    else:
        file_status = "文件上传失败，请重新上传"
        return BaseResponse(code=500, msg=file_status)


async def upload_files(
        files: Annotated[
            List[UploadFile], File(description="Multiple files as UploadFile")
        ],
        knowledge_base_id: str = Form(..., description="Knowledge Base Name", example="kb1"),
):
    saved_path = get_folder_path(knowledge_base_id)
    if not os.path.exists(saved_path):
        os.makedirs(saved_path)
    filelist = []
    for file in files:
        file_content = ''
        file_path = os.path.join(saved_path, file.filename)
        file_content = file.file.read()
        if os.path.exists(file_path) and os.path.getsize(file_path) == len(file_content):
            continue
        with open(file_path, "ab+") as f:
            f.write(file_content)
        filelist.append(file_path)
    if filelist:
        vs_path, loaded_files = local_doc_qa.init_knowledge_vector_store(filelist, get_vs_path(knowledge_base_id))
        if len(loaded_files):
            file_status = f"已上传 {'、'.join([os.path.split(i)[-1] for i in loaded_files])} 至知识库，并已加载知识库，请开始提问"
            return BaseResponse(code=200, msg=file_status)
    file_status = "文件未成功加载，请重新上传文件"
    return BaseResponse(code=500, msg=file_status)


async def list_docs(
        knowledge_base_id: Optional[str] = Query(default=None, description="Knowledge Base Name", example="kb1")
):
    if knowledge_base_id:
        local_doc_folder = get_folder_path(knowledge_base_id)
        if not os.path.exists(local_doc_folder):
            return {"code": 1, "msg": f"Knowledge base {knowledge_base_id} not found"}
        all_doc_names = [
            doc
            for doc in os.listdir(local_doc_folder)
            if os.path.isfile(os.path.join(local_doc_folder, doc))
        ]
        return ListDocsResponse(data=all_doc_names)
    else:
        if not os.path.exists(UPLOAD_ROOT_PATH):
            all_doc_ids = []
        else:
            all_doc_ids = [
                folder
                for folder in os.listdir(UPLOAD_ROOT_PATH)
                if os.path.isdir(os.path.join(UPLOAD_ROOT_PATH, folder))
            ]

        return ListDocsResponse(data=all_doc_ids)


async def delete_docs(
        knowledge_base_id: str = Query(...,
                                       description="Knowledge Base Name(注意此方法仅删除上传的文件并不会删除知识库(FAISS)内数据)",
                                       example="kb1"),
        doc_name: Optional[str] = Query(
            None, description="doc name", example="doc_name_1.pdf"
        ),
):
    knowledge_base_id = urllib.parse.unquote(knowledge_base_id)
    if not os.path.exists(os.path.join(UPLOAD_ROOT_PATH, knowledge_base_id)):
        return {"code": 1, "msg": f"Knowledge base {knowledge_base_id} not found"}
    if doc_name:
        doc_path = get_file_path(knowledge_base_id, doc_name)
        if os.path.exists(doc_path):
            os.remove(doc_path)
            return BaseResponse(code=200, msg=f"document {doc_name} delete success")
        else:
            return BaseResponse(code=1, msg=f"document {doc_name} not found")

        remain_docs = await list_docs(knowledge_base_id)
        remain_docs = remain_docs.json()
        if len(remain_docs["data"]) == 0:
            shutil.rmtree(get_folder_path(knowledge_base_id), ignore_errors=True)
        else:
            local_doc_qa.init_knowledge_vector_store(
                get_folder_path(knowledge_base_id), get_vs_path(knowledge_base_id)
            )
    else:
        shutil.rmtree(get_folder_path(knowledge_base_id))
        return BaseResponse(code=200, msg=f"Knowledge Base {knowledge_base_id} delete success")

async def document():
    return RedirectResponse(url="/docs")

def api_start(host, port):
    global app
    global local_doc_qa

    # Add CORS middleware to allow all origins
    # 在config.py中设置OPEN_DOMAIN=True，允许跨域
    # set OPEN_DOMAIN=True in config.py to allow cross-domain
    if OPEN_CROSS_DOMAIN:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    app.get("/", response_model=BaseResponse)(document)

    app.post("/local_doc_qa/upload_file", response_model=BaseResponse)(upload_file)
    app.post("/local_doc_qa/upload_files", response_model=BaseResponse)(upload_files)
    app.get("/local_doc_qa/list_files", response_model=ListDocsResponse)(list_docs)
    app.delete("/local_doc_qa/delete_file", response_model=BaseResponse)(delete_docs)


    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    # 初始化消息
    api_start('0.0.0.0', 7861)
