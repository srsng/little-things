import time
import DrissionPage as DP


class BackUp(object):
    def __init__(self, **kwargs):
        # self.skey = skey
        # qq群成员管理页面，需要用于登录获取cookies
        self.__url = 'https://qun.qq.com/member.html'
        # 获取qq头像的api，用qq号格式化，get
        self.__get_user_head_img = 'https://q4.qlogo.cn/g?b=qq&nk={}&s=140'
        # 获取QQ群头像的api，用群号格式化，get
        self.__get_group_head_img = 'https://p.qlogo.cn/gh/{0}/{0}/40'
        # 获取好友列表的api，post携带bkn参数
        self.__get_friend_list = 'https://qun.qq.com/cgi-bin/qun_mgr/get_friend_list'
        # 获取QQ群列表的api，post携带bkn参数
        self.__get_group_list = 'https://qun.qq.com/cgi-bin/qun_mgr/get_group_list'
        # 获取QQ群成员的api，post携带多个参数
        self.__get_group_member_list = 'https://qun.qq.com/cgi-bin/qun_mgr/search_group_members'

        # 初始化
        self.__page = DP.WebPage()

        self.__bkn = ...

        # 用户主动输入skey或bkn
        if "bkn" in kwargs:
            self.__bkn = kwargs["bkn"]
        elif "skey" in kwargs:
            self.__get_bkn(kwargs["skey"])

    def get_group_numbers(self, save_to_txt: bool = False, save_path: str = "./joined_groups.txt") -> [(str, str, str), ]:
        """
        获取所有已经加入的QQ群的群号、名称、群主QQ号，类型均为str
        :return: [(群号, 名称, 群主QQ号), ]
        """
        # 检查bkn是否已经获取并做出处理
        self.__check_bkn_getted()

        # 构建params，发送post请求
        params = {"bkn": self.__bkn}
        self.__page.post(url=self.__get_group_list, params=params)

        # 提取获取的response中的需要信息
        response_json = self.__page.response.json()
        create_groups: list = response_json['create']
        join_groups: list = response_json['join']
        manage_groups: list = response_json['manage']
        my_groups = create_groups + join_groups + manage_groups

        # 格式化结果
        result = [(str(group['gc']), group['gn'], str(group['owner'])) for group in my_groups]

        # 保存至文件
        if save_to_txt:
            self.__save_as_txt(save_path, result)

        return result

    def get_group_members(self, number, save_to_txt: bool = False, save_path: str = None):
        """
        获取number对应QQ群的所有群成员
        :return:包含dict的list，dict内容主要有uin, nick等键
        """
        # 检查bkn是否已经获取并做出处理
        self.__check_bkn_getted()

        base = 20  # 每次获取成员的规定步长
        params = {
            'gc': eval(number),
            'st': 0,
            'end': 20,
            'sort': 0,
            'bkn': self.__bkn,
        }  # 仅st与end需要增加

        mems = []  # 存储所有成员信息，存放字典的列表
        # 第一次post
        self.__page.post(url=self.__get_group_member_list, params=params)
        response_json = self.__page.response.json()
        count = response_json["count"]  # 群聊当前人数
        mems += response_json["mems"]

        if save_to_txt:
            details = "\n".join([f"{k}:{v}" for k, v in response_json.items() if k != "mems" and k != "levelname"])
            levelname = "\n".join([f"\t{k}:{v}" for k, v in response_json["levelname"].items()])
            details += "\nlevelname:\n" + levelname + "\n"

        # 计算剩余请求次数
        times = count // base

        # 请求
        for i in range(1, times + 1):
            params['st'] += base
            params['end'] += base
            self.__page.post(url=self.__get_group_member_list, params=params)
            response_json = self.__page.response.json()
            mems += response_json["mems"]

        # 保存与处理
        if save_to_txt:
            text = "\n".join([
                "QQ: " + str(info_dic["uin"]) +
                "\n\tlv: \n" + "\n".join(["\t\t{}: {}".format(k, v) for k, v in info_dic["lv"].items()]) + "\n" +
                "\n".join(["\t{}: {}".format(k, v) for k, v in info_dic.items() if k not in ["lv", "uin"]])
                for info_dic in mems
            ])

            if save_path is None:
                save_path = "./group_{}_details_and_numbers.txt".format(number)
            self.__save_as_txt(save_path, details + text)

        return mems

    def get_friend_list(self, save_to_txt: bool = False, save_path: str = "./my_friends.txt"):
        """
        获取所有好友
        :return:
        """
        # 检查bkn是否已经获取并做出处理
        self.__check_bkn_getted()

        # 构建params，发送post请求
        params = {"bkn": self.__bkn}
        self.__page.post(url=self.__get_friend_list, params=params)

        # 提取获取的response中的需要信息
        response_json = self.__page.response.json()
        friends_ddld = response_json["result"]  # ddld 指dict包含dict包含list包含dict，下同

        def dependency_dict_to_str_in_single_line(dic):
            return "  ".join([f"{k}: {v}" for k, v in dic.items()]) + "\n"

        def ld_to_str(ls):
            return "\t".join(dependency_dict_to_str_in_single_line(dic) for dic in ls)

        if save_to_txt:
            text = "\n".join(
                [
                    group_dld.get("gname", f"群组{seq}") + "\n" +  # 如果有gname，则用gname替代群组名称，否则用"群组{}"
                    f"gid: {group_dld.get('gid', 'None')}\n" +  # gid
                    "\t" + ld_to_str(group_dld["mems"])  # 具体好友
                    for seq, group_dld in friends_ddld.items()
                ]
            )
            self.__save_as_txt(save_path, text)
        return friends_ddld

    def __check_login(self):
        """
        只通过检查页面有无”登录“字样来确定
        """
        times = 0
        while self.__page.ele("登录"):
            print("请登录...")
            times += 1
            if times > 100:
                print("长时间未登录，已结束程序.")
                exit(1)
            time.sleep(3)

    def __get_skey(self):
        self.__page.get(self.__url)
        self.__check_login()

        cookies_dic = self.__page.get_cookies(as_dict=True)
        skey = cookies_dic["skey"]
        return skey

    def __get_bkn(self, skey):
        e = skey
        t = 5381
        n = 0
        o = len(e)
        while n < o:
            t += (t << 5) + ord(e[n])
            n += 1
        self.__bkn = 2147483647 & t

    def __check_bkn_getted(self):
        if self.__bkn is ...:
            self.__get_bkn(self.__get_skey())

    @staticmethod
    def __save_as_txt(save_path: str, content: 'str | [(str,)]'):
        if not save_path.endswith('.txt'):
            save_path += '.txt'

        if isinstance(content, list) and all(
                isinstance(item, tuple) and all(isinstance(sub_item, str) for sub_item in item) for item in content):
            text = "\n".join([format(tup) for tup in content])

        elif isinstance(content, str):
            text = content
        else:
            raise ValueError("content类型错误，无法解析")

        with open(save_path, 'a', encoding='utf-8') as f:
            f.write(text)
            tip_path = save_path.lstrip("./")
            print("save content to \n\t{}".format(tip_path))


if __name__ == "__main__":
    BackUp().get_friend_list(save_to_txt=True)
