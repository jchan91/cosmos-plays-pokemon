import pyautogui
import time
import random


keys = [
    'left',
    'right',
    'up',
    'down',
    'z',
    'x',
    'space'
]


if __name__ == '__main__':
    numKeys = len(keys)

    while True:
        time.sleep(0.5)

        random_index = random.randint(0, numKeys - 1)
        # print('Rand Index: {0}'.format(random_index))

        key = keys[random_index]

        print('Selected key: {0}'.format(key))

        pyautogui.press(key)

