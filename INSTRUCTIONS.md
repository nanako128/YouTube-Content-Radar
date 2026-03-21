# YouTube Content Radar 操作指南

本文件說明如何啟動後端系統、執行爬蟲任務以及生成排行榜。

---

## 0. 前置作業
確保你的 **Docker Desktop** 已經啟動，並且你已經進入專案根目錄。

---

## 1. 啟動後端系統 (Infrastructure & API)

### 第一步：啟動資料庫與 Redis
這會啟動 Docker 中的 PostgreSQL 和 Redis 服務。
```bash
cd "ai_content_radar"
docker compose up -d
```

### 第二步：啟動 API 伺服器
打開一個新的終端機視窗，執行以下指令並**保持開啟**。
```bash
cd "ai_content_radar"
./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*   **API 健康檢查**：訪問 [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
*   **前端網頁**：訪問 [http://localhost:3000](http://localhost:3000)

---

## 2. 執行每日爬蟲與排名更新

當你想抓取最新資料或更新排行榜時，請依序執行以下指令：

### 第一步：加入/同步追蹤頻道 (選配)
如果你修改了 `seed_channels.py` 裡的名單，請執行此指令同步到資料庫。
```bash
cd "ai_content_radar"
./.venv/bin/python seed_channels.py
```

### 第二步：執行 YouTube 影片抓取
這會從 YouTube API 抓取最近 30 天的影片與留言。
```bash
cd "ai_content_radar"
./.venv/bin/python run_crawl.py
```

### 第三步：生成/更新今日排行榜 (重要)
抓完資料後，必須執行此指令，網頁上的排行榜才會更新。
```bash
cd "ai_content_radar"
export PYTHONPATH=$PYTHONPATH:.
./.venv/bin/python -m app.tasks.ranking_tasks
```

---

## 3. 常見問題排除

*   **連不到 API**：請檢查 `uvicorn` 是否正在運行（步驟 1.2）。
*   **網頁沒資料**：請確保執行了「更新今日排行榜」（步驟 2.3）。
*   **資料庫報錯**：請確保 Docker 容器正在運行（步驟 1.1）。
*   **缺少套件**：若提示找不到 `celery` 或 `greenlet`，請執行：
    ```bash
    ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/pip install "celery[redis]" greenlet
    ```
