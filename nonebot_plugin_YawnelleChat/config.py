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
        default="你是一個智能群聊助手，請嚴格遵守以下規則處理消息：\n1. 必須使用自然語言回覆，禁止返回任何代碼塊或格式標記\n2. 當需要主動發送消息到群聊時，調用send_group_message函數並設置required為true，否則設置required為false\n3. 保持對話簡潔，單次回覆不超過3句話",
        description="AI系统提示词"
    )
    
    # 消息队列配置
    max_history_length: int = Field(default=3, description="群聊历史消息最大保存数量")


# 配置加载
plugin_config: Config = get_plugin_config(Config)
global_config = get_driver().config

# 全局名称
NICKNAME: str = next(iter(global_config.nickname), "")
