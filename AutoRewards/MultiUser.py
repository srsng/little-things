from RewardSearch import DailySearch


class MultiUser:
    def __init__(self, headless, need_wait_users_list: [str] = None, *args):
        self.need_wait_users_list = [] if need_wait_users_list is None else need_wait_users_list
        self.user_list = args

        self.ds_no_wait_list = []
        self.ds_need_wait_list = []
        for user in args:
            if user in self.need_wait_users_list:
                self.ds_need_wait_list.append(DailySearch(headless, user=user))
            else:
                self.ds_no_wait_list.append(DailySearch(headless, user=user))

    def __del__(self):
        print("[MultiUser]: DONE")

    def run(self):
        for ds in self.ds_no_wait_list:
            ds.init_page()
            ds.run()
            del ds
        for ds in self.ds_need_wait_list:
            input("Waitting to start {}\nPress Enter to go ahead.".format(ds.co.user))
            ds.run()
            del ds


if __name__ == '__main__':
    mu = MultiUser(False,  None, "Profile 1", "Default")
    # print(mu.need_wait_users_list)
    # print(mu.user_list)
    mu.run()
    quit()
