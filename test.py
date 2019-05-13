"""
author: mengjianhua
date: 2019/5/7
"""
from lib.device.ui_device import UiDevice
import time


def twitter_av_play_coin():
    device = UiDevice('3EP0218B06001724')
    # print(device.device_info())
    # device.driver.unlock()
    device.driver.app_start('tv.danmaku.bili')
    device.driver(resourceId="tv.danmaku.bili:id/tab_icon", className="android.widget.ImageView", instance=2).click()
    device.driver(resourceId="tv.danmaku.bili:id/tab_title").click()
    device.click(resourceId="tv.danmaku.bili:id/video_cover_blur")
    device.driver(resourceId="tv.danmaku.bili:id/coin_icon").click()
    if device.driver(resourceId="tv.danmaku.bili:id/left").exists():
        device.click(resourceId="tv.danmaku.bili:id/left")
    device.click(resourceId="tv.danmaku.bili:id/pay_coins")
    time.sleep(3)
    device.driver.app_stop('tv.danmaku.bili')


if __name__ == '__main__':
    # twitter_av_play_coin()
    print(UiDevice('3EP0218B06001724').driver.screenshot_uri)
    from config.wangzhe_button_path import WzPath

    print(WzPath.login_button)
