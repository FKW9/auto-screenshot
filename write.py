import os
from typing import List
import pyautogui


def get_screenshot_params(pictures_per_page: int):
    """
    Return a list of tuples which describe the position and dimension of each screenshot.

    The user is asked to move the cursor to the upper left and lower right corner of each screenshot.
    From these two XY coordinates, the required tuple with (x, y, width, height) is calculated and returned for each picture.

    Because there is no method in pyautogui to listen to a mouse event, the user has to manually confirm the position by raising an
    KeyboardInterrupt, which is then caught and the position saved.

    Parameters
    ----------
    pictures_per_page : int
        How many screenshots per page

    Returns
    -------
    List[tuple]
        Parameteres required by method 'pyautogui.screenshot()'.
        Length of list is equal to param 'pictures_per_page'
    """
    positions = []

    for page in range(pictures_per_page):
        print(f'----- Picture {page + 1} -----')

        # 1st tuple: upper left corner of screenshot
        # 2nd tuple: lower right corner
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
    """
    Get the XY Coordinates of the screen where the mouse will be clicked when switching the page.

    Detailed explanation in method 'get_screenshot_params()'.

    Returns
    -------
    tuple
        xy coordinates
    """
    try:
        while True:
            pos = pyautogui.position()
            print(f'X:{str(pos[0]).ljust(4)} Y:{str(pos[1]).ljust(4)}', end='    \r')
    except KeyboardInterrupt:
        print(f'X:{str(pos[0]).ljust(4)} Y:{str(pos[1]).ljust(4)}')

    return pos[0], pos[1]


def take_screenshots(page_count: int, screenshot_params: List[tuple], next_page_pos: tuple, page_swap_delay: float=0.1):
    """
    Capture screenshots with the given paramters.

    Parameters
    ----------
    page_count : int
        how many pages to switch
    screenshot_params : List[tuple]
        List of parameters for method pyautogui.screenshot().
        Each tuple contains (x, y, width, height).
    next_page_pos : tuple
        XY coordinates where to click the mouse to switch the page
    page_swap_delay : float, optional
        delay after switching the page, by default 0.1
    """
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
