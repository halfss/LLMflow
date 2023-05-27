from langchain.prompts import PromptTemplate, ChatPromptTemplate


def prompt_data():
    return {
        "answer":{
            "template": "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: {text} \nASSISTANT:",
            "input": ["text"],
            "chinese": "问答"
            },
        "summary": {
            "template": "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: 对下面内容做个总结: {text} \nASSISTANT:",
            "input": ["text"],
            "chinese": "总结"
            },
        "problem": {
            "template": "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions. USER: 下面这段描述有什么潜在的问题: {text} \nASSISTANT:",
            "input": ["text"],
            "chinese": "风险分析"
            },
        "knowledge": {
            "template": '''已知信息：\n{context}\n\n根据上述已知信息，简洁和专业的来回答用户的问题。如果无法从中得到答案，请说 “根据>已知信息无法回答该问题” 或 “没有提供足够的相关信息”，不允许在答案中添加编造成分，答案请使用中文。 问题是：{question}''',
            "input": ["context", "question"],
            }

        }

def get_prompt(name, data):

    prompt_dict = prompt_data()

    string_prompt = PromptTemplate.from_template(prompt_dict[name]['template'])
    string_prompt_value = string_prompt.format_prompt(**data)

    return string_prompt_value.to_string()

