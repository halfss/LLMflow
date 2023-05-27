import torch.cuda
import torch.backends
import os
import logging
import uuid

LOG_FORMAT = "%(levelname) -5s %(asctime)s" "-1d: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)

embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "/data/models/GanymedeNil/text2vec-large-chinese",
}

# Embedding model name
EMBEDDING_MODEL = "text2vec"

# Embedding running device
#EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
EMBEDDING_DEVICE = "cpu"


# LLM 名称
LLM_MODEL = "openai_api"
# 如果你需要加载本地的model，指定这个参数  ` --no-remote-model`，或者下方参数修改为 `True`

VS_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_store")

UPLOAD_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content")

# 文本分句长度
SENTENCE_SIZE = 100

# 匹配后单段上下文长度
CHUNK_SIZE = 250

# LLM input history length
LLM_HISTORY_LEN = 3

# return top-k text chunk from vector store
VECTOR_SEARCH_TOP_K = 5

# 知识检索内容相关度 Score, 数值范围约为0-1100，如果为0，则不生效，经测试设置为小于500时，匹配结果更精准
VECTOR_SEARCH_SCORE_THRESHOLD = 0

NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")

FLAG_USER_NAME = uuid.uuid4().hex

logger.info(f"""
loading model config
embedding device: {EMBEDDING_DEVICE}
dir: {os.path.dirname(os.path.dirname(__file__))}
flagging username: {FLAG_USER_NAME}
""")

# 是否开启跨域，默认为False，如果需要开启，请设置为True
# is open cross domain
OPEN_CROSS_DOMAIN = True

# Bing 搜索必备变量
# 使用 Bing 搜索需要使用 Bing Subscription Key
# 具体申请方式请见 https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/quickstarts/rest/python
BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"
BING_SUBSCRIPTION_KEY = ""
