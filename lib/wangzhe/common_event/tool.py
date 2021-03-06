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
        executor.submit(self.drag_thread)
        print('create click thread')
        executor.submit(self.click_thread)
        print('create add skill thread')
        executor.submit(self.add_skill_thread)

    @staticmethod
    def create_queue():
        # 截屏控制参数
        QUEUE_DATA.set('is_screen', False)
        QUEUE_DATA.set('is_screen_exit', False)
        # 移动控制参数
        QUEUE_DATA.set('move_idx', None)

        # 拖动参数
        QUEUE_DATA.set('is_drag', False)
        QUEUE_DATA.set('is_drag_exit', False)
        QUEUE_DATA.set('drag_cos', (0, 1))
        QUEUE_DATA.set('drag_idx', ())

        # 点击屏幕控制参数
        QUEUE_DATA.set('is_click_exit', False)
        QUEUE_DATA.set('click_idx', ())
        QUEUE_DATA.set('is_click', False)
        QUEUE_DATA.set('is_always_ckick', False)

        # 加技能参数
        QUEUE_DATA.set('is_add_skill_exit', False)

        # 通用坐标
        QUEUE_DATA.set('common_fire_idx', ())
        QUEUE_DATA.set('baili_skill', [])

    @staticmethod
    def screen_event(is_screen=False, is_exit=False):
        QUEUE_DATA.set('is_screen', is_screen)
        QUEUE_DATA.set('is_screen_exit', is_exit)

    @staticmethod
    def drag_event(drag_idx=(0, 0), angel=0, length=0, is_exit=False):
        QUEUE_DATA.set('drag_idx', drag_idx)
        QUEUE_DATA.set('is_drag_exit', is_exit)
        QUEUE_DATA.set('is_drag', True)
        QUEUE_DATA.set('drag_cos', (angel, length))
        time.sleep(length)
        QUEUE_DATA.set('is_drag', False)

    @staticmethod
    def click_event(x=None, y=None, is_exit=False):
        QUEUE_DATA.set('is_click_exit', is_exit)
        QUEUE_DATA.set('is_click', True)
        QUEUE_DATA.set('click_idx', (x, y))
        time.sleep(0.5)
        QUEUE_DATA.set('is_click', False)

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

    def find_init_idx(self):
        self.d.screenshot_minicap()
        movie_idx = self.d._find_img_sift(WzPath.move_idx, threshold=10)
        common_fire_idx = self.d._find_img_sift(WzPath.common_fire_idx, threshold=5)
        skill_1 = self.d._find_img_sift(WzPath.baili_skill_1)
        skill_2 = self.d._find_img_sift(WzPath.baili_skill_2)
        skill_3 = self.d._find_img_sift(WzPath.baili_skill_3)
        if movie_idx and common_fire_idx:
            QUEUE_DATA.set('common_fire_idx', common_fire_idx)
            QUEUE_DATA.set('move_idx', movie_idx)
            QUEUE_DATA.set('baili_skill', [skill_1, skill_2, skill_3])

            return True
        return False

    def click_thread(self):
        while True:
            if QUEUE_DATA.get('is_click_exit'):
                print('exit click thread')
                break
            if QUEUE_DATA.get('is_click'):
                xy = QUEUE_DATA.get('click_idx')
                print('click: {}'.format(xy))
                self.d.driver.click(*xy)
            time.sleep(0.1)

    def drag_thread(self):
        while True:
            if QUEUE_DATA.get('is_drag_exit'):
                print('exit drag thread')
                break
            if QUEUE_DATA.get('is_drag'):
                bxy = QUEUE_DATA.get('drag_idx')
                c, t = QUEUE_DATA.get('drag_cos')
                toxy = self.d.move_coordinate(*bxy, c)
                print('drag: {} -> {}'.format(bxy, toxy))
                self.d.driver.touch.down(*bxy)
                time.sleep(0.01)
                self.d.driver.touch.move(*toxy)

                time.sleep(t)
                self.d.driver.touch.up()
            time.sleep(0.2)

    def add_skill_thread(self):
        while True:
            time.sleep(5)
            if QUEUE_DATA.get('is_add_skill_exit'):
                print('exit add skill thread')
                break
            all_skill = self.d._find_all_img_sift(WzPath.add_skill_button, threshold=4)
            if all_skill:
                skill_idx = all_skill[-1].get('result')
                print('add skill')
                self.click_event(*skill_idx)


    def run(self):
        self.init_thread()
        if self.find_init_idx():
            w.screen_event(is_screen=True)
            w.drag_event(QUEUE_DATA.get('baili_skill')[1], 320, 3)

            time.sleep(2)
            # w.drag_event(90, 3)
            # w.click_event(*QUEUE_DATA.get('common_fire_idx'))
            time.sleep(2)

        else:
            print('获取基坐标失败')
        w.click_event(is_exit=True)
        w.screen_event(is_exit=True)
        w.drag_event(is_exit=True)
        QUEUE_DATA.set('is_add_skill_exit', True)


if __name__ == '__main__':
    w = WangZhe('3EP0218B06001724')
    # w.d.screenshot_adb()
    # w.run()
    # w.close_dialog()
    w.add_skill_thread()
