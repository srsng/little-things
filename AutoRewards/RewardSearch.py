import DrissionPage as DP
import time
import random
from DrissionPage.errors import ElementNotFoundError


class DailySearch:
    def __init__(self, headless=True, user=None):
        self.reward_url = 'https://rewards.bing.com/'
        self.search_url = 'https://cn.bing.com/search?q=at'  # 搜索页面
        self.reward_check_url = "https://rewards.bing.com/status/pointsbreakdown"
        self.co = DP.ChromiumOptions()

        self.login_url = 'https://login.live.com/'
        self.words = self.init_random_words()

        if headless:
            self.co.set_headless()

        if user is None:
            self.co.set_user(user='Default')
        else:
            self.co.set_user(user=user)

        self.page = DP.ChromiumPage(self.co)

    def __del__(self):
        self.page.quit()
        print("[DailySearch]: user {} DONE".format(self.co.user))

    def init_page(self):
        self.page = DP.ChromiumPage(self.co)

    def signin(self, username, password):
        """
        not stable
        """
        self.page.get(self.login_url)
        self.page.ele('#i0116').input(username)
        self.page.ele('#idSIButton9').click()
        time.sleep(1)
        self.page.ele('#i0118').input(password)
        self.page.ele('#idSIButton9').click()
        time.sleep(3)

    def init_random_words(self):
        """
        初始化随机搜索词
        # todo! 网络请求获取随机搜索词
        """
        text = "Before fires ripped through Lahaina, the craftsman-inspired home at 271 Front St. didn’t stand out much in the neighborhood. The nearly 100-year-old structure had been lovingly restored in recent years, but it was one of many charming homes lining the waterfront of one of Hawaii’s most historically important towns.Today, the house is unmissable: A red-roofed structure in seemingly pristine condition, surrounded by piles of ash and rubble for blocks in every direction."
        words = text.split(" ")
        random.shuffle(words)
        return words

    def open_search_url(self):
        """
        打开搜索页面,用于查看创意式积分活动
        """
        self.page.get("https://cn.bing.com/search?q=t")

    def laptop_search_get_needs(self):
        """
        获取PC搜索需要的次数
        """
        self.page.get(self.reward_check_url)
        time.sleep(2)

        # 已获取的积分数
        try:

            already_get = self.page.ele(
                'xpath://*[@id="userPointsBreakdown"]/div/div[2]/div/div[1]/div/div[2]/mee-rewards-user-points-details/div/div/div/div/p[2]/b',
                timeout=0.5).text
            already_get = int(already_get)
        except ElementNotFoundError:
            already_get = 0

        # 最大可获取的积分数
        try:
            max_get = self.page.ele(
                'xpath://*[@id="userPointsBreakdown"]/div/div[2]/div/div[1]/div/div[2]/mee-rewards-user-points-details/div/div/div/div/p[2]/text()',
                timeout=0.5).replace("/", "").replace(" ", "")
            max_get = int(max_get)
        except ElementNotFoundError:
            max_get = 90

        per_get = 5 if max_get == 150 else 3
        print(already_get, max_get, sep="/")
        return (max_get - already_get) / per_get

    def pc_search_daily(self, times: int):
        """
        根据需要的次数进行PC搜索
        """
        if times > 0:
            for i in range(times):
                self.page.get(self.search_url)
                self.page.ele('#sb_form_q').input(self.words[i])
                self.page.ele('#sb_form_go').click()
                time.sleep(0.5)

        # print("每日PC搜索完成")

    def mobile_search_daily(self):
        # TODO 移动端搜索
        pass

    def solve_more_activities(self):
        self.page.get(self.reward_url)
        card_group = self.page.eles('x://*[@id="more-activities"]/div/mee-card')
        for card in card_group:
            try:
                card.ele('x://span[@class="mee-icon mee-icon-AddMedium"]', timeout=0.5)
                card.ele('x://a[@class="ds-card-sec"]').click()
                # self.page.close_tabs()
                time.sleep(1)
            except:
                pass

    def run(self):
        print("user \"{}\" Start".format(self.co.user))
        # 每日PC搜索
        times = self.laptop_search_get_needs()
        self.pc_search_daily(int(times) + 1)
        print("\tuser \"{}\" Search Done".format(self.co.user))
        # 每日移动搜索

        # 每日积分活动
        self.solve_more_activities()
        print("\tuser \"{}\" Activities Done".format(self.co.user))

    def quick_start(self, times):
        self.pc_search_daily(times)

    class Tests:
        """
        测试模块
        普通测试函数命名以test_开头
        """

        @staticmethod
        def run_tests():
            """
            由外层类的实例对象调用，执行外层类中的Tests类中的所有函数名为以test_开头的测试函数
            """
            typeName = "DailySearch.Tests"
            for i in dir(eval(typeName)):
                if i.startswith('test_'):
                    print(f"[Test] [{typeName.split('.')[0]}]: " + i)
                    eval(f"{typeName}.{i}()")

        # @staticmethod
        # def test_quiz():
        #     ds = DailySearch(False)
        #     ds.page.get(
        #         'https://cn.bing.com/search?q=Bing%20Homepage%20quiz&form=ML2BF1&OCID=ML2BF1&PUBL=RewardsDO&PROGRAMNAME=BingDailyOfferIN&CREA=ML2BF1')
        #     ds.reward_quiz()
        #     del ds

        # @staticmethod
        # def test_check_reward_ok():
        #     # TODO 测试check_reward_ok
        #     ds = DailySearch(False)
        #     print(ds.reward_check_ok_clone())
        #     print(ds.reward_check_ok())
        #     input()

        @staticmethod
        def test_test():
            print("test_example")


if __name__ == '__main__':
    # ds = DailySearch(False,"Default")
    # ds.run()
    # ds.quick_start(10)
    # time.sleep(10000)
    # del ds
    # mu = MultiUser("Default","Profile 1")
    # mu.run()
    quit()
