from RewardSearch import DailySearch


if __name__ == "__main__":
    user_list = ["Deafult"] # 按readme.md修改这行
    for user in user_list:
        ds = DailySearch(False, user=user)
        ds.run()
        del ds

    # 想要结束后自己关掉提示用的命令行就删掉下面这行
    input("Press Enter to exit...")
    
    quit()
