import json
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8') # 針對 print() 輸出的內容
sys.stderr.reconfigure(encoding='utf-8') # 針對錯誤訊息或你用 print(..., file=sys.stderr) 的內容
# --- 配置檔案名稱 ---
DATA_FILE = "courts.json"      # 用於儲存球場狀態和排程資訊
SCHEDULE_FILE = "mainDraw.json" # 用於儲存賽程表和比賽結果 (勝者)

# --- 球場數據的載入和儲存 ---
def load_data():
    """從 courts.json 載入球場數據"""
    if not os.path.exists(DATA_FILE):
        # 如果檔案不存在，初始化預設球場並寫入
        initial_courts = [
          { "id": f"Court {i+1}", "player1": "", "player2": "", "nextPlayers": "", "status": "空閒", "score1": None, "score2": None, "current_match_number": None, "next_match_number": None }
          for i in range(2) # 假設預設有 2 個球場
        ]
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(initial_courts, f, ensure_ascii=False, indent=2)
        return initial_courts
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """將球場數據存回 courts.json"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# --- 輔助函數：讀取和寫入 mainDraw.json ---
def load_main_draw_data():
    """從 mainDraw.json 載入賽程數據"""
    if not os.path.exists(SCHEDULE_FILE):
        # 如果檔案不存在，初始化一個空列表並寫入，以避免後續錯誤
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        return []
    with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_main_draw_data(main_draw_data):
    """將賽程數據存回 mainDraw.json"""
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(main_draw_data, f, ensure_ascii=False, indent=2)

### 將mainDraw.json 中 'Winner of Match X' 換成實際勝者
def resolve_winner_placeholders_in_main_draw():
    """
    讀取 mainDraw.json，並將其中所有 'Winner of Match X' 的選手佔位符
    替換為實際的勝者名稱，如果該勝者已確定。
    會將修改後的數據寫回 mainDraw.json。
    """
    main_draw_data = load_main_draw_data()
    has_changes = False
    
    # Compile the regex pattern once for efficiency
    match_pattern = re.compile(r"Winner of (Match \d+)")

    for current_match_info in main_draw_data:
        # Helper to find winner directly within this function
        def _get_winner_for_placeholder(placeholder_str):
            match_result = match_pattern.match(placeholder_str)
            if match_result:
                target_match_label = match_result.group(1)
                try:
                    target_match_number = int(target_match_label.split(' ')[1])
                    for m_info in main_draw_data: # Iterate over the full main_draw_data to find the target match
                        if m_info.get("match") == target_match_number:
                            return m_info.get("winner") 
                except (ValueError, IndexError):
                    pass # Invalid match number format
            return None # Placeholder not found or winner not determined

        # Process player1
        p1_orig_name = current_match_info.get('player1', '')
        if "Winner of Match" in p1_orig_name:
            actual_p1 = _get_winner_for_placeholder(p1_orig_name)
            if actual_p1 and p1_orig_name != actual_p1: # Ensure there's a winner and it's different from current
                current_match_info['player1'] = actual_p1
                has_changes = True
                print(f"已將比賽 {current_match_info.get('match')} 的 Player1 從 '{p1_orig_name}' 更新為 '{actual_p1}'。")

        # Process player2
        p2_orig_name = current_match_info.get('player2', '')
        if "Winner of Match" in p2_orig_name:
            actual_p2 = _get_winner_for_placeholder(p2_orig_name)
            if actual_p2 and p2_orig_name != actual_p2: # Ensure there's a winner and it's different from current
                current_match_info['player2'] = actual_p2
                has_changes = True
                print(f"已將比賽 {current_match_info.get('match')} 的 Player2 從 '{p2_orig_name}' 更新為 '{actual_p2}'。")
    
    if has_changes:
        save_main_draw_data(main_draw_data)
        print("mainDraw.json 已更新，勝者佔位符已替換為實際選手名稱。")
    else:
        print("mainDraw.json 中沒有需要更新的勝者佔位符。")



def complete_match_on_court(court_id: str):
    """
    處理指定球場上比賽的結束流程：
    1. 從 courts.json 讀取該球場的狀態和分數。
    2. 使用球場上的 current_match_number 找到 mainDraw.json 中對應的比賽。
    3. 更新 mainDraw.json 中該比賽的狀態為 "比賽結束"，並寫入分數和勝者。
       注意：此函數會根據分數判斷勝者，並將其寫入 mainDraw.json 的 winner 欄位。
    4. 清空 courts.json 中該球場的 player1, player2, score1, score2, current_match_number，並將狀態設為 "空閒"。

    Args:
        court_id (str): 結束比賽的球場 ID (例如："Court 1")。
    """
    courts_data = load_data()
    main_draw_data = load_main_draw_data()

    target_court = None
    for court in courts_data:
        if court.get("id") == court_id:
            target_court = court
            break

    if not target_court:
        print(f"錯誤：找不到球場 '{court_id}'。")
        return

    current_match_num = target_court.get("current_match_number")
    if current_match_num is None:
        print(f"錯誤：球場 '{court_id}' 目前沒有進行中的比賽或無有效比賽編號。")
        return

    current_player1 = target_court.get("player1")
    current_player2 = target_court.get("player2")
    try:
        final_score1 = int(target_court.get("score1")) if target_court.get("score1") is not None else None
        final_score2 = int(target_court.get("score2")) if target_court.get("score2") is not None else None
    except (ValueError, TypeError):
        final_score1 = None
        final_score2 = None

    # 檢查分數是否為有效數字
    if not isinstance(final_score1, (int, float)) or not isinstance(final_score2, (int, float)):
        print(f"警告：球場 '{court_id}' 上的比賽分數無效 ({final_score1}-{final_score2})。無法確定勝者。")
        final_winner = None
    else:
        # 根據分數判斷勝者
        if final_score1 > final_score2:
            final_winner = current_player1
        elif final_score2 > final_score1:
            final_winner = current_player2
        else:
            final_winner = None # 平局

    # 在 mainDraw.json 中找到對應的比賽並更新
    match_found_in_draw = False
    for match_info in main_draw_data:
        if match_info.get("match") == current_match_num:
            if match_info.get("status") != "比賽結束": 
                match_info["status"] = "比賽結束"
                match_info["score_p1"] = final_score1
                match_info["score_p2"] = final_score2
                # 將判斷出的勝者保存到 mainDraw.json
                match_info["winner"] = final_winner 
                match_found_in_draw = True
                print(f"已更新 mainDraw.json 中比賽 {current_match_num} 的結果：")
                print(f"  選手: {current_player1} vs {current_player2}")
                print(f"  比分: {final_score1}-{final_score2}，勝者: {final_winner}")
                break
            else:
                print(f"警告：mainDraw.json 中的比賽 (Match {current_match_num}) 已標記為 '比賽結束'，跳過更新。")
                match_found_in_draw = True
                break

    if not match_found_in_draw:
        print(f"警告：在 mainDraw.json 中找不到與球場 '{court_id}' (比賽編號 {current_match_num}) 對應的比賽。")

    # 更新 courts.json 中該球場的狀態和清空選手資訊
    target_court["player1"] = ""
    target_court["player2"] = ""
    target_court["score1"] = None
    target_court["score2"] = None
    target_court["status"] = "空閒"
    target_court["current_match_number"] = None
    
    '''這邊由assign_next_match 來處理
    target_court["next_match_number"] = None # This was already in place'''

    save_data(courts_data) # 保存更新後的 courts.json
    save_main_draw_data(main_draw_data) # 保存更新後的 mainDraw.json
    print(f"球場 '{court_id}' 已清空並設為空閒。")

        
def assign_next_match(data):
    """
    根據球場狀態和等待選手列表，排定下一場比賽。
    邏輯現在改為：
    1. 首先檢查並將 nextPlayers 晉升到 player1/player2 (如果主場地空閒)。
    2. 然後再為所有可用的 nextPlayers 位置預排新比賽。
    注意：此函數不再負責更新 mainDraw.json 中的勝者佔位符。
    """
    active_player_names = set() # 用於追蹤單一選手是否活躍
    scheduled_match_numbers = set()

    # 從目前的球場數據中填充 active_player_names 和 scheduled_match_numbers
    # 這裡的目的是在排程前，先知道哪些選手和比賽已經被佔用或預定
    for court in data:
        if court["player1"].strip():
            active_player_names.add(court['player1'].strip())
        if court["player2"].strip():
            active_player_names.add(court['player2'].strip())
        if court.get("current_match_number") is not None:
            scheduled_match_numbers.add(court["current_match_number"])

        if court["nextPlayers"].strip():
            p1_next, p2_next = court["nextPlayers"].strip().split(" vs ")
            active_player_names.add(p1_next)
            active_player_names.add(p2_next)
        if court.get("next_match_number") is not None:
            scheduled_match_numbers.add(court["next_match_number"])

    # --- 整合 get_waiting_players 的邏輯 ---
    main_draw_data = load_main_draw_data() # Load current mainDraw data
    waiting_matches_info = []
    
    for match in main_draw_data:
        # Exclude completed matches, these don't need to be scheduled
        if match.get("status") == "比賽結束":
            continue

        p1_name = match['player1'] 
        p2_name = match['player2']
        match_num = match['match'] 

        # If a player is still a placeholder, it means the winner isn't determined yet,
        # so this match cannot be scheduled.
        if "Winner of Match" in p1_name or "Winner of Match" in p2_name:
            continue

        waiting_matches_info.append((match_num, p1_name, p2_name))
    
    waiting_matches_info.sort(key=lambda x: x[0]) # Sort by match_num to prioritize lower-numbered matches
    # --- 整合結束 ---

    # --- 階段一：晉升預備選手到主場地 ---
    for court in data:
        # 如果 player1/player2 是空的，並且 nextPlayers 有選手
        if not court["player1"].strip() and not court["player2"].strip() and court["nextPlayers"].strip():
            
            p1_promo, p2_promo = court["nextPlayers"].strip().split(" vs ")
            match_num_promo = court["next_match_number"]

            court["player1"] = p1_promo
            court["player2"] = p2_promo
            court["status"] = "進行中" # 比賽正式開始
            court["score1"] = 0
            court["score2"] = 0
            court["current_match_number"] = match_num_promo # 將預排的比賽編號移為當前比賽編號
            
            # 清空 nextPlayers 和 next_match_number，為下一次預排準備
            court["nextPlayers"] = "" 
            court["next_match_number"] = None
            
            print(f"球場 {court['id']}：已將預備比賽 {match_num_promo} ({p1_promo} vs {p2_promo}) 晉升至主場地。")
            

    # --- 階段二：為所有可用的 nextPlayers 位置預排新比賽 ---
    for court in data:
        if not court["nextPlayers"].strip(): # 如果 nextPlayers 是空的
            for match_num, p1, p2 in waiting_matches_info:
                # 檢查這個比賽是否已經被排程到任何球場 (當前或下一場)
                if match_num in scheduled_match_numbers:
                    continue

                # 檢查選手是否已經在場上或已排入下一場
                if p1 in active_player_names or p2 in active_player_names:
                    continue # 選手活躍，跳過這場比賽

                # 如果選手都不活躍，則將比賽分配給這個球場的 nextPlayers
                court["nextPlayers"] = f"{p1} vs {p2}"
                court["next_match_number"] = match_num # 儲存比賽編號到 next_match_number
                
                # 將這些選手和比賽標記為已使用，避免重複排程
                active_player_names.add(p1)
                active_player_names.add(p2)
                scheduled_match_numbers.add(match_num)
                
                print(f"已預排比賽 {match_num} ({p1} vs {p2}) 到球場 {court['id']} 的下一場。")
                break # 找到一組就停止，處理下一個球場

# --- 主程式入口點 ---
def main():
    """
    主函數：載入數據、執行排程，並自動觸發已結束比賽的結果同步。
    """

    print("\n--- 系統啟動 ---")
    
    # 確保文件存在或被初始化
    _ = load_data() # 載入並確保 courts.json 存在
    _ = load_main_draw_data() # 載入並確保 mainDraw.json 存在

    # Step 1: 自動更新 mainDraw.json 中的勝者佔位符 (先執行)
    print("\n--- 執行自動更新 mainDraw.json 中的勝者佔位符 ---")
    resolve_winner_placeholders_in_main_draw()

    # Step 2: 自動檢測並同步結束的比賽結果 (從 courts.json 判斷)
    # 使用 while 迴圈確保所有已結束的比賽都被處理，因為每次處理會改變 courts.json 的狀態
    print("\n--- 執行自動檢測並同步結束的比賽結果 ---")
    
    # 這裡的邏輯需要確保只要有任何一個球場被標記為"比賽結束"，它就能被處理
    # 我們使用一個迴圈，直到沒有更多「比賽結束」狀態的球場為止
    while True:
        courts_data_current = load_data() # 每次迴圈都載入最新狀態
        found_completed_match = False
        
        for court in courts_data_current:
            if court.get("status") == "比賽結束" and court.get("current_match_number") is not None:
                print(f"DEBUG: 檢測到球場 {court['id']} (Match {court['current_match_number']}) 狀態為 '比賽結束'，觸發處理。")
                complete_match_on_court(court["id"])
                found_completed_match = True
                # 因為 complete_match_on_court 會修改並保存 courts.json，
                # 所以一旦處理完一個球場，我們需要中斷當前迴圈並重新從檔案載入最新數據
                # 否則，你可能會在一個過時的數據副本上繼續迭代
                break # 處理完一個就跳出內層 for 迴圈，重新開始外層 while 迴圈
        
        if not found_completed_match:
            break # 如果沒有找到任何已結束的比賽，則跳出 while 迴圈
            
    # Step 3: 執行比賽排程
    print("\n--- 執行比賽排程 ---")
    # 重新載入 courts.json 的最新狀態，因為前面的 `complete_match_on_court` 可能已經修改了它
    court_data_for_assignment = load_data() 
    assign_next_match(court_data_for_assignment)
    save_data(court_data_for_assignment) # 保存排程後的 courts.json
    
    print(json.dumps({"status": "ok", "message": "下一場選手排程完成"}))

    print("\n--- 系統任務執行完畢 ---")
            

if __name__ == "__main__":
    main()