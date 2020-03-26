import requests
import bs4
import os


'''
链接格式

mp3 = "http://music.163.com/song/media/outer/url?id=%s.mp3" % id
lyrcs = "http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1" % id
'''
class Download():
    def __init__(self):     
        self.h1 = {
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

    def download_list(self, listid):
        playlist = requests.get("https://music.163.com/playlist?id=%s"%listid, headers=self.h1)
        soup = bs4.BeautifulSoup(playlist.text, 'html.parser')
        title = soup.find_all("h2")
        title = title[0].get_text()
        try:
            des = soup.find_all("p", id="album-desc-more")[0].get_text()
        except IndexError:
            des = "莫得简介！"
        num = soup.find_all("span", id="playlist-track-count")[0].get_text()

        l = soup.find_all("a")
        b = []
        for each in l:
            if '/song?id=' in str(each):
                b.append(each)
        
        for i in range(5):
            for each in b:
                c = each
                if r"${" in str(c):
                    b.remove(each)
        
        plist = []
        for each in b:
            plist.append(each.get_text())
            
        id_list = []
        for each in b:
            id_ = each["href"].split("=")[-1]
            id_list.append(id_)

        for each in ["/", "\\", '"', "'", "*", ">", "<", "|"]:
            title = title.replace(each, " ")
        title = title.replace(each, "：")
        return [plist, id_list, des, num, title]


    def save_file(self, id_list, plist, title):
        new_file = "歌单   %s" % title
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
            filename = filename.replace("?", "？")
            filename = filename.replace(":", "：")
            url = "http://music.163.com/song/media/outer/url?id=%s.mp3" % id_list[i]
            music = requests.get(url, headers=self.h1).content
            with open("%s.mp3" % filename, "wb+") as f:
                f.write(music)
                f.close()
        
            url_lrc = "http://music.163.com/api/song/lyric?os=osx&id=%s&lv=-1&kv=-1&tv=-1" % id_list[i]
            lrc = requests.get(url_lrc, headers=self.h1).json()

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
            except OSError:
                signal = "歌曲  %s  歌词下载失败...(原因：程序不支持特殊字符)" % filename
            print("\n")
            print(signal)
        os.chdir("..\\")
        return "Finished......"

def start():
    d = Download()
    listid = input("您好，欢迎使用，请输入歌单id:")
    l = d.download_list(listid)
    plist = l[0]
    id_list = l[1]
    des = l[2]
    num = l[3]
    print("*"*20)
    print(l[4])
    print("*"*20)
    print("\n简介：%s\n" % des)
    print("*"*20)
    print("总共下载：%s首歌曲......" % num)
    print("*"*20)
    print("序号\t歌曲名称")
    print("-"*40)
    for each in range(len(plist)):
        print(str(each) + "\t" + plist[each])
    print("*"*20)
    print("Downloading......")
    end = d.save_file(id_list, plist, l[4])
    print("*"*20)
    print(end)
    
if __name__ == "__main__":
    while True:
        start()
