import requests
import bs4
import os

class DownloadRank():
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            #'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'referer': 'https://music.163.com/',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
        self.url = "https://music.163.com/discover/toplist?id="
        self.rankdict = {
            '云音乐飙升榜': '19723756',
            '云音乐新歌榜': '3779629',
            '网易原创歌曲榜': '2884035',
            '云音乐热歌榜': '3778678',
            '云音乐说唱榜': '991319590',
            '云音乐古典音乐榜': '71384707',
            '云音乐电音榜': '1978921795',
            '抖音排行榜': '2250011882',
            '新声榜': '2617766278',
            '云音乐ACG音乐榜': '71385702',
            '云音乐韩语榜': '745956260',
            '云音乐国电榜': '10520166',
            '英国Q杂志中文版周榜': '2023401535',
            '电竞音乐榜': '2006508653',
            'UK排行榜周榜': '180106',
            '美国Billboard周榜': '60198',
            'Beatport全球电子舞曲榜': '3812895',
            'KTV唛榜': '21845217',
            'iTunes榜': '11641012',
            '日本Oricon周榜': '60131',
            'Hit FM Top榜': '120001',
            '台湾Hito排行榜': '112463',
            '云音乐欧美热歌榜': '2809513713',
            '云音乐欧美新歌榜': '2809577409',
            '法国 NRJ Vos Hits 周榜': '27135204',
            '中国新乡村音乐排行榜': '3112516681',
        }
        self.choose = """
1.云音乐飙升榜
2.云音乐新歌榜
3.网易原创歌曲榜
4.云音乐热歌榜
5.云音乐说唱榜
6.云音乐古典音乐榜
7.云音乐电音榜
8.抖音排行榜
9.新声榜
10.云音乐ACG音乐榜
11.云音乐韩语榜
12.云音乐国电榜
13.英国Q杂志中文版周榜
14.电竞音乐榜
16.美国Billboard周榜
17.Beatport全球电子舞曲榜
18.KTV唛榜
19.iTunes榜
20.日本Oricon周榜
21.Hit FM Top榜
22.台湾Hito排行榜
23.云音乐欧美热歌榜
24.云音乐欧美新歌榜
25.法国 NRJ Vos Hits 周榜
26.中国新乡村音乐排行榜
请输入序号："""
        self.choosenum = {
            '1': '云音乐飙升榜',
            '2': '云音乐新歌榜',
            '3': '网易原创歌曲榜',
            '4': '云音乐热歌榜',
            '5': '云音乐说唱榜',
            '6': '云音乐古典音乐榜',
            '7': '云音乐电音榜',
            '8': '抖音排行榜',
            '9': '新声榜',
            '10': '云音乐ACG音乐榜',
            '11': '云音乐韩语榜',
            '12': '云音乐国电榜',
            '13': '英国Q杂志中文版周榜',
            '14': '电竞音乐榜',
            '15': 'UK排行榜周榜',
            '16': '美国Billboard周榜',
            '17': 'Beatport全球电子舞曲榜',
            '18': 'KTV唛榜',
            '19': 'iTunes榜',
            '20': '日本Oricon周榜',
            '21': 'Hit FM Top榜',
            '22': '台湾Hito排行榜',
            '23': '云音乐欧美热歌榜',
            '24': '云音乐欧美新歌榜',
            '25': '法国 NRJ Vos Hits 周榜',
            '26': '中国新乡村音乐排行榜',
        }


    def getid(self):
        choose = self.choose
        c = input(choose)
        try:
            num = self.choosenum[c]
        except:
            print("Error")
        return self.rankdict[num]

    def gethtml(self, rankid):
        self.url += rankid
        html = requests.get(self.url, headers=self.headers)
        return html

    def get_songlist(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        songlist = soup.find_all("ul", class_="f-hide")
        songlist = songlist[0]
        songlist = songlist.contents
        slist = []
        for each in songlist:
            slist.append(each.get_text())
        idlist = []
        for each in songlist:
            idlist.append(each.find_all("a")[0]["href"].split("=")[-1])
        return [slist, idlist]

    def save_file(self, id_list, plist, title):
        new_file = "排行榜   %s" % title
        try:
            os.mkdir(new_file)
        except FileExistsError:
            os.chdir(".\\%s" % new_file)
        else:
            os.chdir(".\\%s" % new_file)
        for i in range(len(id_list)):
            filename = plist[i]
            for each in ["/", "\\", '"', "'", "*", ">", "<", "|"]:
                filename = filename.replace(each, " ")
            title = title.replace(":", "：")
            title = title.replace("?", "？")
            url = "http://music.163.com/song/media/outer/url?id=%s.mp3" % id_list[i]
            music = requests.get(url, headers=self.headers).content
            with open("%s.mp3" % filename, "wb+") as f:
                f.write(music)
                f.close()
        
            url_lrc = "http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1" % id_list[i]
            lrc = requests.get(url_lrc, headers=self.headers).json()
            
            try:
                content = lrc["lrc"]["lyric"]
                with open("%s.lrc" % filename, "w+") as lrc_f:
                    lrc_f.write(content)
                    lrc_f.close()
                signal = "歌曲  %s  已经完成下载..." % filename
            except KeyError:
                try:
                    content = lrc["lrc"]["tlyric"]
                    with open("%s.lrc" % filename, "w+") as lrc_f:
                        lrc_f.write(content)
                        lrc_f.close()
                    signal = "歌曲  %s  已经完成下载..." % filename
                except:
                    signal = "歌曲  %s  歌词下载失败...(原因：未知错误)" % filename
                else:
                    signal = "歌曲  %s  歌词下载失败...(原因：未知错误)" % filename
            except UnicodeEncodeError:
                try:
                    os.remove("%s.lrc" % filename)
                    signal = "歌曲  %s  歌词下载失败...(原因：程序不支持特殊字符)" % filename
                except FileNotFoundError:
                    signal = "歌曲  %s  歌词下载失败...(原因：程序不支持特殊字符)" % filename
            print("\n")
            print(signal)
        os.chdir("..\\")
        return "Finished......"

    def get_title(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        title = soup.find_all("h2", class_="f-ff2")
        title = title[0].get_text()
        time = soup.find_all("div", class_="user f-cb")
        time = time[0].get_text()
        return [title, time]


def start():
    print("="*30)
    print("网易云音乐歌单下载工具v1.0.0\nby @emat")
    print("="*30)
    get = DownloadRank()
    rankid = get.getid()
    text = get.gethtml(rankid).text
    title = get.get_title(text)
    info = title[1]
    title = info.split("：")[-1].split("（")[0] + get.get_title(text)[0]
    songlist = get.get_songlist(text)
    slist = songlist[0]
    idlist = songlist[1]
    a = get.save_file(idlist, slist, title)
    print("\n"+ "*"*30 +"\n排行榜下载完成，\n排行榜更新信息如下%s" % info)

if __name__ == '__main__':
    while True:
        start()