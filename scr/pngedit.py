import base64
import os

# プログラム自身の場所を基準にする
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 1つ上の階層の assets フォルダ内にある 97.png を指す
IMAGE_PATH = os.path.join(BASE_DIR, "..", "assets", "97.png")

try:
    with open(IMAGE_PATH, "rb") as f:
        # 画像を文字列（Base64）に変換
        img_str = base64.b64encode(f.read()).decode('utf-8')
        
        # 結果をテキストファイルに保存（コンソールだと長すぎて切れるため）
        with open("encoded_image.txt", "w") as out:
            out.write(img_str)
            
        print("変換成功！ 'encoded_image.txt' に保存しました。")
        print("この中身を main.py の IMG_DATA に貼り付けてください。")

except FileNotFoundError:
    print(f"エラー: {IMAGE_PATH} が見つかりません。")
    print("フォルダ構成とファイル名が合っているか確認してください。")