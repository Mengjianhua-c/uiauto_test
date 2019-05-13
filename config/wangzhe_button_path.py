"""
author: mengjianhua
date: 2019/5/10
"""
from settings import ICON_PATH
import os

wangzhe_path = os.path.join(ICON_PATH, 'wangzhe')


def mk_icon_path(filename):
    return os.path.join(wangzhe_path, filename)


class WzPath:
    login_button = mk_icon_path('login_button.png')
    close_button = mk_icon_path('close_button.png')
    battle_button = mk_icon_path('battle_button.png')
    arena_button = mk_icon_path('arena_button.png')
    vs5_button = mk_icon_path('5vs5_button.png')
    add_skill_button = mk_icon_path('add_skill_button.png')
    baili_skill_1 = mk_icon_path('baili_skill_1.png')
    baili_skill_2 = mk_icon_path('baili_skill_2.png')
    baili_skill_3 = mk_icon_path('baili_skill_3.png')
    black_hall = mk_icon_path('black_hall.png')
    black_home = mk_icon_path('black_home.png')
    common_fire_idx = mk_icon_path('common_fire_idx.png')
    comment_button = mk_icon_path('comment_button.png')
    device_1 = mk_icon_path('device_1.png')
    device_2 = mk_icon_path('device_2.png')
    device_3 = mk_icon_path('device_3.png')
    device_4 = mk_icon_path('device_4.png')
    device_5 = mk_icon_path('device_5.png')
    device_6 = mk_icon_path('device_6.png')
    enemy_idx = mk_icon_path('enemy_idx.png')
    go_home_button = mk_icon_path('go_home_button.png')
    hero_baili = mk_icon_path('hero_baili.png')
    mini_enemy_idx = mk_icon_path('mini_enemy_idx.png')
    move_idx = mk_icon_path('move_idx.png')
    over_button = mk_icon_path('over_button.png')
    owner_idx = mk_icon_path('owner_idx.png')
    quck_move_button = mk_icon_path('quck_move_button.png')
    start_button = mk_icon_path('start_button.png')
    yes_button = mk_icon_path('yes_button.png')
    close_live_button = mk_icon_path('close_live_button.png')


