import requests
import bs4
import json
'''
https://music.163.com/song?id=1342950406
'''

class GetSong():
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
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
    def songurl(self, songid):
        return "https://music.163.com/song?id=%s" % songid

    def gethtml(self, url):
        html = requests.get(url, headers=self.headers)
        soup = bs4.BeautifulSoup(html.text, "html.parser")
        return soup

    def getinfo(self, soup):
        info = soup.find_all("script", type="application/ld+json")
        j = info[0].get_text()
        j = json.loads(j)
        title = j["title"]
        images = j["images"]
        des = j["description"]
        return {
            "title": title,
            "images": images,
            "des":des,
        }

    def get_singer(self, soup):
        soup.find_all("a", _class="s-fc7")
        singer = soup.find_all("p")
        for each in singer:
            if '歌手' in each.text:
                singer = each
        return singer.find_all("span")[0]["title"]


    def get_image(self, url):
        img = requests.get(url, headers=self.img_headers)
        return img

    def getsong(self, songid):
        mp3url = "http://music.163.com/song/media/outer/url?id=%s.mp3" % songid
        mp3 = requests.get(mp3url, headers=self.headers)
        return mp3

    def get_lrc(self, songid):
        lyrcs = "http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1" % songid
        lrc = requests.get(lyrcs ,headers=self.headers).json()
        return lrc["lrc"]["lyric"]

    def savefile(self, content, ty, title, singer):
        for each in ["/", "\\", '"', "'", "*", ">", "<", "|"]:
            title = title.replace(each, " ")
            singer = singer.replace(each, " ")
        title = title.replace(":", "：")
        title = title.replace("?", "？")
        singer = title.replace("?", "？")
        singer = singer.replace(":", "：")
        if ty == "song":
            with open("%s  %s.mp3" % (singer, title), "wb") as f:
                f.write(content)
                f.close()
        if ty == "img":
            with open("%s  %s.jpg" % (singer, title), "wb") as f:
                f.write(content)
                f.close()
        if ty == "lrc":
            with open("%s  %s.lrc" % (singer, title), "w") as f:
                f.write(content)
                f.close()

def start(songid):
    get = GetSong()
    url = get.songurl(songid)
    soup = get.gethtml(url)
    info = get.getinfo(soup)
    mp3 = get.getsong(songid)
    singer = get.get_singer(soup)
    get.savefile(mp3.content, 'song', info["title"], singer)
    img = get.get_image(info["images"][0])
    get.savefile(img.content, 'img', info["title"], singer)
    lrc = get.get_lrc(songid)
    get.savefile(lrc, 'lrc', info["title"], singer)

if __name__ == "__main__":
    while True:
        songid = input('songid:')
        start(songid)