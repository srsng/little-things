import keyboard
import threading
from playsound import playsound


def get_press(x):
    x = str(x)[14:-1]
    if x[-1] == 'p':
        pass
    else:
        x = x[:-5]
        return x


def press(x):
    """

    :param x: 上一次按压的键的提示信息，来自keyboard中的类型
    :return:
    """
    global pressed
    global module
    global hot_words
    global sound_path
    last_press = get_press(x)

    if last_press is not None:
        pressed.append(last_press)
        length = len(hot_words)
        for k in range(length):
            if last_press == hot_words[k][-1] and pressed[-len(hot_words[k]):-1] == list(hot_words[k][:-1]):
                threading.Thread(target=playsound, args=(sound_path[k],)).start()


if __name__ == "__main__":
    module = False
    hot_words = []
    sound_path = []
    pressed = []
    with open(r"load_cmds.txt", 'r', encoding='utf-8') as f:
        ls = f.readlines()
    cnt = 0
    for i in ls:
        i = i.replace("\n", "")
        if cnt % 2 == 0:
            hot_words.append(i)
            cnt += 1
        else:
            sound_path.append(i)
            cnt += 1

    keyboard.hook(press)
    keyboard.wait()
