from collections import deque
import json
from pathlib import Path

from nonebot import logger

from .config import plugin_config

# 消息类型定义
Message = tuple[str, str]  # (发送者, 消息内容)

class GroupMessageQueue:
    """群聊消息队列管理类"""

    def __init__(self):
        # 群组ID -> 消息队列的映射
        self._group_queues: dict[str, deque[Message]] = {}
        self._max_length = plugin_config.max_history_length
        self._history_file = Path(plugin_config.history_file)
        self._load_history()

    def _load_history(self) -> None:
        if not self._history_file.exists():
            return
        try:
            data = json.loads(self._history_file.read_text(encoding="utf-8"))
            for gid, msgs in data.items():
                dq = deque(maxlen=self._max_length)
                for sender, content in msgs:
                    dq.append((sender, content))
                self._group_queues[gid] = dq
        except Exception as e:
            logger.error(f"加载历史记录失败: {e}")

    def _save_history(self) -> None:
        try:
            data = {
                gid: list(queue)
                for gid, queue in self._group_queues.items()
            }
            self._history_file.write_text(
                json.dumps(data, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as e:
            logger.error(f"保存历史记录失败: {e}")

    def add_message(self, group_id: str, sender: str, content: str) -> None:
        """添加消息到指定群聊的消息队列

        Args:
            group_id: 群聊ID
            sender: 发送者名称或ID
            content: 消息内容
        """
        if group_id not in self._group_queues:
            self._group_queues[group_id] = deque(maxlen=self._max_length)

        self._group_queues[group_id].append((sender, content))
        logger.debug(f"Added message to group {group_id}: {sender}: {content}")
        self._save_history()

    def get_history(self, group_id: str) -> list[Message]:
        """获取指定群聊的历史消息

        Args:
            group_id: 群聊ID
        Returns:
            历史消息列表，如果群聊不存在则返回空列表
        """
        if group_id not in self._group_queues:
            return []

        return list(self._group_queues[group_id])

    def clear_history(self, group_id: str) -> None:
        """清空指定群聊的历史消息

        Args:
            group_id: 群聊ID
        """
        if group_id in self._group_queues:
            self._group_queues[group_id].clear()
            logger.info(f"Cleared message history for group {group_id}")
            self._save_history()

    def get_groups(self) -> list[str]:
        """返回已有记录的群聊ID列表"""
        return list(self._group_queues.keys())

# 全局消息队列实例
message_queue = GroupMessageQueue()
