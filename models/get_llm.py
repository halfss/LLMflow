from configs import model_config

import models

def llm():
    llm = getattr(models, model_config.LLM_MODEL)
    return getattr(llm, model_config.LLM_MODEL)()
