const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const { execFile } = require('child_process');
const http = require('http'); // 用於發送內部請求

const app = express();
app.use(cors());
app.use(express.json());

const DATA_FILE = path.join(__dirname, 'courts.json');

// 初始預設球場資料（共 12 球場）
function getInitialCourts() {
  return Array.from({ length: 12 }, (_, index) => ({
    id: `Court ${index + 1}`,
    player1: "", score1: null,
    player2: "", score2: null,
    nextPlayers: "",
    status: "尚未開始"
  }));
}

// 讀取球場資料
function readData() {
  try {
    const raw = fs.readFileSync(DATA_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch (e) {
    console.error(`[ERROR] 讀取或解析 courts.json 失敗 (${e.message})，將初始化預設球場資料。`);
    const init = getInitialCourts();
    saveData(init);
    return init;
  }
}

// 儲存球場資料
function saveData(data) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

// 提供靜態資源（如 admin.html, viewer.html）
app.use(express.static(path.join(__dirname, 'public')));

// GET 所有球場資料
app.get('/courts', (req, res) => {
  res.json(readData());
});

// AI 辨識比分功能路由
app.post('/update-score/all', (req, res) => {
  console.log(`[INFO] 呼叫 AI 比分識別中...`);

  execFile('python', ['recognize_score.py', 'all'], {
    cwd: __dirname, // 確保工作目錄正確
    encoding: 'utf8',
  }, (error, stdout, stderr) => {
    if (error) {
      console.error(`[ERROR] AI 比分識別腳本執行失敗 (execFile error):`);
      console.error(`    錯誤代碼: ${error.code}`);
      console.error(`    訊號: ${error.signal}`);
      console.error(`    訊息: ${error.message}`);
      console.error(`    Python STDERR:\n${stderr}`);
      return res.status(500).json({ error: 'AI 辨識腳本啟動或執行失敗', details: error.message });
    }

    if (stdout) {
      console.log('[INFO] Python STDOUT:\n', stdout);
    }
    if (stderr) {
      console.log('[INFO] Python STDERR (from script):\n', stderr);
    }

    res.json({ message: '[OK] AI 比分辨識已觸發並完成背景更新。' });
  });
});

// POST 排程下一場選手（呼叫 Python）
app.post('/assign-next', (req, res) => {
  console.log(`[INFO] 呼叫自動排程功能中...`); // 新增日誌
  execFile('python', ['schedule_manager.py'], {
    cwd: __dirname,
    encoding: 'utf8',
  }, (error, stdout, stderr) => {
    if (error) {
      console.error(`[ERROR] 排程腳本執行失敗 (execFile error):`); // 修正日誌
      console.error(`    錯誤代碼: ${error.code}`);
      console.error(`    訊號: ${error.signal}`);
      console.error(`    訊息: ${error.message}`);
      console.error(`    Python STDERR:\n${stderr}`); // 修正日誌
      return res.status(500).json({ error: '排程失敗', details: error.message }); // 修正錯誤訊息
    }
    if (stdout) {
      console.log('[INFO] Schedule Manager STDOUT:\n', stdout);
    }
    if (stderr) {
      console.log('[INFO] Schedule Manager STDERR:\n', stderr);
    }
    res.json({ message: '[OK] 下一場選手已分配完成' });
  });
});

// 預設首頁：顯示 viewer.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/viewer.html'));
});

// 管理介面 admin.html
app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/admin.html'));
});


// 自動觸發排程的函數
function triggerScheduleUpdate() {
  console.log(`[INFO] 觸發自動排程...`);
  const options = {
    hostname: 'localhost',
    port: PORT,
    path: '/assign-next',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  };

  const req = http.request(options, (res) => {
    console.log(`[INFO] 自動排程回應狀態碼: ${res.statusCode}`);
    res.on('end', () => { console.log('[INFO] 自動排程請求已完成。'); });
  });
  req.on('error', (e) => { console.error(`[ERROR] 自動排程請求失敗: ${e.message}`); });
  req.end();
}


// 自動觸發 AI 比分識別的函數
function triggerAiScoreUpdate() {
  console.log(`[INFO] 觸發 AI 比分識別...`);
  const options = {
    hostname: 'localhost',
    port: PORT,
    path: '/update-score/all',
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  };

  const req = http.request(options, (res) => {
    console.log(`[INFO] AI 比分識別回應狀態碼: ${res.statusCode}`);
    res.on('end', () => { console.log('[INFO] AI 比分識別請求已完成。'); });
  });
  req.on('error', (e) => { console.error(`[ERROR] AI 比分識別請求失敗: ${e.message}`); });
  req.end();
}




// 啟動伺服器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`[OK] Server running at http://localhost:${PORT}`);
  
  // 伺服器啟動後立即觸發一次所有自動化任務
  console.log('[INFO] 伺服器已啟動，立即觸發所有自動化功能...');
  triggerAiScoreUpdate();
  triggerScheduleUpdate();

  // 然後每 10 秒觸發一次 AI 比分識別
  setInterval(triggerAiScoreUpdate, 10000); 
  console.log(`[INFO] 已設定 AI 比分識別功能每 10 秒自動更新。`);

  // 然後每 10 秒觸發一次自動排程
  setInterval(triggerScheduleUpdate, 10000); 
  console.log(`[INFO] 已設定自動排程功能每 10 秒自動更新。`);
});