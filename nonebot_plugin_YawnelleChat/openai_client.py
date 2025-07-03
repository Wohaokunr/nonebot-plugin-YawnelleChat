from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from nonebot import logger
from openai import AsyncOpenAI

from .config import plugin_config


@dataclass
class OpenAIClient:
    """Wrapper around :class:`AsyncOpenAI` with lazy initialization."""

    api_key: str | None = None
    api_base: str | None = None
    _client: AsyncOpenAI | None = None

    def __post_init__(self) -> None:
        if self.api_key is None:
            self.api_key = plugin_config.openai_api_key
        if self.api_base is None:
            self.api_base = plugin_config.openai_api_base

    def _ensure_client(self) -> None:
        if self._client is not None:
            return
        if not self.api_key:
            logger.error("OpenAI API key is not configured")
            return
        kwargs: dict[str, Any] = {"api_key": self.api_key}
        if self.api_base:
            kwargs["base_url"] = self.api_base
        try:
            self._client = AsyncOpenAI(**kwargs)
            logger.info("OpenAI async client initialized")
        except Exception as exc:
            logger.error(f"Failed to initialize OpenAI client: {exc}")

    async def chat(self, **kwargs: Any):
        self._ensure_client()
        if not self._client:
            return None
        return await self._client.chat.completions.create(**kwargs)
