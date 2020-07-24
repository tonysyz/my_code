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

def o_summer():
    t = time.localtime()
    if t.tm_hour == 14 and t.tm_min in range(45,47):
        return True

def o_winter():
    t = time.localtime()
    if t.tm_hour == 14 and t.tm_min in range(45,47):
        return True

def get_last_watched_time():
    with open('runtime.log', 'r') as f:
        return int(f.readlines()[-1])

def zel():
    os.popen('ffplay -i ".\(0.125)ハセガワダイスケ,菅野祐悟 - 杜王町Radio.flac" -t 6 -autoexit -nodisp')
    t = get_last_watched_time()
    if t <= 3600:
        r = os.popen('ffplay -i 周恩来的四个昼夜.TS -ss {}:{}:{} -t 720 -fs -window_title 砸瓦鲁多 -autoexit'.format(int(t/3600), int(t/60), t%60))
    if t >= 3600:
        r = os.popen('ffplay -i 周恩来的四个昼夜.TS -ss {}:{}:{} -t 720 -fs -window_title 砸瓦鲁多 -autoexit'.format(int(t/3600), int(t/60)-60, t%60))
    time.sleep(720)
    os.system('taskkill /IM ffplay.exe /f')
    with open('runtime.log', 'a') as f:
        f.write('{}\n'.format(t+720))
        f.close()

# ffmpeg -i "ハセガワダイスケ,菅野祐悟 - 杜王町Radio.flac" -filter:a "volume=0.5" output.flac

if __name__ == '__main__':
    a = win32api.MessageBox(0, "距离高考还有{}天".format(get_left_days()), "提醒学习小助手", win32con.MB_ICONWARNING)
    while True:
        if c() == True:
            os.popen('ffplay -i ".\(0.125)ハセガワダイスケ,菅野祐悟 - 杜王町Radio.flac" -t 6 -autoexit -nodisp -window_title 杜王町Radio')
            os.popen('ffplay -i https://cctvcnch5ca.v.wscdns.com/live/cctv1_2/index.m3u8 -window_title 杜王町Radio -fs')
            time.sleep(1860)
            os.popen('taskkill /IM ffplay.exe /f')
        elif o_summer() == True:
            zel()
        else:
            time.sleep(10)