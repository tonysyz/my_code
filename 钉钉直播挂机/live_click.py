import pymouse
import os
import random
import time
from PIL import ImageGrab

# color rgb(255, 148, 62) 正在直播
# 237 241 244 直播窗口色
class Live:

    def getScreenShot(self):
        return ImageGrab.grab()

    def get_mouse(self):
        return pymouse.PyMouse()

    def findButton(self, img):
        buttun_pixel = []
        for each in range(img.size[0]):
            for each_ in range(img.size[1]):
                if img.load()[each, each_] == (255, 148, 62):
                    buttun_pixel.append([each, each_])
        return buttun_pixel

    def get_in_live(self, buttun_pixel, mouse):
        print('entering live......')
        for i in range(2):
            mouse.click(buttun_pixel[random.randint(0, len(buttun_pixel)-1)][0], buttun_pixel[random.randint(0, len(buttun_pixel)-1)][1])

    def like(self, img, mouse, times):
        print('upload %s like(s)'%times)
        mouse.move(int(img.size[0]*0.5), int(img.size[1]*0.5))
        time.sleep(0.8)
        img = ImageGrab.grab()
        img0 = img.load()
        like = []
        for each in range(img.size[0]):
            for each_ in range(img.size[1]):
                if img0[each, each_] == (67, 132, 251):
                    like.append([each, each_])
        pixel = like[int(len(like)*0.75)]
        time.sleep(1)
        if times != -1:
            for i in range(times):
                time.sleep(0.2)
                mouse.click(pixel[0], pixel[1]+35)
        if times == -1:
            while True:
                time.sleep(0.2)
                mouse.click(pixel[0], pixel[1]+35)

    def exit_live(self, mouse):
        # 0 137 255
        img = ImageGrab.grab()
        img0 = img.load()
        exit0 = []
        result = False
        for each in range(img.size[0]):
            for each_ in range(img.size[1]):
                if img0[each, each_] == (203, 173, 161):
                    exit0.append([each, each_])
                    result = True
        if result == True:
            pixel = exit0[int(len(exit0)*0.6)]
            for i in range(1000):
                mouse.click(pixel[0], pixel[1])
            time.sleep(0.3)
            print("exit live......")
            return True
        else:
            return False
if __name__ == '__main__':
    title = """
钉钉直播挂机助手 by @tonysyz
钉钉直播挂机是怎么回事呢，钉钉直播挂机相信大家都很清楚，但是直播挂机是怎么回事呢？今天就让小编。。。咳咳
废话少说，开始挂机...
注意：程序使用过程中请保持钉钉主页面在最上层！
"""
    live = Live()
    print(title)
    while True:
        try:
            mouse = live.get_mouse()
            img = live.getScreenShot()
            buttun_pixel = live.findButton(img)
        except ValueError:
            continue
        try:
            live.get_in_live(buttun_pixel, mouse)
        except ValueError:
            print("还没有检测到直播！请稍后再试...")
            continue
        else:
            print("成功进入直播间")
        time.sleep(1)
        # live.like(img, mouse, 10)
        while True:
            r = live.exit_live(mouse)
            if r == True:
                break

