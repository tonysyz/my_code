import requests
import bs4
import os

class DownloadAlbum():
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
        self.img_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            #'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'p2.music.126.net',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }
    def gethtml(self, albumid):
        url = "https://music.163.com/album?id=%s" % albumid
        html = requests.get(url, headers=self.headers)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        return soup

    def getinfo(self, html):
        title = html.find_all('meta', property="og:title")[0]["content"]
        #print(title)
        img = html.find_all('meta', property="og:image")[0]["content"]
        #print(img)
        des = html.find_all('meta', property="og:description")[0]["content"]
        #print(des)
        return [title, img, des]

    def getsonglist(self, html):
        song = html.find_all("meta", property="music:song")
        songlist = []
        for each in song:
            songlist.append(each["content"].split("=")[-1])
        return songlist

    def songname(self, html):
        songname = html.find_all("meta", property="og:music:album:song")
        songnamelist = []
        for each in songname:
            songnamelist.append(each["content"].split(";")[0].split("=")[-1])
        return songnamelist

    def save_file(self, id_list, plist, title):
        new_file = "专辑   %s" % title
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
                    os.remove("%s.lrc" % filename)
                except FileNotFoundError:
                    signal = "歌曲  %s  歌词下载失败...(原因：未知错误)" % filename
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

    def save_img(self, imgurl, title):
        os.chdir(".\\专辑   %s" % title)
        img = requests.get(imgurl, headers=self.img_headers)
        for each in ["/", "\\", '"', "'", "*", ">", "<", "|"]:
            title = title.replace(each, " ")
        title = title.replace(":", "：")
        with open("%s.jpg" % (title), "wb") as f:
            f.write(img.content)
            f.close()
        os.chdir("..\\")

def start():
    albumid = input("您好，请输入专辑id：")
    do = DownloadAlbum()
    html = do.gethtml(albumid)
    info = do.getinfo(html)
    songlist = do.getsonglist(html)
    songnamelist = do.songname(html)
    print(info[2])
    save = do.save_file(songlist, songnamelist, info[0])
    do.save_img(info[1], info[0])
    print(save)

if __name__ == "__main__":
    start()