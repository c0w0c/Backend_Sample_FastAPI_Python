"""全域相關的設定值"""

import os
from collections import deque
from datetime import datetime
from threading import Lock

import pytz

from source.core.schema.websocket import WebSocketConnection


class GlobalConfig:
    """全域設定"""

    _timezone: str = "Asia/Taipei"
    _websocket_lock = Lock()
    _websocket_connection_list: deque[WebSocketConnection] = deque()

    @classmethod
    def project_name(cls) -> str:
        """專案名稱"""
        return "backend_sample_fastapi_python"

    @classmethod
    def is_production(cls) -> bool:
        """是否為生產環境"""
        return bool(os.getenv("IS_PRODUCTION", "False").lower() == "true")

    @classmethod
    def is_use_production_path(cls) -> bool:
        """是否使用生產環境路徑"""
        return bool(os.getenv("IS_USE_PRODUCTION_PATH", "False").lower() == "true")

    @classmethod
    def uvicorn_host(cls) -> str:
        """uvicorn 伺服器主機"""
        return "0.0.0.0" if cls.is_production() else "127.0.0.1"

    @classmethod
    def uvicorn_port(cls) -> int:
        """uvicorn 伺服器埠號"""
        return 8000

    @classmethod
    def is_uvicorn_reload(cls) -> bool:
        """uvicorn 伺服器是否自動重新載入"""
        return not cls.is_production()

    @classmethod
    def timezone(cls) -> str:
        """時區"""
        return cls._timezone

    @classmethod
    def set_timezone(cls, new_timezone: str) -> None:
        """設定時區"""
        cls._timezone = new_timezone

    @classmethod
    def datetime_now(cls) -> datetime:
        """帶有時區的現在時間"""
        return datetime.now(tz=pytz.timezone(cls._timezone))

    @classmethod
    def websocket_connection_list(cls) -> list[WebSocketConnection]:
        """WebSocket 連線列表"""
        with cls._websocket_lock:
            return list(cls._websocket_connection_list)

    @classmethod
    def add_websocket_connection(
        cls, websocket_connection: WebSocketConnection
    ) -> None:
        """新增 WebSocket 連線"""
        with cls._websocket_lock:
            cls._websocket_connection_list.append(websocket_connection)

    @classmethod
    def remove_websocket_connection(
        cls, websocket_connection: WebSocketConnection
    ) -> None:
        """移除 WebSocket 連線"""
        with cls._websocket_lock:
            if websocket_connection in cls._websocket_connection_list:
                cls._websocket_connection_list.remove(websocket_connection)
