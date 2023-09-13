from RewardSearch import DailySearch


if __name__ == "__main__":
    for user in user_list:
        ds = DailySearch(True, user=user)
        ds.run()
        del ds

    input("Press Enter to exit...")
    quit()
