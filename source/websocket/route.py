"""websocket相關的路由"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger as log

from source.websocket.service import client_disconnect, init_connect

router = APIRouter(tags=["websocket"])


@router.websocket("/")
async def websocket_process(websocket: WebSocket):
    """WebSocket 程序"""
    try:
        await websocket.accept()
        connection = init_connect(websocket=websocket)
        await connection.websocket.send_text("歡迎連線")
        while True:
            raw_data = await connection.websocket.receive_text()
            log.info(f"索引: {id(connection.websocket)} 收到訊息: {raw_data}")
    except WebSocketDisconnect as error:
        client_disconnect(
            websocket=websocket,
            code=error.code,
            reason=error.reason,
        )
    except Exception as error:
        log.error(
            f"索引: {id(websocket)} WebSocket 發生未知錯誤, "
            f"{type(error).__name__}: {error}"
        )
    finally:
        try:
            await websocket.close()
        except Exception:
            pass
