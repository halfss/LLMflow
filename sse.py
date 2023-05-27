import asyncio
import uvicorn
import time


from fastapi import Body, FastAPI, File, Form, Query, UploadFile, WebSocket, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from configs.model_config import (VS_ROOT_PATH, UPLOAD_ROOT_PATH, EMBEDDING_DEVICE, EMBEDDING_MODEL, NLTK_DATA_PATH, VECTOR_SEARCH_TOP_K, LLM_HISTORY_LEN, OPEN_CROSS_DOMAIN)

from stands.message import *

app = FastAPI()

message_queue = []


@app.post("/send-message")
async def send_message(message: ChatMessage):
    # 将收到的消息添加到消息队列中
    message_queue.append(message.json(ensure_ascii=False))
    return {"message": "Message sent"}


@app.get("/stream")
async def stream_data(response: Response):
    async def event_stream():
        while True:
            if message_queue:
                # 如果消息队列中有新消息，则发送给客户端
                message = message_queue.pop(0)
                yield f"data: {message}\n\n"
            else:
                await asyncio.sleep(0.1)

    response.headers["Content-Type"] = "text/event-stream"
    return StreamingResponse(event_stream(), media_type="text/event-stream")


def api_start(host, port):
    global app

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

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    api_start('0.0.0.0', 7862)
