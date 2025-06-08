"""主程式"""

import os
import shutil

import uvicorn
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger as log

from source.config import GlobalConfig
from source.system.service import change_native_log_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """生命週期"""
    try:
        change_native_log_settings()

        log.info(
            (
                f"專案啟動成功, 專案名稱:{GlobalConfig.project_name()}, "
                f"埠號:{GlobalConfig.uvicorn_port()}, "
                f"環境:{"生產" if GlobalConfig.is_production() else "開發"}"
            )
        )

        yield
    except Exception as error:  # pylint: disable=W0718
        log.error(f"專案啟動失敗: {error}")
    finally:
        for root, dirs, __ in os.walk("."):
            for dir_name in dirs:
                if dir_name in {"__pycache__", ".pytest_cache"}:
                    shutil.rmtree(os.path.join(root, dir_name))

        log.warning("專案結束")


app = FastAPI(
    lifespan=lifespan,
    openapi_url=None if GlobalConfig.is_production() else "/openapi.json",
    docs_url=None if GlobalConfig.is_production() else "/docs",
    redoc_url=None if GlobalConfig.is_production() else "/redoc",
    title="backend sample fastapi python API",
    version="0.0.1",
    description="將會使用 FastAPI 後端框架來練習開發後端功能，包含 API、Websocket、UDP、TCP等相關功能。",
    servers=[
        {"url": f"http://{GlobalConfig.uvicorn_host()}:{GlobalConfig.uvicorn_port()}"}
    ],
    openapi_tags=[],
)

# NOTE: 添加中介層順序，會影響執行的順序，需注意
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app if GlobalConfig.is_production() else "source.main:app",
        host=GlobalConfig.uvicorn_host(),
        port=GlobalConfig.uvicorn_port(),
        proxy_headers=True,
        reload=GlobalConfig.is_uvicorn_reload(),
        log_level="error" if GlobalConfig.is_production() else "debug",
    )
