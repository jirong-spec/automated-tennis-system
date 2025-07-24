from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # 使用 OCR 辨識
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image, lang='eng')
    
    # 假設格式為 "11-8" 或 "11 : 8"
    import re
    match = re.search(r'(\d{1,2})\D+(\d{1,2})', text)
    if match:
        score1, score2 = match.groups()
        return jsonify({"score1": score1, "score2": score2})
    else:
        return jsonify({"error": "無法辨識比數"}), 200

if __name__ == '__main__':
    app.run(port=5000)
