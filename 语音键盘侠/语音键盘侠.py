import threading
import keyboard
from playsound import playsound


def press(x):
    """
    :param x: 上一次按压的键的提示信息，来自keyboard中的类型
    """
    global pressed
    global hot_words
    global sound_path
    global module
    last_press = ''

    def get_press(pressed):
        nonlocal last_press
        nonlocal x
        x = str(x)[14:-1]
        if x[-1] == 'n':
            last_press = x[:-5]
            pressed.append(last_press)

    get_press(pressed)

    for k in range(len(hot_words)):
        if last_press == hot_words[k][-1] and pressed[-len(hot_words[k]):-1] == list(hot_words[k][:-1]):
            threading.Thread(target=playsound, args=(sound_path[k],)).start()


def load_cmds(hot_words,sound_path):
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


if __name__ == "__main__":
    module = False
    hot_words = []
    sound_path = []
    pressed = []
    load_cmds(hot_words,sound_path)
    keyboard.hook(press)
    keyboard.wait()
