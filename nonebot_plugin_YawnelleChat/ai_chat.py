from __future__ import annotations

import json

from nonebot import logger

from .config import plugin_config
from .group_config_manager import group_config_manager
from .message_queue import Message
from .openai_client import OpenAIClient


class AIChatHandler:
    """AI聊天处理类，负责与OpenAI API交互"""

    def __init__(self) -> None:
        self._client = OpenAIClient()

    def _build_messages(self, history: list[Message], system_prompt: str) -> list[dict[str, str]]:
        """构建OpenAI API所需的消息格式

        Args:
            history: 历史消息列表

        Returns:
            OpenAI API所需的消息列表
        """
        # 添加系统提示词
        messages = [{"role": "system", "content": system_prompt}]

        # 如果历史消息为空，返回带有默认用户消息的列表
        if not history:
            messages.append({"role": "user", "content": "你好"})
            return messages

        # 添加历史消息
        has_user_message = False
        for item in history:
            sender, content = item.sender, item.content
            if sender != "AI":
                has_user_message = True
                # 添加用户名称到消息内容
                messages.append(
                    {
                        "role": "user",
                        "content": f"<UserName>{sender}</UserName>: <Content>{content}</Content>",
                    }
                )
            # AI自己的回复
            else:
                messages.append({"role": "assistant", "content": content})

        # 如果没有用户消息，添加一个默认的用户消息
        if not has_user_message:
            messages.append({"role": "user", "content": "你好"})
        # 如果最后一条消息是AI回复，添加一个用户消息以继续对话
        elif messages[-1]["role"] == "assistant":
            messages.append({"role": "user", "content": "请继续"})

        return messages

    async def get_ai_response(self, history: list[Message], group_id: str) -> str | None:
        """获取AI回复

        Args:
            history: 历史消息列表

        Returns:
            AI回复内容，如果出错则返回None
        """
        response = None

        try:
            system_prompt = group_config_manager.get(group_id, "system_prompt", plugin_config.system_prompt)
            model = group_config_manager.get(group_id, "openai_model", plugin_config.openai_model)
            messages = self._build_messages(history, system_prompt)

            # 调用OpenAI API
            response = await self._client.chat(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "send_group_message",
                            "description": "当需要主动发送消息到群聊时调用此函数",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "required": {
                                        "type": "boolean",
                                        "description": "是否必须发送此消息，true表示需要立即发送，false表示不需要发送",
                                    },
                                    "message_content": {"type": "string", "description": "要发送的消息内容"},
                                },
                                "required": ["required", "message_content"],
                            },
                        },
                    }
                ],
                tool_choice="auto",
            )

            logger.debug(f"OpenAI API响应: {response}")

            message = response.choices[0].message

            if not getattr(message, "tool_calls", None):
                _ = message.content
            logger.info(f"检测到工具调用: {message.tool_calls}")
            if not getattr(message, "tool_calls", None):
                return None
            tool_call = message.tool_calls[0]

            if tool_call.type != "function" or tool_call.function.name != "send_group_message":
                logger.warning(f"未知的工具调用: {tool_call.type} - {tool_call.function.name}")
                return None

            try:
                # 解析并验证函数参数
                function_args = json.loads(tool_call.function.arguments)
                required = function_args.get("required", False)
                message_content = function_args.get("message_content", "").strip()

                # 参数验证
                if not isinstance(required, bool):
                    required = str(required).lower() in ["true", "1", "yes", "y"]

                # 如果required为false或消息内容为空，返回None
                if not required or not message_content:
                    return None

                return message_content

            except Exception as e:
                logger.error(f"处理工具调用失败: {e}")
                return None

            # 处理普通回复并过滤格式
            # reply = response.choices[0].message.content
            # # 移除代码块和特殊符号
            # reply = reply.replace('```', '').replace('`', '').strip()
            # return reply if reply else None
        except Exception as e:
            logger.error(f"获取AI回复失败: {e}")
            return f"AI回复出错: {e!s}"


# 全局AI聊天处理实例
ai_chat_handler = AIChatHandler()
