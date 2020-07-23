import time
import os
from datetime import datetime
import win32api, win32con

def get_left_days():
    future = datetime.strptime('2021-06-07 00:00:00', '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    delta = future - now
    return delta.days

def c():
    t = time.localtime()
    if t.tm_hour == 19 and t.tm_min in range(5):
        return True

if __name__ == '__main__':
    a = win32api.MessageBox(0, "距离高考还有{}天".format(get_left_days()), "提醒学习小助手", win32con.MB_ICONWARNING)
    while True:
        if c() == True:
            os.popen('ffplay -i https://cctvcnch5ca.v.wscdns.com/live/cctv1_2/index.m3u8 -window_title 新闻联播 -fs')
            time.sleep(1860)
            os.system('taskkill /IM ffplay.exe /f')
        else:
            time.sleep(10)