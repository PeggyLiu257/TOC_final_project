from agent import Agent

def main():
    print("—————— 吉卜力電影大師 ——————")
    print(
        "這是一個看吉卜力劇照猜測來源電影的遊戲\n"
        "首先，請輸入想要的遊戲難度敘述，不同難度會將圖片裁切不同大小。\n"
        "接著，必須看圖猜測圖片出自哪一部吉卜力電影。\n"
        "若是答對了，這局遊戲就贏了。\n"
        "若是答錯了，玩家可以選擇直接公布答案開始下一輪遊戲，或者以原題目降低難度再猜測一次。\n"
        "注意，只能有一次的重猜機會，若是答對了就贏了這一輪遊戲；若是再次猜錯則輸掉遊戲，本輪結束。\n"
    )
    print("提示：若要離開請輸入exit")
    
    agent = Agent()

    while True:
        user_input = input("玩家 > ").strip()

        if user_input.lower() == "exit":
            print("結束遊戲")
            break

        reply = agent.step(user_input)
        print(f"小精靈 > {reply}")
        if agent.cont == False:
            break

if __name__ == "__main__":
    main()