from nonebot import logger, require, on_message
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.adapters import Event, Bot
from nonebot.typing import T_State
from nonebot.permission import GROUP
from nonebot.rule import to_me
from openai import (OpenAI)


require("nonebot_plugin_waiter")
require("nonebot_plugin_uninfo")
require("nonebot_plugin_alconna")
require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")
from .config import Config
from .message_queue import message_queue
from .ai_chat import ai_chat_handler

__plugin_meta__ = PluginMetadata(
    name="YawnelleChat",
    description="适用于多人群聊的ai聊天插件",
    usage="用法",
    type="application",  # library
    homepage="https://github.com/Wohaokunr/nonebot-plugin-YawnelleChat",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna", "nonebot_plugin_uninfo"),
    # supported_adapters={"~onebot.v11"}, # 仅 onebot 应取消注释
    extra={"author": "Wohaokunr <Wohaokunr@gmail.com>"},
)

from arclet.alconna import Alconna, Args, Arparma, Option, Subcommand
from nonebot_plugin_alconna import on_alconna
from nonebot_plugin_alconna.uniseg import UniMessage
from nonebot_plugin_uninfo import UserInfo

# 定义命令处理器
chat = on_alconna(
    Alconna(
        "chat",
        Option("-c|--clear", help_text="清空当前群聊的消息历史"),
    )
)

# 定义消息处理器，响应@机器人的消息
ai_reply = on_message(rule=to_me(), permission=GROUP, priority=10)

# 定义群聊消息监听器，记录所有群聊消息
group_msg = on_message(permission=GROUP, priority=15)


@chat.handle()
async def handle_chat(bot: Bot, event: Event, state: T_State, result: Arparma):
    # 获取群聊ID
    group_id = getattr(event, "group_id", None)
    if not group_id:
        await chat.finish("此命令只能在群聊中使用")
    
    # 清空历史记录
    if result.find("-c") or result.find("--clear"):
        message_queue.clear_history(str(group_id))
        await chat.finish("已清空当前群聊的消息历史")
    
    # 显示帮助信息
    await chat.finish("使用方法：\n- @机器人 [消息]：与AI对话\n- /chat -c：清空当前群聊的消息历史")


@group_msg.handle()
async def handle_group_message(bot: Bot, event: Event):
    # 获取群聊ID和用户ID
    group_id = getattr(event, "group_id", None)
    user_id = getattr(event, "user_id", None)
    
    if not group_id or not user_id:
        return
    
    # 获取消息内容
    msg = getattr(event, "message", None)
    if not msg:
        return
    
    # 获取用户信息
    user_info = await get_user_info(bot, event)
    sender_name = user_info.user_name or f"用户{user_id}"
    
    # 添加消息到队列
    message_queue.add_message(str(group_id), sender_name, str(msg))


@ai_reply.handle()
async def handle_ai_reply(bot: Bot, event: Event):
    # 获取群聊ID
    group_id = getattr(event, "group_id", None)
    if not group_id:
        return
    
    # 获取消息内容
    msg = getattr(event, "message", None)
    if not msg:
        return
    
    # 获取历史消息
    history = message_queue.get_history(str(group_id))
    
    # 获取AI回复
    reply = await ai_chat_handler.get_ai_response(history)
    
    if reply:
        # 将AI回复添加到消息队列
        message_queue.add_message(str(group_id), "AI", reply)
        # 发送回复
        await ai_reply.finish(UniMessage.text(reply))
    else:
        await ai_reply.finish(UniMessage.text("AI回复出错，请稍后再试"))
