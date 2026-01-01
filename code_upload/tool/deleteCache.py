from pathlib import Path
import shutil

def cleanCache(cache_id : str) -> dict :
    code_Path = Path(__file__).resolve().parent.parent
    to_be_clean_Path = code_Path / "cache" / cache_id
    if to_be_clean_Path.exists() and to_be_clean_Path.is_dir():
        shutil.rmtree(to_be_clean_Path)
        resultClean = {
            "success" : True,
            "deleteFolder" : str(to_be_clean_Path)
        }
        return resultClean
    else:
        resultClean = {
            "success" : False,
            "cache_id" : cache_id,
            "deleteFolder" : str(to_be_clean_Path)
        }

if __name__ == "__main__":
    print("輸入欲刪除的cahce id:")
    cache_id = input()
    result = cleanCache(cache_id)
    print(result["success"])