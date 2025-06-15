"""核心相關結構-WebSocket"""

from datetime import datetime

from fastapi import WebSocket
from pydantic import BaseModel, Field, StrictInt, StrictStr


class WebSocketConnectionUser(BaseModel):
    """WebSocket 連線用戶資訊"""

    id: StrictInt = Field(..., description="索引")
    account: StrictStr = Field(..., description="帳號")
    name: StrictStr = Field(..., description="名稱")


class WebSocketConnection(BaseModel):
    """WebSocket 連線資訊"""

    model_config = {"arbitrary_types_allowed": True}

    user: WebSocketConnectionUser = Field(..., description="用戶資訊")
    websocket: WebSocket
    last_heartbeat: datetime = Field(..., description="最後心跳時間")
