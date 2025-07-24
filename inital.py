import json
import os

# --- 配置檔案名稱 ---
# 這些變數應該與您在 schedule_manager.py 中使用的檔案名稱一致
DATA_FILE = "courts.json"       # 用於儲存球場狀態和排程資訊
SCHEDULE_FILE = "mainDraw.json" # 用於儲存賽程表和比賽結果 (勝者)

# --- 輔助函數：讀取和寫入 courts.json ---
def load_data():
    """從 courts.json 載入球場數據"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            #print(f"錯誤：{DATA_FILE} 檔案內容無效，將初始化為空列表。")
            return []
    return [] # 如果檔案不存在，返回空列表

def save_data(data):
    """將球場數據存回 courts.json"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"寫入 {DATA_FILE} 檔案時發生錯誤: {e}")

# --- 輔助函數：讀取和寫入 mainDraw.json ---
def load_main_draw_data():
    """從 mainDraw.json 載入賽程數據"""
    if os.path.exists(SCHEDULE_FILE):
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"錯誤：{SCHEDULE_FILE} 檔案內容無效，將初始化為空列表。")
            return []
    return [] # 如果檔案不存在，返回空列表

def save_main_draw_data(main_draw_data):
    """將賽程數據存回 mainDraw.json"""
    try:
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(main_draw_data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"寫入 {SCHEDULE_FILE} 檔案時發生錯誤: {e}")

# --- 輔助函數：初始化 courts.json 為指定狀態 ---
def initialize_courts_data_to_specific_state():
    """
    將 courts.json 初始化為使用者指定的預設狀態。
    這對於測試或重置球場數據非常有用。
    """
    initial_state = [
        {
            "id": "Court 1",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒", # 確保狀態為空閒，以便下一場比賽可以被分配
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 2",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 3",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 4",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 5",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 6",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 7",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 8",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 9",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 10",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 11",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        },
        {
            "id": "Court 12",
            "player1": "",
            "score1": None,
            "player2": "",
            "score2": None,
            "nextPlayers": "",
            "status": "空閒",
            "next_match_number": None,
            "current_match_number": None
        }
    ]
    save_data(initial_state)
    print("courts.json 已初始化為指定的預設狀態。")

# --- 輔助函數：初始化 mainDraw.json 為指定狀態 ---
def initialize_main_draw_to_specific_state():
    """
    將 mainDraw.json 初始化為使用者指定的預設賽程狀態。
    這對於測試或重置比賽數據非常有用。
    """
    initial_main_draw = [
      {
        "round": 1,
        "match": 1,
        "player1": "Roger Federer",
        "player2": "Andy Roddick",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始" # 確保每個比賽都有 status 字段
      },
      {
        "round": 1,
        "match": 2,
        "player1": "Jo-W Tsonga",
        "player2": "David Ferrer",
        "winner": None, # 這裡即使分數寫了，也讓程式去判斷勝者，所以保持 None
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 3,
        "player1": "Stan Wawrinka",
        "player2": "Dominic Thiem",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 4,
        "player1": "Marin Cilic",
        "player2": "Richard Gasquet",
        "winner": None, # 保持 None，讓程式判斷
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 5,
        "player1": "Novak Djokovic",
        "player2": "Fernando Verdasco",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 6,
        "player1": "Tomas Berdych",
        "player2": "John Isner",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 7,
        "player1": "Andy Murray",
        "player2": "Kevin Anderson",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 8,
        "player1": "Grigor Dimitrov",
        "player2": "Jack Sock",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 9,
        "player1": "Rafael Nadal",
        "player2": "Fabio Fognini",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 10,
        "player1": "Denis Shapovalov",
        "player2": "Taylor Fritz",
        "winner": None, # 保持 None，讓程式判斷
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 11,
        "player1": "Alexander Zverev",
        "player2": "Alex de Minaur",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 12,
        "player1": "Diego Schwartzman",
        "player2": "Pablo Carreno Busta",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 13,
        "player1": "Jannik Sinner",
        "player2": "Gael Monfils",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 14,
        "player1": "Casper Ruud",
        "player2": "Karen Khachanov",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 15,
        "player1": "Holger Rune",
        "player2": "Frances Tiafoe",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 1,
        "match": 16,
        "player1": "Daniil Medvedev",
        "player2": "Ben Shelton",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 2,
        "match": 17,
        "player1": "Winner of Match 1",
        "player2": "Winner of Match 2",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 2,
        "match": 18,
        "player1": "Winner of Match 3",
        "player2": "Winner of Match 4",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 2,
        "match": 19,
        "player1": "Winner of Match 5",
        "player2": "Winner of Match 6",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 2,
        "match": 20,
        "player1": "Winner of Match 7",
        "player2": "Winner of Match 8",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 2,
        "match": 21,
        "player1": "Winner of Match 9",
        "player2": "Winner of Match 10",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 2,
        "match": 22,
        "player1": "Winner of Match 11",
        "player2": "Winner of Match 12",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 2,
        "match": 23,
        "player1": "Winner of Match 13",
        "player2": "Winner of Match 14",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 2,
        "match": 24,
        "player1": "Winner of Match 15",
        "player2": "Winner of Match 16",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 3,
        "match": 25,
        "player1": "Winner of Match 17",
        "player2": "Winner of Match 18",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 3,
        "match": 26,
        "player1": "Winner of Match 19",
        "player2": "Winner of Match 20",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 3,
        "match": 27,
        "player1": "Winner of Match 21",
        "player2": "Winner of Match 22",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 3,
        "match": 28,
        "player1": "Winner of Match 23",
        "player2": "Winner of Match 24",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 4,
        "match": 29,
        "player1": "Winner of Match 25",
        "player2": "Winner of Match 26",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 4,
        "match": 30,
        "player1": "Winner of Match 27",
        "player2": "Winner of Match 28",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      },
      {
        "round": 5,
        "match": 31,
        "player1": "Winner of Match 29",
        "player2": "Winner of Match 30",
        "winner": None,
        "score_p1": None,
        "score_p2": None,
        "status": "尚未開始"
      }
    ]
    save_main_draw_data(initial_main_draw)
    print("mainDraw.json 已初始化為指定的賽程狀態。")

# --- 主程式入口點 ---
def main():
    """
    主函數：載入數據、執行排程，並自動觸發已結束比賽的結果同步。
    此函數假設 courts.json 和 mainDraw.json 會由外部系統或初始化步驟維護。
    """

    print("--- 系統啟動 ---")
    
    # --- 在這裡呼叫初始化函數來設定預設狀態 ---
    initialize_courts_data_to_specific_state()
    initialize_main_draw_to_specific_state() # 初始化 mainDraw.json 
    
    print(f"請檢查 {DATA_FILE} 和 {SCHEDULE_FILE} 的內容是否已更新為預設狀態。")


if __name__ == "__main__":
    main()