"""
系統相關的服務 - 變更日誌原生設定
"""

import logging
import os
import sys
import traceback
from typing import Any

from loguru import logger as log
from loguru._defaults import env  # type: ignore

from source.config import GlobalConfig


def change_native_log_settings() -> None:
    """變更日誌原生設定"""

    class InterceptHandler(logging.Handler):
        """
        攔截日誌訊息
        """

        def emit(self, record: logging.LogRecord):
            try:
                level = log.level(record.levelname).name
            except ValueError:
                level = record.levelno

            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:  # type: ignore
                frame = frame.f_back  # type: ignore
                depth += 1

            log.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    def format_record(record: dict[str, str | int | None]) -> str:
        """格式化 log 訊息"""

        format_string: Any = env(
            "LOGURU_FORMAT",
            str,
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS Z}</green> | "
            "<level>{level: <8}</level> | ",
        )

        # 處理檔案位置及行號
        _, _, n3 = sys.exc_info()
        if len(traceback.extract_tb(n3)) > 0:
            last_call_stack = traceback.extract_tb(n3)[0]
            last_call_file_path = os.path.abspath(last_call_stack.filename)
            line_number = last_call_stack.lineno
            function_name = last_call_stack.name
            file_path = os.path.relpath(last_call_file_path, os.getcwd())
            format_string += (
                f"<cyan>{file_path.removeprefix("source/")}</cyan>:<cyan>{line_number}</cyan> | "
                f"<cyan>{function_name}</cyan> - "
                "<level><normal>{message}</normal></level>\n"
            )
        else:
            record_file_set: Any = record.get("file")
            if record_file_set:
                if hasattr(record_file_set, "path"):
                    file_path = os.path.relpath(record_file_set.path, os.getcwd())
                    format_string += (
                        f"<cyan>{file_path.removeprefix("source/")}</cyan>"
                        ":<cyan>{line}</cyan> | "
                        "<cyan>{function}</cyan> - <level><normal>{message}</normal></level>\n"
                    )
            else:
                format_string += (
                    "<cyan>{name}</cyan>:<cyan>{line}</cyan> - "
                    "<cyan>{function}</cyan> - <level><normal>{message}</normal></level>\n"
                )

        return format_string

    # pylint: disable=E1101
    loggers = (logging.getLogger(name) for name in logging.root.manager.loggerDict)

    # 將其他控制 logging 的設定改成相同格式，並將他們層級提升到 ERROR 才產生紀錄
    intercept_handler = InterceptHandler()
    for logger_set in loggers:
        logger_set.handlers = [intercept_handler]
        logger_set.setLevel(logging.ERROR)

    log.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": logging.DEBUG,
                "format": format_record,
                "filter": lambda record: record["level"].no < 40,  # type: ignore
                "colorize": True,
            },
            {
                "sink": sys.stderr,
                "level": logging.ERROR,
                "format": format_record,
                "colorize": True,
            },
            {
                "sink": (
                    "/app/log/main.log"
                    if GlobalConfig.is_production()
                    else "./log/main.log"
                ),
                "level": logging.DEBUG,
                "format": format_record,
                "rotation": ("00:00" if GlobalConfig.is_production() else "1 MB"),
                "retention": ("10 days" if GlobalConfig.is_production() else 1),
                "colorize": True,
            },
        ]
    )
