"""
author: mengjianhua
date: 2019/5/9
"""
from settings import SCREENSHOT_SAVE_PATH, ICON_PATH
import os
from lib.device.ui_device import UiDevice
from config.wangzhe_button_path import WzPath

if __name__ == '__main__':
    # driver = UiDevice('3EP0218B06001724')
    icon_path = os.path.join(ICON_PATH, 'channel_icon.png')
    # driver.driver.app_start('tv.danmaku.bili')

    # driver.click_by_search_icon_img(icon_path)
    # path = os.path.join(SCREENSHOT_SAVE_PATH, 'screenshot.png')
    path = os.path.join(SCREENSHOT_SAVE_PATH, 'st6.png')

    xy = UiDevice._find_img_sift(WzPath.move_idx, path, threshold=3)
    print(xy)
    xys = []
    for idx in range(1, 30):
        o = idx*5
        z = UiDevice.move_coordinate(*xy, o)
        c = (xy[0], xy[1], z[0], z[1])
        xys.append(c)

    UiDevice.image_draw_lines(path, xys)
