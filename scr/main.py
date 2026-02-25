import tkinter as tk
from PIL import Image, ImageTk
import pyautogui
import random
from pynput import keyboard
import os
import requests  # 追加
import tempfile  # 追加

# --- 設定 ---
# GitHubの「Raw」ボタンを押した後のURLをここに貼り付けてください
IMAGE_URL = "https://raw.githubusercontent.com/cocolo0503/akyama_w/main/assets/97.png"

secret_word = "akiyamaoshi"
COMMAND = [keyboard.KeyCode.from_char(c) for c in secret_word]

current_input = []
AUTO_SPAWN_INTERVAL = 3000  
MAX_WINDOWS = 500000            
window_count = 0            

# ★ 追加：画像をオンラインから取得してパスを返す関数
def get_image_path():
    # PCの一時フォルダに保存するパスを作成
    temp_path = os.path.join(tempfile.gettempdir(), "downloaded_97.png")
    
    # まだダウンロードしていない場合のみ実行
    if not os.path.exists(temp_path):
        try:
            print("画像をダウンロード中...")
            response = requests.get(IMAGE_URL, timeout=10)
            if response.status_code == 200:
                with open(temp_path, "wb") as f:
                    f.write(response.content)
            else:
                return None # ダウンロード失敗
        except Exception as e:
            print(f"エラー: {e}")
            return None
    return temp_path

# ダウンロードを実行してパスを取得
IMAGE_PATH = get_image_path()

def on_press(key):
    global current_input
    current_input.append(key)
    if len(current_input) >= len(COMMAND):
        if current_input[-len(COMMAND):] == COMMAND:
            print("隠しコマンド成功！終了します。")
            root.destroy()
            return False 
    if len(current_input) > 20:
        current_input = current_input[-len(COMMAND):]

listener = keyboard.Listener(on_press=on_press)
listener.start()

def create_window():
    global window_count
    if window_count >= MAX_WINDOWS or IMAGE_PATH is None:
        return

    window = tk.Toplevel()
    window.overrideredirect(True)
    window.attributes("-topmost", True)

    width, height = 200, 200
    # IMAGE_PATH（一時フォルダのパス）から読み込む
    img = Image.open(IMAGE_PATH).convert("RGBA")
    img = img.resize((width, height))
    tk_img = ImageTk.PhotoImage(img)
    
    label = tk.Label(window, image=tk_img)
    label.image = tk_img
    label.pack()

    screen_w, screen_h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry(f"+{random.randint(0, screen_w-100)}+{random.randint(0, screen_h-100)}")
    
    label.bind("<Button-1>", lambda e: create_window())
    window_count += 1
    root.after(AUTO_SPAWN_INTERVAL, create_window)

def jump_mouse():
    screen_w, screen_h = pyautogui.size()
    pyautogui.moveTo(random.randint(0, screen_w), random.randint(0, screen_h), duration=0)
    root.after(5000, jump_mouse)

root = tk.Tk()
root.withdraw() 

# 画像が正常に準備できてから開始
if IMAGE_PATH:
    create_window()
    jump_mouse()
    root.mainloop()
else:
    print("画像が取得できなかったため起動できませんでした。URLを確認してください。")