"""
author: mengjianhua
date: 2019/5/9
"""
import os
import dotenv
from getenv import env
from cacheout import Cache


# 项目根地址
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

try:
    dotenv_path = os.path.join(PROJECT_ROOT, '.env')
    dotenv.read_dotenv(dotenv_path)
except Exception as e:
    Exception('没有读取到APP_SECRET ！')

STATIC_PATH = os.path.join(PROJECT_ROOT, 'static')
SCREENSHOT_SAVE_PATH = os.path.join(STATIC_PATH, 'screenshot')
ICON_PATH = os.path.join(STATIC_PATH, 'icon')


QUEUE_DATA = Cache()
"""
is_screen
监控是否结束： finish_watch
移动： run_watch
普攻： common_fire
技能准备： skill_watch
阵亡监控： kill_watch
jiajineng： add_skill

com.tencent.tmgp.sgame
"""
comments = [
    '......'
]

DEBUG = False

SCREEN_INTERVAL = 0.2
