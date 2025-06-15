"""WebSocket 連線初始化"""

from fastapi import WebSocket
from loguru import logger as log

from source.config import GlobalConfig
from source.core.schema import WebSocketConnection, WebSocketConnectionUser


def init_connect(*, websocket: WebSocket) -> WebSocketConnection:
    """
    初始化 WebSocket 連線

    Args:
        websocket: WebSocket 連線

    Returns:
        WebSocketConnection: WebSocket 連線
    """
    websocket_connection = WebSocketConnection(
        websocket=websocket,
        user=WebSocketConnectionUser(
            id=0,
            account="",
            name="",
        ),
        last_heartbeat=GlobalConfig.datetime_now(),
    )

    GlobalConfig.add_websocket_connection(websocket_connection)

    log.info(
        f"WebSocket 連線, 索引: {id(websocket_connection.websocket)}, "
        f"IP: {websocket_connection.websocket.headers.get('x-forwarded-for', '0.0.0.0')}"
    )

    return websocket_connection
