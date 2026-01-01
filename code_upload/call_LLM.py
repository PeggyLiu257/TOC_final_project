import requests

api_key = ""
api_uri = ""
model = "gemma3:4b"

def call_LLM(message: str):
    headers = {
        "Authorization" : f"Bearer {api_key}" ,
        "Content_type" : "application/json"
    }

    payload = {
        "model" : model,
        "prompt" : message,
        "stream" : False
    }

    r = requests.post(api_uri,  json=payload, headers=headers, timeout=60)
    r.raise_for_status()

    if r.json()["done_reason"] == 'load':
        r = requests.post(api_uri, json=payload, headers=headers, timeout=60)
        r.raise_for_status()

    return r.json()['response']

if __name__ == "__main__":
    reply = call_LLM(f"""          
輸入會包含四個以 "||" 分隔的詞：
- 第一個詞：玩家輸入
- 第二到第四個詞：正確的詞，包含不同語言（繁體中文 / 英文 / 日文）

你的任務是：
判斷「第一個詞」是否在字面或合理錯字範圍內，與後三個詞中的任一個表示同一部電影。

比對規則：
- 允許輕微錯字、大小寫差異、或常見譯名錯誤（例如艾莉緹 / 愛麗緹）。
- 不允許不同電影名稱。
- 不允許將不同作品視為相同。

嚴格禁止（必須遵守）：
- 禁止使用任何外部知識或背景推論。
- 禁止自行翻譯、改寫、補充或創造電影名稱。
- 禁止產生任何解釋或說明文字。

輸出規則：
- 輸出 yes 或 no
- 不得輸出任何其他文字、符號、標點或換行。

玩家輸入：龍貓||地海戰記||Tales from Earthsea||ゲド戦記
            """)
    print(reply)