import os
from pathlib import Path

def openPic(path : str):
    open_path = Path(path)
    if not open_path.exists():
        print("錯誤！找不到檔案")
        return
    
    os.startfile(str(open_path.resolve()))

if __name__ == "__main__":
    path = input("請輸入路徑：")
    openPic(path)