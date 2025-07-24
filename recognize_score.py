import cv2
import json
import sys
import os
import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import traceback # 用於打印完整的錯誤堆棧

sys.stdout.reconfigure(encoding='utf-8') # 針對 print() 輸出的內容
sys.stderr.reconfigure(encoding='utf-8') # 針對錯誤訊息或你用 print(..., file=sys.stderr) 的內容
# ----------------------------------------------------------------

'''# --- 全局偵錯日誌開頭 ---
print(f"[{os.path.basename(__file__)}] Python script starting...", file=sys.stderr)
# ... (rest of your recognize_score.py code) ...

# --- 全局偵錯日誌開頭（無 Unicode 符號） ---
print(f"[{os.path.basename(__file__)}] Python script starting...", file=sys.stderr)
print(f"[{os.path.basename(__file__)}] Current working directory: {os.getcwd()}", file=sys.stderr)
print(f"[{os.path.basename(__file__)}] Script directory: {os.path.dirname(__file__)}", file=sys.stderr)
# ---
'''

# 讓 Python 找得到 model.py
# 確保 SVHN 資料夾與 recognize_score.py 在同一層
svhn_path = os.path.join(os.path.dirname(__file__), 'SVHN')
sys.path.append(svhn_path)
#print(f"[{os.path.basename(__file__)}] Appending to sys.path: {svhn_path}", file=sys.stderr)

try:
    from model import SVHNCNN
    #print(f"[{os.path.basename(__file__)}] SVHNCNN model imported successfully.", file=sys.stderr)
except ImportError as e:
    print(f"[{os.path.basename(__file__)}] ERROR: Failed to import SVHNCNN model: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1) # 無法載入模型，直接退出

# 載入 SVHN 模型與權重
# 確保權重檔案路徑正確
model_weights_path = os.path.join(svhn_path, "svhn_cnn_weights.pth")
#print(f"[{os.path.basename(__file__)}] DEBUG: Model weights path: {model_weights_path}", file=sys.stderr)

if not os.path.exists(model_weights_path):
    print(f"[{os.path.basename(__file__)}] ERROR: Model weights file NOT FOUND at {model_weights_path}", file=sys.stderr)
    sys.exit(1) # 強制退出，讓 Node.js 捕獲到錯誤

try:
    model = SVHNCNN()
    model.load_state_dict(torch.load(model_weights_path, map_location="cpu"))
    model.eval()
    #print(f"[{os.path.basename(__file__)}] DEBUG: Model loaded successfully.", file=sys.stderr)
except Exception as e:
    print(f"[{os.path.basename(__file__)}] ERROR: Failed to load model: {e}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    sys.exit(1) # 強制退出

# SVHN 是彩色圖片，32x32
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((32, 32)),
    transforms.ToTensor(),
])

def enhance_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

def crop_score_regions(image):
    h, w = image.shape[:2]
    center_x = w // 2
    player1_img = image[:, :center_x]
    player2_img = image[:, center_x:]
    return player1_img, player2_img

def predict_digit(image_region):
    if isinstance(image_region, Image.Image):
        image_region = np.array(image_region)
    elif len(image_region.shape) == 2: # 如果是灰階，轉成三通道
        image_region = cv2.cvtColor(image_region, cv2.COLOR_GRAY2BGR)

    img_t = transform(image_region).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img_t)
        predicted = outputs.argmax(dim=1).item()
    return str(predicted if predicted != 10 else 0)

def parse_score(s):
    try:
        return int(s)
    except ValueError:
        return 0

# --- courts.json 檔案路徑定義 ---
# 假設 courts.json 與 recognize_score.py 在同一層目錄
DATA_FILE = os.path.join(os.path.dirname(__file__), 'courts.json')
#print(f"[{os.path.basename(__file__)}] DEBUG: DATA_FILE path: {DATA_FILE}", file=sys.stderr)

def read_courts_data():
    """讀取 courts.json 檔案。如果檔案不存在或格式錯誤，返回一個空列表。"""
    #print(f"[{os.path.basename(__file__)}] DEBUG: Attempting to read from {DATA_FILE}", file=sys.stderr)
    if not os.path.exists(DATA_FILE):
        print(f"[{os.path.basename(__file__)}] ERROR: courts.json NOT FOUND at {DATA_FILE}", file=sys.stderr)
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            #print(f"[{os.path.basename(__file__)}] DEBUG: courts.json read successful. Found {len(data)} courts.", file=sys.stderr)
            return data
    except json.JSONDecodeError as e:
        print(f"[{os.path.basename(__file__)}] ERROR: {DATA_FILE} JSON decode error: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return []
    except Exception as e:
        print(f"[{os.path.basename(__file__)}] ERROR: Failed to read {DATA_FILE}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return []

def save_courts_data(data):
    """將資料寫入 courts.json 檔案。"""
    #print(f"[{os.path.basename(__file__)}] DEBUG: Attempting to save to {DATA_FILE}", file=sys.stderr)
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False) # ensure_ascii=False 為了中文顯示
        #print(f"[{os.path.basename(__file__)}] DEBUG: courts.json saved successfully.", file=sys.stderr)
        return {"success": True}
    except Exception as e:
        print(f"[{os.path.basename(__file__)}] ERROR: Failed to write to {DATA_FILE}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return {"error": f"寫入 {DATA_FILE} 失敗: {e}"}

def recognize_and_process_court(court_id_str):
    """處理單一球場的比分識別和數據更新。"""
    court_id = int(court_id_str)
    
    # 確保 score_ocr folder 的路徑也是絕對的
    # score_ocr 資料夾應該與 recognize_score.py 在同一層
    folder = os.path.join(os.path.dirname(__file__), "score_ocr", f"court_{court_id}")
    #print(f"[{os.path.basename(__file__)}] DEBUG: Processing Court {court_id}. Image folder: {folder}", file=sys.stderr)

    if not os.path.exists(folder):
        print(f"[{os.path.basename(__file__)}] ERROR: Court folder NOT FOUND: {folder}", file=sys.stderr)
        return # 不再返回詳細結果給 stdout，直接透過 stderr 記錄錯誤

    images = sorted([f for f in os.listdir(folder) if f.endswith(".jpg") or f.endswith(".png")])
    if not images:
        print(f"[{os.path.basename(__file__)}] ERROR: No images found in folder: {folder}", file=sys.stderr)
        return # 不再返回詳細結果

    latest_img_path = os.path.join(folder, images[-1])
    #print(f"[{os.path.basename(__file__)}] DEBUG: Latest image path: {latest_img_path}", file=sys.stderr)
    image = cv2.imread(latest_img_path)
    if image is None:
        print(f"[{os.path.basename(__file__)}] ERROR: Image read failed for: {latest_img_path}", file=sys.stderr)
        return # 不再返回詳細結果

    try:
        #enhanced_image = enhance_image(image)  處理圖像
        enhanced_image = image 
        region1, region2 = crop_score_regions(enhanced_image) # 對處理後的圖像進行裁剪

        score1_str = predict_digit(region1)
        score2_str = predict_digit(region2)
        #print(f"[{os.path.basename(__file__)}] DEBUG: Predicted scores for Court {court_id}: {score1_str}:{score2_str}", file=sys.stderr)

        s1 = parse_score(score1_str)
        s2 = parse_score(score2_str)
        
        # 比分狀態判斷邏輯
        status = "進行中"
        if ((s1 >= 6 or s2 >= 6) and abs(s1 - s2) >= 2) or s1 >= 7 or s2 >= 7:
            status = "比賽結束"
        
        #print(f"[{os.path.basename(__file__)}] DEBUG: Court {court_id} status: {status}", file=sys.stderr)
        
        # --- 在這裡讀取、更新並儲存 courts.json ---
        courts_data = read_courts_data()
        
        court_index = court_id - 1
        if 0 <= court_index < len(courts_data):
            #print(f"[{os.path.basename(__file__)}] DEBUG: Updating courts_data[{court_index}] for Court {court_id}", file=sys.stderr)
            courts_data[court_index]["score1"] = score1_str
            courts_data[court_index]["score2"] = score2_str
            courts_data[court_index]["status"] = status
            
            save_result = save_courts_data(courts_data)
            if "error" in save_result:
                print(f"[{os.path.basename(__file__)}] ERROR: Failed to save courts.json after updating Court {court_id}: {save_result['error']}", file=sys.stderr)
        else:
            print(f"[{os.path.basename(__file__)}] ERROR: Invalid court index {court_index} for Court {court_id} in courts.json. Data length: {len(courts_data)}", file=sys.stderr)

    except Exception as e:
        print(f"[{os.path.basename(__file__)}] ERROR: AI prediction or processing failed for Court {court_id}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr) # 打印完整的錯誤堆棧


if __name__ == "__main__":
    print(f"[{os.path.basename(__file__)}] Python script execution started via __main__.", file=sys.stderr)
    if len(sys.argv) != 2:
        print(f"[{os.path.basename(__file__)}] ERROR: Invalid number of arguments. Usage: python recognize_score.py [court_id|all]", file=sys.stderr)
        sys.exit(1)

    input_court_id = sys.argv[1]
    #print(f"[{os.path.basename(__file__)}] DEBUG: Received argument: {input_court_id}", file=sys.stderr)

    if input_court_id == "all":
        #print(f"[{os.path.basename(__file__)}] DEBUG: Processing all courts (1-12).", file=sys.stderr)
        for i in range(1, 13):
            recognize_and_process_court(str(i)) # 不再收集結果
    else:
        try:
            cid = int(input_court_id)
            if cid < 1 or cid > 12:
                raise ValueError()
            #print(f"[{os.path.basename(__file__)}] DEBUG: Processing single court: {input_court_id}.", file=sys.stderr)
            recognize_and_process_court(input_court_id) # 不再收集結果
        except ValueError:
            print(f"[{os.path.basename(__file__)}] ERROR: Invalid court ID: {input_court_id}", file=sys.stderr)
            sys.exit(1)
    
    print(f"[{os.path.basename(__file__)}] Python script finished execution.", file=sys.stderr)