"""Фильтры и утилиты для логирования.

Отдельный модуль, чтобы не тянуть main.py с его зависимостями
(loader, telegram bot, .env) в тесты и вспомогательные скрипты.
"""
import logging
import re

TOKEN_RE = re.compile(r"bot\d+:[A-Za-z0-9_-]+")


class MaskTokenFilter(logging.Filter):
    """Маскирует bot<TOKEN> в логах."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = TOKEN_RE.sub("bot<TOKEN>", record.msg)
        if record.args:
            if isinstance(record.args, tuple):
                record.args = tuple(
                    TOKEN_RE.sub("bot<TOKEN>", a) if isinstance(a, str) else a
                    for a in record.args
                )
            elif isinstance(record.args, dict):
                record.args = {
                    k: (TOKEN_RE.sub("bot<TOKEN>", v) if isinstance(v, str) else v)
                    for k, v in record.args.items()
                }
        return True
