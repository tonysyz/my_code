import requests
import bs4
import os
import json

import musiclib.album as album
import musiclib.music_list as ml
import musiclib.rank as rank
import musiclib.song as song

if __name__ == "__main__":
    while True:
        print("**"*30)
        print("网易云音乐下载程序v2.0.0 by @tonysyz")
        print("**"*30)
        print("请勿在下载过程中切换网络或代理，保持网络畅通！")
        print("注意：本程序仅支持网页未登录状态在线可以播放的音乐的相关下载，如果下载目录中存在版权歌曲(程序将会自动报错崩溃)，请自行抓包下载或者购买！\n歌单下载歌曲时：只会下载前1000首歌曲!\n祝您使用愉快")
        print("======"*12)
        print("---1.下载歌曲\n---2.下载歌单\n---3.下载专辑\n---4.下载排行榜\n")
        choice = input("请选择序号：")
        if choice == "1":
            print("-"*20)
            songid = input("请输入歌曲id：")
            song.start(songid)
        
        if choice == "2":
            print("-"*20)
            ml.start()

        if choice == "3":
            print("-"*20)
            album.start()

        if choice == "4":
            print("-"*20)
            rank.start()
