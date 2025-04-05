from typing import List, Dict, Any, Optional
from nonebot import logger
from openai import OpenAI
from .config import plugin_config
from .message_queue import Message

class AIChatHandler:
    """AI聊天处理类，负责与OpenAI API交互"""
    
    def __init__(self):
        # 初始化OpenAI客户端
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """初始化OpenAI客户端"""
        try:
            api_key = plugin_config.openai_api_key
            api_base = plugin_config.openai_api_base
            
            if not api_key:
                logger.error("OpenAI API密钥未配置，AI聊天功能将无法使用")
                return
            
            client_kwargs = {"api_key": api_key}
            if api_base:
                client_kwargs["base_url"] = api_base
                
            self._client = OpenAI(**client_kwargs)
            logger.info("OpenAI客户端初始化成功")
        except Exception as e:
            logger.error(f"OpenAI客户端初始化失败: {e}")
    
    def _build_messages(self, history: List[Message]) -> List[Dict[str, str]]:
        """构建OpenAI API所需的消息格式
        
        Args:
            history: 历史消息列表
            
        Returns:
            OpenAI API所需的消息列表
        """
        # 添加系统提示词
        messages = [
            {"role": "system", "content": plugin_config.system_prompt}
        ]
        
        # 添加历史消息
        for sender, content in history:
            # 用户消息
            if sender != "AI":
                messages.append({"role": "user", "content": f"{sender}: {content}"})
            # AI自己的回复
            else:
                messages.append({"role": "assistant", "content": content})
        
        return messages
    
    async def get_ai_response(self, history: List[Message]) -> Optional[str]:
        """获取AI回复
        
        Args:
            history: 历史消息列表
            
        Returns:
            AI回复内容，如果出错则返回None
        """
        if not self._client:
            self._initialize_client()
            if not self._client:
                return "AI聊天功能未正确配置，请联系管理员设置OpenAI API密钥"
        
        try:
            messages = self._build_messages(history)
            
            # 调用OpenAI API
            response = self._client.chat.completions.create(
                model=plugin_config.openai_model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            
            # 提取回复内容
            reply = response.choices[0].message.content
            return reply
        except Exception as e:
            logger.error(f"获取AI回复失败: {e}")
            return f"AI回复出错: {str(e)}"

# 全局AI聊天处理实例
ai_chat_handler = AIChatHandler()