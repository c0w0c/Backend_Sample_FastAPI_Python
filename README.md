# Backend_Sample_FastAPI_Python

將會使用 FastAPI 後端框架來練習開發後端功能，包含 API、Websocket、UDP、TCP等相關功能。

## 環境

- pyenv 2.6.0
- python 3.12.4

## 執行

專案下載

```bash
git clone https://github.com/c0w0c/Backend_Sample_FastAPI_Python.git

cd Backend_Sample_FastAPI_Python

python -m venv venv

source venv/bin/activate

pip install -r requirements/dev.txt
```

使用 8000 port 啟動服務

```bash
python -m source.main
```

程式碼風格檢查

```bash
tool/lint.sh
```