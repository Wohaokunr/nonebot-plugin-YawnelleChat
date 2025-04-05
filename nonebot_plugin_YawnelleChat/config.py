from nonebot import get_driver, get_plugin_config
from pydantic import BaseModel, Field
from typing import Optional


class Config(BaseModel):
    # OpenAI API配置
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API密钥")
    openai_api_base: Optional[str] = Field(default=None, description="OpenAI API基础URL，可选")
    openai_model: str = Field(default="gpt-3.5-turbo", description="OpenAI模型名称")
    
    # 系统提示词配置
    system_prompt: str = Field(
        default="你是一个友好的AI助手，正在参与群聊对话。请根据上下文提供有帮助的回复。",
        description="AI系统提示词"
    )
    
    # 消息队列配置
    max_history_length: int = Field(default=30, description="群聊历史消息最大保存数量")


# 配置加载
plugin_config: Config = get_plugin_config(Config)
global_config = get_driver().config

# 全局名称
NICKNAME: str = next(iter(global_config.nickname), "")
