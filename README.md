# 自動化網球比賽系統

---

## 簡介

這是一個先進的自動化網球比賽管理系統，旨在實現比賽的**無人化順利進行**。它結合了 AI 圖像辨識技術來自動判讀比賽分數，並智能地管理球場狀態與賽程排程。無論是追蹤比賽進度、自動記錄結果，還是安排下一場賽事，本系統都能高效且精準地運作。

---

## 功能特色

* **智能分數判讀：** 利用 AI（CNN 模型）自動辨識場上比分，並即時更新球場狀態。
* **球場狀態自動管理：** 精準追蹤每個球場的即時狀態，包括「空閒」、「進行中」和「比賽結束」。
* **自動化比賽排程：** 當球場變為空閒時，系統會智能地將預定的選手晉升為當前比賽選手，並為接下來的比賽預排新的選手。
* **比賽結果記錄與分析：** 根據自動判讀的比分，系統自動判斷比賽勝者，並將完整的比賽結果（比分、勝者）保存到主賽程表中。
* **賽程佔位符更新：** 自動將賽程表中如 "Winner of Match X" 的選手佔位符替換為已確定的實際勝者名稱，確保賽程圖的即時性。
* **前端可視化介面：** 提供一個簡單直觀的網頁介面，方便管理員或觀眾查看即時比賽狀態和賽程。

---

## 技術棧

* **程式語言：** Python 3.13 (AI 處理與核心邏輯), Node.js (伺服器與前端管理)
* **數據儲存：** JSON 檔案 (`courts.json`, `mainDraw.json`)
* **AI 模型：** CNN (卷積神經網絡)
* **訓練數據集：** The Street View House Numbers (SVHN) Dataset

---

## 檔案結構
```
├── recognize_score.py      # 負責使用 CNN 模型辨識分數並更新 courts.json
├── schedule_manager.py     # 負責處理比賽排程、晉升選手等邏輯
├── inital.py               # 用於初始化或重置 courts.json 和 mainDraw.json 到預設狀態
├── courts.json             # 儲存各球場的即時狀態、分數、當前/下一場比賽資訊
├── mainDraw.json           # 儲存完整的賽程表和比賽結果
├── README.md               # 專案說明文件
├── score_ocr/              # 存放用於分數辨識的圖片，例如 court1 到 court12 的比分圖片
├── SVHN/                   # 包含 AI 模型訓練相關文件
│   ├── model.py            # CNN 模型定義
│   └── svhn_cnn_weights.pth# 預訓練的 SVHN CNN 模型權重
└── public/                 # 存放前端網頁文件
    └── admin.html          # 管理/顯示比賽狀態的前端網頁
└── server.js               # Node.js 伺服器，負責啟動和協調 Python 後端邏輯，並提供 API 服務給前端
```
### 🚀 如何開始

### 前置條件

在運行本專案之前，請確保您的系統已安裝以下軟體：

* **Python 3.13 或更高版本**
    * 您需要安裝在 `requirements.txt` 中列出的所有 Python 套件。
* **Node.js (LTS 版本推薦)**

### 安裝步驟

1.  **下載專案：**
    * 如果您使用 Git，可以克隆本儲存庫：
        ```bash
        git clone [https://github.com/jirong-spec/automated-tennis-system]
        cd [automated-tennis-system]
        ```
    * 如果沒有 Git，您可以直接下載專案的壓縮檔並解壓縮。

2.  **安裝 Python 依賴：**
    * 進入專案根目錄，打開終端機或命令提示字元，執行：
        ```bash
        pip install -r requirements.txt
        ```

3.  **安裝 Node.js 依賴：**
    * **請確保您已安裝 Node.js。**
    * 在相同的專案根目錄下，執行：
        ```bash
        npm install
        ```
    * 這會自動安裝 `express`、`cors` 和 `node-cron` 等 Node.js 服務端和前端管理介面所需的套件。

### 運行專案

您的系統主要由 **Node.js 伺服器**驅動。一旦 `node server.js` 啟動，它將會自動協調所有 Python 後端邏輯的執行（包括 AI 分數辨識和比賽排程）。

1.  **啟動 Node.js 伺服器：**
    * 在專案根目錄下，打開一個終端機或命令提示字元，執行：
        ```bash
        node server.js
        ```
    * 啟動成功後，後端 API 會在 `http://localhost:3000` 提供服務。**此時，您的所有 Python 後端邏輯（包括分數辨識、排程和賽程更新等）都將由 `server.js` 自動觸發並在後台運行。**

2.  **開啟網頁管理介面 (前端)：**
    * 在瀏覽器中打開 `public/admin.html` 檔案即可開始使用管理介面，查看即時比賽狀態和賽程。

---

## 使用說明

本系統透過即時讀取和寫入 `courts.json` 和 `mainDraw.json` 檔案來運作，並由 `recognize_score.py` 自動更新分數，由 `schedule_manager.py` 自動排程。**所有 Python 後端邏輯的執行都將由 Node.js 伺服器 (`server.js`) 負責協調和觸發。**

1.  **初始化系統：**
    * 首次使用或需要重置系統時，您可以手動運行 `inital.py`。
        ```bash
        python inital.py
        ```
    * 這將會自動創建 `courts.json` (包含預設空閒球場) 和 `mainDraw.json` (為空列表或預設賽程)。您可以根據需要修改 `inital.py` 來設定自己的初始化邏輯。

2.  **設定初始賽程：**
    * 手動編輯 `mainDraw.json` 檔案，按照以下格式填寫您的比賽賽程。請確保 `status` 欄位初始為 `"尚未開始"`。
        ```json
        [
          {
            "match": 1,
            "player1": "選手A",
            "player2": "選手B",
            "status": "尚未開始",
            "score_p1": null,
            "score_p2": null,
            "winner": null
          },
          {
            "match": 2,
            "player1": "選手C",
            "player2": "選手D",
            "status": "尚未開始",
            "score_p1": null,
            "score_p2": null,
            "winner": null
          },
          {
            "match": 3,
            "player1": "Winner of Match 1", # 系統會自動替換為實際勝者
            "player2": "Winner of Match 2", # 系統會自動替換為實際勝者
            "status": "尚未開始",
            "score_p1": null,
            "score_p2": null,
            "winner": null
          }
        ]
        ```
    * **注意：** 包含 `"Winner of Match X"` 佔位符的比賽，會在前一場比賽結果確定後自動更新選手名稱。

3.  **系統運作流程 (由 `node server.js` 統一管理)：**
    * 當 `node server.js` 啟動後：
        * **分數辨識 (`recognize_score.py`):** `server.js` 將會觸發 `recognize_score.py` 運行，持續監測並使用 AI 辨識球場上的分數變化 (例如從 `score_ocr/` 目錄讀取圖像)，自動更新 `courts.json` 中對應球場的 `score1` 和 `score2` 欄位，並將球場 `status` 更新為 `"進行中"` 或 `"比賽結束"`。
        * **比賽結果處理與排程 (`schedule_manager.py`):** `server.js` 也會定期或根據事件觸發 `schedule_manager.py` 執行。該腳本會處理已結束的比賽結果（記錄到 `mainDraw.json`，並清空 `courts.json` 中的當前比賽資訊），同時執行排程邏輯，自動晉升選手和預排新的比賽。

4.  **前端顯示 (`public/admin.html`):**
    * 網頁會透過 Node.js 伺服器提供的 API，實時顯示 `courts.json` 和 `mainDraw.json` 中的數據，為管理員和觀眾提供直觀的比賽概覽。
    * **局域網連接：** 若想讓局域網內其他設備能夠連線觀看，請編輯 `public/admin.html` 中的 `API_BASE` 變數。將 `http://192.168.x.x:3000` 改成你的電腦在局域網中的 IPv4 位址（例如：`http://192.168.1.1:3000`），確保同一區域網路內的其他人能正確連線。

---

## 注意事項 ⚠️

* 請確保所有 `.py` 和 `.json` 檔案都位於正確的相對路徑下，符合檔案結構的定義。
* 在手動編輯 `.json` 檔案時，務必確保其是有效的 JSON 格式，否則程式可能會報錯。
* `current_match_number`、`next_match_number` 和 `status` 等關鍵欄位應主要由程式自動管理，除非您非常清楚其影響，否則不建議手動修改。
* AI 分數辨識的準確性取決於模型訓練效果和影像品質。

---

## 未來潛在功能

* **更完善的 AI 模型：** 引入更先進的深度學習模型，提升分數辨識的準確性和魯棒性，以應對各種光照、角度和字體。
* **開發一套專門控制相機（例如透過特定 API 或 SDK）的程式碼**，使其能夠直接獲取實時影像串流，而非僅從預存的圖片文件讀取。這將實現更為即時和自動化的分數更新流程。
* **多語言支持：** 為前端介面和系統提示提供多語言選項。
* **更豐富的前端介面：** 增加更多的統計數據、歷史記錄查詢、賽程圖可視化等功能。

---

## 貢獻

如果您對此專案感興趣並希望貢獻，請隨時提出 Pull Request 或提交 Issue。我們歡迎任何形式的貢獻！

---

## 許可證

本專案採用 **MIT License** 授權。詳情請參閱專案根目錄下的 `LICENSE` 檔案。
