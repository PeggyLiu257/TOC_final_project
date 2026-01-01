from tool.getPic import getOrigPic
from tool.processPic import cropPic
from tool.deleteCache import cleanCache
from openPic import openPic
from call_LLM import call_LLM

dif_mode_name = ["簡單", "普通", "困難", "專家"]
state_name = ["askDif", "guessing", "wrongAns", "end"]

class Agent:
    def __init__(self):
        self.state = state_name[0]
        self.try_time = 0
        self.dif = None
        self.cache_id = None
        self.cache_id_path = None
        self.ans_zh = None
        self.ans_en = None
        self.ans_jp = None
        self.ans_pic_path = None
        self.pb_pic_path1 = None
        self.pb_pic_path2 = None
        self.crp_center_x = None
        self.crp_center_y = None
        self.cont = True

    # classify states
    def step(self, user_input : str):
        if self.state == state_name[0]:
            return self.askDif(user_input)
        
        elif self.state == state_name[1]:
            return self.judgeAns(user_input)
        
        elif self.state == state_name[2]:
            return self.wrongAns(user_input)
        
        elif self.state == state_name[3]:
            return self.endGame(user_input)
    
    # ask the expected difficulty to user
    def askDif(self, user_input: str) -> str:
        self.dif = self.detemine_dif(user_input)
        if self.dif == -1:
            return "輸入錯誤！請輸入難度！"
        elif self.dif == -2:
            return "連線失敗，請稍後重新輸入難度"

        resultAns = getOrigPic()
        self.ans_zh = resultAns["ans_movie_zh"]
        self.ans_en = resultAns["ans_movie_en"]
        self.ans_jp = resultAns["ans_movie_jp"]
        self.cache_id_path = resultAns["cache_id_folder"]
        self.cache_id = resultAns["cache_id"]
        self.ans_pic_path = resultAns["ans_pic_path"]

        resultPb = cropPic(self.cache_id, self.dif)
        self.pb_pic_path1 = resultPb["pb_pic_path"]
        self.crp_center_x = resultPb["crp_center_x"]
        self.crp_center_y = resultPb["crp_center_y"]

        openPic(self.pb_pic_path1)

        self.state = state_name[1]
        self.try_time = 1

        return (f"題目難度：{dif_mode_name[self.dif]}\n請問這是哪一部電影呢？")
    
    def detemine_dif(self, user_input) -> int:
        prompt = f"""
            你是一個輸入解析器。
            任務：判斷玩家想要的遊戲難度。
            只允許輸出以下其中一個單字（完全一致，小寫，不要任何其他字）：
            easy
            normal
            hard
            expert
            unknown

            判斷規則(舉例，僅供參考，不只有以下的可能輸入)：
            - 玩家想要「最難、地獄、最不可能、超難、專家、最高難度」→ expert
            - 玩家想要「簡單、入門、容易、新手」→ easy
            - 玩家想要「普通、一般」→ normal
            - 玩家想要「困難、很難」→ hard
            - 無法判斷 → unknown

            玩家輸入：{user_input}
            """
        try:
            dif_result = call_LLM(prompt).strip().lower()
            while dif_result == "":
                dif_result = call_LLM(prompt).strip().lower()
            
            resultToNum = {"easy" : 0, "normal" : 1, "hard" : 2, "expert": 3}
            return resultToNum.get(dif_result, -1)
        except:
            return -2

    def judgeAns(self, user_input: str) -> str:
        prompt = f"""
請執行一個「字面名稱比對任務」。

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

輸入：{user_input}||{self.ans_zh}||{self.ans_en}||{self.ans_jp}
            """
        llm_judge = call_LLM(prompt).strip().lower()
        if user_input == self.ans_zh:
            self.state = state_name[3]
            reply = f"回答正確！答案是{self.ans_zh}。本輪結束，是否再次遊玩？若選否將自動關閉"
            if self.dif > 0:
                openPic(self.ans_pic_path)
            return reply
        elif user_input == self.ans_en:
            self.state = state_name[3]
            reply = f"回答正確！答案是{self.ans_en}。本輪結束，是否再次遊玩？若選否將自動關閉"
            if self.dif > 0:
                openPic(self.ans_pic_path)
            return reply
        elif user_input == self.ans_jp:
            self.state = state_name[3]
            reply = f"回答正確！答案是{self.ans_jp}。本輪結束，是否再次遊玩？若選否將自動關閉"
            if self.dif > 0:
                openPic(self.ans_pic_path)
            return reply
        else:

            if llm_judge == "yes":
                self.state = state_name[3]
                reply = f"回答正確！答案是{self.ans_zh}。本輪結束，是否再次遊玩？若選否將自動關閉"
                if self.dif > 0:
                    openPic(self.ans_pic_path)
                return reply
            else:
                if self.dif == 0:
                    self.state = state_name[3]
                    return f"回答錯誤！答案是{self.ans_zh}。本輪結束，是否再次遊玩？若選否將自動關閉"
                else:
                    if self.try_time == 1:
                        self.state = state_name[2]
                        return f"回答錯誤！要降低難度再猜一次還是直接公布答案呢？"
                    else:
                        openPic(self.ans_pic_path)
                        return f"回答錯誤！答案是{self.ans_zh}。本輪結束，是否再次遊玩？若選否將自動關閉"

    def wrongAns(self, user_input: str):
        prompt = f"""
請根據以下輸入判斷玩家語意，告訴我他想要直接公布答案還是降低難度再次猜測？
回答只能使用yes或no，不可以加其他任何字
如果他要直接公布答案(不繼續猜測)，回答no；如果他要再次猜測，回答yes

玩家輸入：{user_input}
"""     
        llm_reply = call_LLM(prompt).strip().lower()
        if llm_reply == "no":
            self.state = state_name[3]
            openPic(self.ans_pic_path)
            return f"答案是{self.ans_zh}。本輪結束，是否再次遊玩？若選否將自動關閉"
        else:
            self.try_time = 2
            self.dif = self.dif - 1
            resultPb = cropPic(self.cache_id, self.dif, self.crp_center_x, self.crp_center_y)
            self.pb_pic_path2 = resultPb["pb_pic_path"]
            openPic(self.pb_pic_path2)
            self.state = state_name[1]
            return "再次猜測吧！答案是哪部電影呢？"
    
    def endGame(self, user_input: str) -> str:
        cleanCache(self.cache_id)
        prompt = f"""
請根據以下輸入判斷玩家語意，告訴我他想要再次進行遊戲還是結束遊戲？
回答只能使用yes或no，不可以加其他任何字
如果他要結束遊戲，回答no；如果他要再次進行遊戲，回答yes

玩家輸入：{user_input}
"""     
        llm_reply = call_LLM(prompt).strip().lower()
        if llm_reply == "no":
            self.cont = False
            return "感謝遊玩，拜拜~"
        else:
            self.__init__()
            return "好的，請輸入這次遊玩想要的難度"
            

if __name__ == "__main__":
    agent = Agent()
    user_input = input("請輸入：")
    reply = agent.step(user_input)
    print("回覆：", reply)