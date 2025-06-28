import json
from pathlib import Path
from typing import Any

from nonebot import logger


class GroupConfigManager:
    def __init__(self) -> None:
        self._file = Path("group_config.json")
        self._configs: dict[str, dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        if not self._file.exists():
            return
        try:
            self._configs = json.loads(self._file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.error(f"加载群配置失败: {e}")

    def _save(self) -> None:
        try:
            self._file.write_text(json.dumps(self._configs, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.error(f"保存群配置失败: {e}")

    def set(self, group_id: str, key: str, value: Any) -> None:
        cfg = self._configs.setdefault(group_id, {})
        cfg[key] = value
        self._save()

    def get(self, group_id: str, key: str, default: Any = None) -> Any:
        cfg = self._configs.get(group_id, {})
        return cfg.get(key, default)


# 全局实例
group_config_manager = GroupConfigManager()
