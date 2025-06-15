"""
WebSocket 客戶端斷開連線
"""

from fastapi import WebSocket
from loguru import logger as log
from pydantic import StrictInt, StrictStr

from source.config import GlobalConfig
from source.core.schema import WebSocketConnection


def client_disconnect(
    *, websocket: WebSocket, code: StrictInt, reason: StrictStr
) -> None:
    """
    客戶端斷開連線

    Args:
        websocket: WebSocket 連線
        code: 斷開連線代碼
        reason: 斷開連線原因

    Returns:
        None
    """
    disconnect_connection: WebSocketConnection | None = None

    for connection in GlobalConfig.websocket_connection_list():
        if connection.websocket == websocket:
            disconnect_connection = connection
            break

    if disconnect_connection is not None:
        log.warning(
            f"索引: {id(disconnect_connection.websocket)} "
            "斷開 WebSocket 連線, "
            f"代碼: {code}, 原因: {reason}"
        )
        GlobalConfig.remove_websocket_connection(disconnect_connection)
