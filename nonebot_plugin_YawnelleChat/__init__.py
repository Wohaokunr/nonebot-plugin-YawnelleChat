from __future__ import annotations

from nonebot import get_driver, logger, on_command, on_message
from nonebot.adapters import Bot, Event
from nonebot.adapters.onebot.v11 import GROUP, Message
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

from .ai_chat import ai_chat_handler
from .config import Config
from .group_config_manager import group_config_manager
from .message_queue import message_queue

__all__ = ["ai_chat_handler", "ai_reply", "chat", "chat_config", "pip"]

__plugin_meta__ = PluginMetadata(
    name="YawnelleChat",
    description="适用于多人群聊的ai聊天插件",
    usage="用法",
    type="application",
    homepage="https://github.com/Wohaokunr/nonebot-plugin-YawnelleChat",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra={"author": "Wohaokunr <Wohaokunr@gmail.com>"},
)


# 简单的演示命令，供测试使用
pip = on_message(rule=lambda event: event.get_plaintext().startswith("pip"), permission=GROUP, priority=5)


@pip.handle()
async def _(event: Event):
    if "nonebot2" in event.get_plaintext():
        await pip.finish(Message("nonebot2"))
    await pip.finish()


# 定义命令处理器
chat = on_message(rule=lambda event: event.get_plaintext().startswith("/chat"), permission=GROUP, priority=10)
chat_config = on_command("chat_config", permission=GROUP, priority=10)

# 定义消息处理器，响应所有群消息
ai_reply = on_message(permission=GROUP, priority=10)

driver = get_driver()
scheduler = getattr(driver, "scheduler", None)

if scheduler:

    @scheduler.scheduled_job("cron", hour=9, minute=0)
    async def _morning_push():
        for bot in driver.bots.values():
            for gid in message_queue.get_groups():
                try:
                    await bot.send_group_msg(group_id=int(gid), message="早上好~")
                except Exception as e:
                    logger.error(f"主动推送失败: {e}")


@chat_config.handle()
async def handle_chat_config(bot: Bot, event: Event, state: T_State):
    group_id = getattr(event, "group_id", None)
    if not group_id:
        await chat_config.finish("此命令只能在群聊中使用")

    args = str(event.get_message()).strip().split(None, 1)
    if len(args) < 2:
        await chat_config.finish("用法: /chat_config <model|prompt> <值>")
    key, value = args[0], args[1]

    if key == "model":
        group_config_manager.set(str(group_id), "openai_model", value)
        await chat_config.finish(f"已设置模型为 {value}")
    elif key == "prompt":
        group_config_manager.set(str(group_id), "system_prompt", value)
        await chat_config.finish("已更新系统提示词")
    else:
        await chat_config.finish("未知配置项")


@chat.handle()
async def handle_chat(bot: Bot, event: Event, state: T_State):
    # 获取群聊ID
    group_id = getattr(event, "group_id", None)
    if not group_id:
        await chat.finish("此命令只能在群聊中使用")

    # 获取消息内容
    msg = str(event.get_message()).strip()

    # 清空历史记录
    if msg == "/chat -c" or msg == "/chat --clear":
        message_queue.clear_history(str(group_id))
        await chat.finish(Message("已清空当前群聊的消息历史"))

    # 显示帮助信息
    await chat.finish(Message("使用方法：\n- @机器人 [消息]：与AI对话\n- /chat -c：清空当前群聊的消息历史"))

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
    sender_name = user_info.get("user_name", f"用户{user_id}")  # 使用字典键访问

    # 添加消息到队列
    message_queue.add_message(str(group_id), sender_name, str(msg))


async def get_user_info(bot: Bot, event: Event) -> dict:
    """
    获取用户信息
    :param bot: Bot 对象
    :param event: Event 对象
    :return: 用户信息字典
    """
    user_id = getattr(event, "user_id", None)
    group_id = getattr(event, "group_id", None)

    if not user_id:
        return {"user_name": "未知用户"}

    try:
        if group_id:  # 如果是群聊消息
            user_info = await bot.call_api("get_group_member_info", group_id=group_id, user_id=user_id)
            return {"user_name": user_info.get("card") or user_info.get("nickname", "未知用户")}
        else:  # 如果是私聊消息
            user_info = await bot.call_api("get_stranger_info", user_id=user_id)
            return {"user_name": user_info.get("nickname", "未知用户")}
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        return {"user_name": f"用户{user_id}"}


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

    # 获取用户信息
    user_info = await get_user_info(bot, event)
    sender_name = user_info.get("user_name", f"用户{getattr(event, 'user_id', 'unknown')}")

    #     # 添加防循环机制
    # if sender_name == "AI":
    #     return

    # 添加用户消息到队列（保留原始消息内容）
    message_queue.add_message(str(group_id), sender_name, str(msg))

    # 获取历史消息
    history = message_queue.get_history(str(group_id))

    # 获取AI回复
    reply = await ai_chat_handler.get_ai_response(history, str(group_id))

    # 如果返回None，表示AI决定不需要回复
    if reply is None:
        return

    # 检查回复是否为错误信息
    if reply.startswith("AI回复出错"):
        await ai_reply.finish(Message(reply))

    # 将有效的AI回复添加到消息队列并发送
    message_queue.add_message(str(group_id), "AI", reply)
    await ai_reply.finish(Message(reply))
