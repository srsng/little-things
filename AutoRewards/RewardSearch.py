import string
import DrissionPage as DP
import time
import random
import pyautogui


class DailySearch:
    def __init__(self, headless=True, user=None):
        self.reward_url = 'https://rewards.bing.com/'
        self.search_url = 'https://cn.bing.com/search?q=at'  # 搜索页面
        self.search_url_pc_with_key = 'https://cn.bing.com/search?q={}'
        self.search_url_mobile_with_key = "https://cn.bing.com/search?q={}&qs=ds&form=ANSPH1&pc=EDGEXST"
        self.reward_check_url = "https://rewards.bing.com/status/pointsbreakdown"
        self.co = DP.ChromiumOptions()

        if headless:
            self.co.set_headless()

        if user is None:
            self.co.set_user(user='Default')
        else:
            self.co.set_user(user=user)

        # 自动打开开发者工具
        self.co.set_argument("--auto-open-devtools-for-tabs")

        self.page = DP.ChromiumPage(self.co)

        self.page.set.main_tab()

    def __del__(self):
        print("[DailySearch]: user {} DONE".format(self.co.user))
        self.page.quit()

    def open_search_url(self):
        """
        打开搜索页面,用于查看创意式积分活动
        """
        self.page.get("https://cn.bing.com/search?q=t")

    @staticmethod
    def random_letters():
        t = ""
        times = random.randint(3, 10)
        for i in range(times):
            if random.randint(0, 1):
                t += str(random.randint(0, 9))
            else:
                t += string.ascii_letters[random.randint(0, 51)]
        return t

    def pc_search_daily(self, times: int):
        """
        根据需要的次数进行PC搜索
        """
        if times > 0:
            for i in range(times):
                self.page.get(self.search_url_pc_with_key.format(self.random_letters()))
                time.sleep(0.2)

        return None

    def mobile_model_on(self):
        self.page.to_main_tab()
        self.page.close_other_tabs()
        # pyautogui.hotkey('ctrl', 'shift', "i")
        # time.sleep(1)
        pyautogui.hotkey('ctrl', 'shift', "m")
        time.sleep(0.5)

    def mobile_model_off(self):
        self.page.to_main_tab()
        self.page.close_other_tabs()
        pyautogui.hotkey('ctrl', 'shift', "m")
        time.sleep(0.5)
        # pyautogui.hotkey('ctrl', 'shift', "i")
        # time.sleep(0.4)

    def mobile_search_daily(self, times: int):
        if times > 0:
            self.mobile_model_on()
            for i in range(times):
                self.page.get(self.search_url_mobile_with_key.format(self.random_letters()))
                time.sleep(0.4)
            self.mobile_model_off()
        return None

    def solve_more_activities(self):
        self.page.get(self.reward_url)
        card_group = self.page.eles('x://*[@id="more-activities"]/div/mee-card')
        for card in card_group:
            try:
                card.ele('x://span[@class="mee-icon mee-icon-AddMedium"]', timeout=0.5)
                card.ele('x://a[@class="ds-card-sec"]').click()
                time.sleep(1)
            except:
                pass

    def _run(self):
        print("user \"{}\" Start".format(self.co.user))
        # 每日PC搜索
        # times = self.laptop_search_get_needs()
        # self.pc_search_daily(int(times) + 1)
        print("\tuser \"{}\" PC Search Done".format(self.co.user))

        # 每日移动搜索
        times = 20
        self.mobile_search_daily(times)
        print("\tuser \"{}\" Mobile Search Done".format(self.co.user))
        # 每日积分活动
        # self.page.new_tab(self.reward_url)
        self.solve_more_activities()

        print("\tuser \"{}\" Activities Done".format(self.co.user))

    def get_times(self):
        self.page.get(self.reward_check_url)
        try:
            cur_status_ls = self.page.eles('x://p[@class="pointsDetail c-subheading-3 ng-binding"]//text()')
            cur_status_ls = [int(str(i).replace("/", "").replace(" ", "")) for i in cur_status_ls]
            print(f"{cur_status_ls[0]}/{cur_status_ls[1]}, {cur_status_ls[2]}/{cur_status_ls[3]}")
            pc_times = (cur_status_ls[1] - cur_status_ls[0]) // (3 if cur_status_ls[1] == 90 else 5)
            mobile_time = (cur_status_ls[3] - cur_status_ls[2]) // (3 if cur_status_ls[3] == 60 else 5)
        except:
            print("Something wrong, try doing max times.")
            pc_times = 30
            mobile_time = 20

        return pc_times, mobile_time

    def do_search(self, pc_search: bool = True, mobile_search: bool = False):
        do_pc = pc_search
        do_mobile = mobile_search
        loop_times = 0

        while do_pc or do_mobile:
            loop_times += 1
            pc, mo = self.get_times()

            if pc_search:
                self.pc_search_daily(pc)
                if pc == 0:
                    do_pc = False

            if mobile_search:
                self.mobile_search_daily(mo)
                if mo == 0:
                    do_mobile = False

            if loop_times > 4:
                do_pc = False
                do_mobile = False

    def run(self, pc_search: bool = True, mobile_search: bool = True):
        self.do_search(pc_search=pc_search, mobile_search=mobile_search)
        self.solve_more_activities()
