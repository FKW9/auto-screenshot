import os
from typing import List
import pyautogui


def get_screenshot_params(pictures_per_page: int):
    positions = []

    for page in range(pictures_per_page):
        print(f'----- Picture {page + 1} -----')

        coords = [(0, 0), (0, 0)]

        for j in range(2):
            try:
                while True:
                    coords[j] = pyautogui.position()
                    print(f'X{j + 1}:{str(coords[j][0]).ljust(4)} Y{j + 1}:{str(coords[j][1]).ljust(4)}', end='    \r')
            except KeyboardInterrupt:
                print(f'X{j + 1}:{str(coords[j][0]).ljust(4)} Y{j + 1}:{str(coords[j][1]).ljust(4)}')

        x1 = coords[0][0]
        y1 = coords[0][1]
        w  = coords[1][0] - x1
        h  = coords[1][1] - y1

        positions.append((x1, y1, w, h))

    return positions


def get_next_page_position():
    try:
        while True:
            pos = pyautogui.position()
            print(f'X:{str(pos[0]).ljust(4)} Y:{str(pos[1]).ljust(4)}', end='    \r')
    except KeyboardInterrupt:
        print(f'X:{str(pos[0]).ljust(4)} Y:{str(pos[1]).ljust(4)}')

    return pos[0], pos[1]


def take_screenshots(page_count: int, screenshot_params: List[tuple], next_page_pos: tuple, page_swap_delay: float=0.1):
    for page in range(page_count):
        for i, pos in enumerate(screenshot_params):
            pyautogui.screenshot(f'page{page + 1}_pic{i + 1}.png', pos)

        pyautogui.click(next_page_pos[0], next_page_pos[1])
        pyautogui.sleep(page_swap_delay)


if __name__ == '__main__':
    page_cnt = int(input('Page count:'))
    pics_cnt = int(input('Picture count:'))
    swap_del = float(input('Swap delay (s):'))

    print('='*78+'\nTo select a position, place your cursor at the right position and press CTRL+C\n'+'='*78)
    print('Select position where to click to switch the page:')
    page_pos = get_next_page_position()

    print('Select two points for each screenshot:')
    params = get_screenshot_params(pics_cnt)

    reply = input('Start capture? (Y/N)')

    if reply.lower() == 'y':
        pyautogui.sleep(0.2)
        take_screenshots(page_cnt, params, page_pos, swap_del)
        os.system(f'explorer "{os.getcwd()}"')
