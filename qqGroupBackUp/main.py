import BackUp


if __name__ == '__main__':
    # 初始化 可以手动输入或bkn、skey，减少运行流程
    bc = BackUp.BackUp()

    # 保存好友列表
    bc.get_friend_list(save_to_txt=True)

    # 保存加入了的群
    groups = bc.get_group_numbers(save_to_txt=True)

    # 保存first_group_number的群基本资料与所有成员的基本资料
    first_group_number = groups[0][0]
    bc.get_group_members(first_group_number, save_to_txt=True)
