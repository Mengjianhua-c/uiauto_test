"""
author: mengjianhua
date: 2019/5/10
"""

from settings import SCREENSHOT_SAVE_PATH, ICON_PATH
import os
from lib.device.ui_device import UiDevice
from config.wangzhe_button_path import WzPath
import time
from settings import QUEUE_DATA, SCREEN_INTERVAL
from concurrent.futures import ThreadPoolExecutor


class WangZhe:
    def __init__(self, device_id):
        self.d = UiDevice(device_id)
        self._open()
        self.create_queue()

    def _open(self):
        self.d.driver.app_start('com.tencent.tmgp.sgame')

    def init_thread(self):
        executor = ThreadPoolExecutor(10)
        print('create screen thread')
        executor.submit(self.screen_executor)
        print('create move thread')
        executor.submit(self.move_thread)

    @staticmethod
    def create_queue():
        # 截屏控制参数
        QUEUE_DATA.set('is_screen', False)
        QUEUE_DATA.set('is_screen_exit', False)
        # 移动控制参数
        QUEUE_DATA.set('is_move', False)
        QUEUE_DATA.set('is_move_exit', False)
        QUEUE_DATA.set('move_cos', (0, 1))
        QUEUE_DATA.set('move_idx', None)
        print('init {}'.format(QUEUE_DATA))

    @staticmethod
    def screen_event(is_screen=False, is_exit=False):
        QUEUE_DATA.set('is_screen', is_screen)
        QUEUE_DATA.set('is_screen_exit', is_exit)

    @staticmethod
    def move_event(angel=0, length=0, is_exit=False):
        QUEUE_DATA.set('is_move_exit', is_exit)
        QUEUE_DATA.set('is_move', True)
        QUEUE_DATA.set('move_cos', (angel, length))
        time.sleep(length)
        QUEUE_DATA.set('is_move', False)

    def screen_executor(self):

        while True:
            if QUEUE_DATA.get('is_screen_exit'):
                print('exit screen thread')
                break
            if QUEUE_DATA.get('is_screen'):
                self.d.screenshot_minicap()
                print('screen')
            time.sleep(SCREEN_INTERVAL)

    def login_event(self):
        time.sleep(5)
        while True:
            print('login event')
            time.sleep(1)
            self.d.screenshot_minicap()
            st = self.d.click_by_search_icon_img(WzPath.login_button, is_show=True)
            if st:
                break
        time.sleep(5)

    def close_dialog(self):
        for idx in range(6):
            time.sleep(1)
            st = self.d.click_by_search_icon_img(WzPath.close_button, is_show=True, threshold=20)
            if st is not True:
                print('close ok')
                break
        for idx in range(3):
            time.sleep(1)
            st = self.d.click_by_search_icon_img(WzPath.close_live_button, is_show=True)
            if st is not True:
                print('close live ok')
                break

    def find_move_idx(self):
        self.d.screenshot_minicap()
        xy = self.d._find_img_sift(WzPath.move_idx, threshold=5)
        if xy:
            QUEUE_DATA.set('move_idx', xy)
            return True
        return False

    def move_thread(self):
        while True:
            if QUEUE_DATA.get('is_move_exit'):
                break
            if QUEUE_DATA.get('is_move'):
                bxy = QUEUE_DATA.get('move_idx')
                c, t = QUEUE_DATA.get('move_cos')
                toxy = self.d.move_coordinate(*bxy, c)
                print('drag: {} -> {}'.format(bxy, toxy))
                self.d.driver.touch.down(*bxy)
                time.sleep(0.01)
                self.d.driver.touch.move(*toxy)

                time.sleep(t)
                self.d.driver.touch.up()
            else:
                print('wait move event')
            time.sleep(0.2)

    def run(self):
        self.init_thread()
        if self.find_move_idx():
            w.screen_event(is_screen=True)
            w.move_event(210, 3)
            w.move_event(90, 3)

        else:
            print('获取移动盘基坐标失败')
        w.screen_event(is_exit=True)
        w.move_event(is_exit=True)


if __name__ == '__main__':
    w = WangZhe('3EP0218B06001724')
    # w.d.screenshot_adb()
    w.run()
    # w.close_dialog()
