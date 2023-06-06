# 言程

```
用对话为你的每件事定义一智能个小助手
```

--------

## 🚩 平台演示

![演示](https://raw.githubusercontent.com/halfss/LLMflow/master/img/demo.gif)



[完整视频](https://www.bilibili.com/video/BV1To4y1g7gT/?vd_source=45d3792231c93bfb34ab403e73360ac2)

## 🚩 1：项目背景：

##### 💡应用思路

```markdown
原来的用代码只能实现结构化、明确的、规范的流程处理,
这里面有逻辑，但逻辑是写死在代码里面的；不能轻易调整；
但有了LLM之后，对非结构化的数据的处理有了质的提高，逻辑不仅仅可以用代码实现，还可以用口述的语言实现;
那么理论上就可以基于语言借助于平台直接实现业务需求。
```

##### 💡 场景思路：

```markdown
既然可以通过语言实现业务需求，那么就给每个人提供一个自己定义自己业务需求流程的平台；
给自己的每件事都配上一个有思考能力的小助手。
```

##### 💡 技术思路：

```markdown
模型管理：Fastchat
    1: Fastchat模型支持做的比较完善
    2：Fastchat专门做模型管理这块，我们没必要重新做一遍，直接引用是最好的选择

核心库：langchain

后端：python
前端：vue

其他技术点：sse
```

## 🚩2: 平台介绍：

### 1：基础功能：

##### 💡 与文字做交互

- [x] 做分析
  - 一段话中潜在的问题
- [x] 分类：
  - 张三今年没来过医院；张三是否应该归到首次就诊呢？
- [x] 文本信息抽取（结构化）：
  - 从”我的名字是王五，性别为男，去年得得了小细胞癌，没来过咱们医院“提取信息，包括：姓名、性别、患病史、是否来院，以json形式输出
- [x] 流程问答：
  - 张三的治疗流程顺序为：疗程B，疗程A，疗程F，疗程E；现在张三已经完成了疗程A的治疗，下一步应该执行什么疗程？

##### 💡与文档做交互

- [x] 文档总结
- [x] 文档内容提取

##### 💡与网页交互

- [x] http/https
- [ ] RSS

##### 💡与数据库交互

- [ ] mysql
- [ ] oracle

##### 💡与平台交互

- [ ] 调用API

##### 💡执行代码

- [ ] python

### 2：高级功能：

- [ ] 定义流程
  - 基于用户的每步输入，自动得到用户的整个处理流程；后续用户只需要输入初始问题，即可基于这个流程做完成处理，并给出用户
- [ ] 定期执行
  - 每个流程可设置定期执行，并触发对应的流程

## 🚩 3：应用场景：

##### 💡典型场景

- [ ] 路由处理：
  - 基于规范流程文档，输入当前场景状态，给出下一步要进行的流程
- [ ] 文档处理
  - 从非结构化文档中（word，pdf，txt，图片）中按照需求提取结构化数据，整理数据
- [ ] 人文关怀：
  * 针对每个人的情况，编写一段文字，对他进行定期关怀
- [ ] RSS总结：
  * 从特定地址获取内容，并进行总结，发送

##### 💡AI知识库

##### **🎉 有比较有意思的、典型的场景需求，可以一起交流、探讨**

---

### 支持模型列表

Fastchat目前支持的模型，具体见 [连接](https://github.com/lm-sys/FastChat)

- Vicuna, Alpaca, LLaMA, Koala
- [lmsys/fastchat-t5-3b-v1.0](https://huggingface.co/lmsys/fastchat-t5)
- [BlinkDL/RWKV-4-Raven](https://huggingface.co/BlinkDL/rwkv-4-raven)
- [databricks/dolly-v2-12b](https://huggingface.co/databricks/dolly-v2-12b)
- [FreedomIntelligence/phoenix-inst-chat-7b](https://huggingface.co/FreedomIntelligence/phoenix-inst-chat-7b)
- [h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-7b-preview-300bt-v2](https://huggingface.co/h2oai/h2ogpt-gm-oasst1-en-2048-open-llama-7b-preview-300bt-v2)
- [mosaicml/mpt-7b-chat](https://huggingface.co/mosaicml/mpt-7b-chat)
- [OpenAssistant/oasst-sft-1-pythia-12b](https://huggingface.co/OpenAssistant/oasst-sft-1-pythia-12b)
- [project-baize/baize-lora-7B](https://huggingface.co/project-baize/baize-lora-7B)
- [StabilityAI/stablelm-tuned-alpha-7b](https://huggingface.co/stabilityai/stablelm-tuned-alpha-7b)
- [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b)
- [Neutralzz/BiLLa-7B-SFT](https://huggingface.co/Neutralzz/BiLLa-7B-SFT)

---

## 🎉友情链接🎉

本项目在开发过程中，基础代码来源于 [imClumsyPanda](https://github.com/GanymedeNil) 的项目 [langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM)

-------

### 🎉 LLMflow项目交流

<img title="" src="img/wechat.jpg" alt="二维码" width="230" data-align="left">
