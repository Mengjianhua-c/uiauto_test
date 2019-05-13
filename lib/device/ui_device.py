"""
author: mengjianhua
date: 2019/5/8
"""
import uiautomator2
import json
from config.device import HEALTH_LEVEL, BATTERY_HEALTH
import time
import requests
import os
import aircv as ac
from PIL import Image
from PIL import ImageDraw
from settings import SCREENSHOT_SAVE_PATH, ICON_PATH, DEBUG
import math


class UiDevice:
    def __init__(self, device_id):
        self.driver = uiautomator2.connect(device_id)
        self._check_device_heath()

    @staticmethod
    def image_draw_lines(path, xys, fill='red', width=2):
        img = Image.open(path)
        draw = ImageDraw.Draw(img)
        for xy in xys:
            draw.line(xy, fill=fill, width=width)
        img.show()

    @staticmethod
    def move_coordinate(x, y, o=0, z_len=100):
        """o >=0, =<360"""
        if 0 <= o <= 360:
            t = [0, 90, 180, 270, 360]
            if o in t:
                if o == 0 or o == 360:
                    return x + z_len, y
                elif o == 90:
                    return x, y - z_len
                elif o == 180:
                    return x - z_len, y
                elif o == 270:
                    return x, y + z_len
            else:
                p = 180 / math.pi
                if 0 < o < 90:
                    cx = z_len * math.cos(o / p)
                    cy = z_len * math.sin(o / p)
                    return x + cx, y - cy
                elif 90 < o < 180:
                    o = 90 - (o - 90)
                    cx = z_len * math.cos(o / p)
                    cy = z_len * math.sin(o / p)
                    return x - cx, y - cy
                elif 180 < o < 270:
                    o = 90 - (o - 180)
                    cx = z_len * math.cos(o / p)
                    cy = z_len * math.sin(o / p)
                    return x - cx, y + cy

                elif 270 < o < 360:
                    o = 90 - (o - 270)
                    cx = z_len * math.cos(o / p)
                    cy = z_len * math.sin(o / p)
                    return x + cx, y + cy
        else:
            return x, y

    @staticmethod
    def _find_img_sift(icon_path, path=None, is_show=False, threshold=60):
        try:
            if DEBUG is True:
                is_show = True
            if path is None:
                path = os.path.join(SCREENSHOT_SAVE_PATH, 'screenshot.png')
            imsrc = ac.imread(path)
            imsch = ac.imread(icon_path)
            img = Image.open(path)
            result = ac.find_sift(imsrc, imsch, min_match_count=threshold)
            x = result.get('result')[0]
            y = result.get('result')[1]
            if is_show:
                draw = ImageDraw.Draw(img)
                print(result)
                res = (result.get('result')[0], result.get('result')[1], result.get('result')[0] + 1,
                       result.get('result')[1] + 1)
                draw.line(res, fill='red', width=3)
                rec = result.get('rectangle')
                draw.line((rec[0], rec[3], rec[2], rec[1], rec[0]), fill='red', width=5)
                try:
                    img.show()
                except:
                    pass
            return x, y
        except:
            return False

    def click_by_search_icon_img(self, icon_path=None, is_show=False, threshold=60):

        if os.path.exists(icon_path):
            path = os.path.join(SCREENSHOT_SAVE_PATH, 'screenshot.png')
            time.sleep(0.5)
            self.screenshot_minicap(save_path=path)
            result = self._find_img_sift(icon_path=icon_path, path=path, is_show=is_show, threshold=threshold)
            if result:
                if result[0] > 0 and result[1] > 0:
                    self.driver.click(*result)
                    print('click x:{}, y:{}'.format(*result))
                    return True
                else:
                    return False
            else:
                return False
        else:
            print('{} 不存在'.format(icon_path))
            return False

    def screenshot_adb(self, save_path=None):
        self.driver.adb_shell('screencap -p /sdcard/screenshot.png')
        if save_path is None:
            save_path = os.path.join(SCREENSHOT_SAVE_PATH, 'screenshot.png')
        self.driver.pull("/sdcard/screenshot.png", save_path)
        if DEBUG:
            print('adb screenshot {}'.format(save_path))
        time.sleep(0.2)

    def screenshot_minicap(self, minicap=False, save_path=None):
        """使用内置的uiautomator截图"""
        url = '{}?minicap={}'.format(self.driver.screenshot_uri, 'true' if minicap else 'false')
        html = requests.get(url)
        if save_path is None:
            save_path = os.path.join(SCREENSHOT_SAVE_PATH, 'screenshot.png')
        if save_path:
            with open(save_path, 'wb') as f:
                f.write(html.content)
            if DEBUG:
                print(url)
                print('save screenshot success {}'.format(save_path))
        return html.content

    def send_key(self, sleep=0.3, text=None, **kwargs):
        self.driver(**kwargs).send_keys(text)
        time.sleep(sleep)

    def click(self, sleep=0.3, **kwargs):
        try:
            self.driver(**kwargs).click()
            time.sleep(sleep)
        except Exception as e:
            print(e)

    def device_info(self):
        info = self.driver.device_info
        return info

    def _check_device_heath(self):
        info = self.device_info()
        battery = info.get('battery')
        level = battery.get('level')
        health = battery.get('health')
        print('check device status... ', end='')
        print('model: {}, version: {}, sdk: {} ---> '.format(info.get('model'),
                                                             info.get('version'),
                                                             info.get('sdk')), end='')
        if health != 2:
            raise Exception('电池状态异常，参考码：{}->{}'.format(health, BATTERY_HEALTH.get(health)))
        if level <= HEALTH_LEVEL:
            raise Exception(f'设备电池电量低于{HEALTH_LEVEL}%,禁止相关操作')
        print('device ok')
