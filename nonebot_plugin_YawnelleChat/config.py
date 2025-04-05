from nonebot import get_driver, get_plugin_config
from pydantic import BaseModel, Field
from typing import Optional


class Config(BaseModel):
    # OpenAI API配置
    openai_api_key: Optional[str] = Field(default='none', description="OpenAI API密钥")
    openai_api_base: Optional[str] = Field(default='https://dashscope.aliyuncs.com/compatible-mode/v1', description="OpenAI API基础URL，可选")
    openai_model: str = Field(default="qwen2.5-vl-32b-instruct", description="OpenAI模型名称")
    
    # 系统提示词配置
    system_prompt: str = Field(
        default="你是一个智能群聊助手，请严格遵守以下规则处理消息：\n1. 必须使用自然语言回复，禁止返回任何代码块或格式标记\n2. 当且仅当不需要主动发送消息时调用send_group_message函数，设置required为false\n4. 保持对话简洁，单次回复不超过3句话",
        description="AI系统提示词"
    )
    
    # 消息队列配置
    max_history_length: int = Field(default=3, description="群聊历史消息最大保存数量")


# 配置加载
plugin_config: Config = get_plugin_config(Config)
global_config = get_driver().config

# 全局名称
NICKNAME: str = next(iter(global_config.nickname), "")
