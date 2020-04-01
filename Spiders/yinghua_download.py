import requests
import bs4
import os
import json

class downloadVideo():
    def __init__(self):
        # 请求头
        self.headers = {
            #'Connection': 'keep-alive',
            #'Cache-Control': 'max-age=0',
            #'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            #'Referer': 'http://www.imomoe.in/view/7599.html',
            #'Accept-Encoding': 'gzip, deflate',
            #'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            #'Cookie': 'count_h=2; count_m=2; __music_index__=2; UM_distinctid=1712bda5b907-0ab31d4ef067a7-f313f6d-100200-1712bda5b934f9; CNZZDATA1260742008=672860595-1585575238-https%253A%252F%252Fwww.baidu.com%252F%7C1585575238; first_h=1585578663312; count_h=1; first_m=1585578663316; count_m=1; __music_index__=1; Hm_lvt_38c112aee0c8dc4d8d4127bb172cc197=1585578664; bdshare_firstime=1585578663843; qike123=%u67D0%u79D1%u5B66%u7684%u8D85%u7535%u78C1%u70AET%20%u7B2C01%u96C6^http%3A//www.imomoe.in/player/7599-0-0.html_$_|; Hm_lpvt_38c112aee0c8dc4d8d4127bb172cc197=1585578693',
            #'If-None-Match': '"f66de0cdf44d61:0"',
            #'If-Modified-Since': 'Sat, 28 Mar 2020 11:34:12 GMT',
        }
        # 请求js的请求头
        self.jh = {
            'Referer': 'http://www.imomoe.in/player/7758-0-1.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        }
        #获取视频的时候的请求头
        self.vh = {
            'accept': '*/*',
            'sec-fetch-dest': 'video',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        }

    #获取网页全部内容
    def getsoup(self, url):
        self.jh["Referer"] = url
        html = requests.get(url, headers=self.headers)
        soup = bs4.BeautifulSoup(html.content.decode('gbk'), 'html.parser')
        return soup

    def get_title(self, soup):
        title = soup.find_all('title')[0].get_text()
        for each in ["/", "\\", '"', "'", "*", ">", "<", "|"]:
            title = title.replace(each, " ")
        title = title.replace("?", "？")
        title = title.replace(":", "：")
        return title

    #获取js的url
    def get_jsonurl(self, soup):
        return 'http://www.imomoe.in' + soup.find_all('div', class_="player")[0].find_all('script', type="text/javascript")[0]['src']

    def get_vurl(self, url):
        index = self.jh["Referer"].split("-")[2][:-5]
        js = requests.get(url, headers=self.jh)
        urllist = js.content.decode("unicode_escape")[18:-68].split('$')
        vurl = []
        for each in urllist:
            if '.mp4' in each:
                vurl.append(each)
        return vurl[int(index)]

    #下载保存视频
    def download(self, url, title):
        videocontent = requests.get(url, headers=self.vh).content
        with open('%s.mp4' % title, 'wb') as videofile:
            videofile.write(videocontent)
            videofile.close()

    def start(self, url):
        soup = self.getsoup(url)
        js = self.get_jsonurl(soup)
        vurl = self.get_vurl(js)
        title = self.get_title(soup)
        try:
            os.mkdir('%s' % title.split(' ', 1)[0])
        except:
            os.chdir('%s' % title.split(' ', 1)[0])
        else:
            os.chdir('%s' % title.split(' ', 1)[0])
        self.download(vurl, title)
        os.chdir('..\\')

class getList():
    def __init__(self):
        self.headers = {
            'Accept-Ranges': 'bytes',
            'Cache-Control': 'max-age=180',
            # 'Content-Encoding': 'gzip',
            # 'Content-Length': '4899',
            'Content-Type': 'text/html',
            # 'Date': 'Mon, 30 Mar 2020 16:11:01 GMT',
            # 'ETag': '"d453e8cdf44d61:0"',
            # 'Expires': 'Mon, 30 Mar 2020 16:14:01 GMT',
            # 'Last-Modified': 'Sat, 28 Mar 2020 11:34:12 GMT',
            'Server': 'NWS_Oversea_AP',
            'X-Cache-Lookup': 'Hit From MemCache Gz',
            # 'X-NWS-LOG-UUID': '2977714397790064795 c7d446ad79384de09cfbe737ae7b566c',
        }

    def get_soup(self, url):
        html = requests.get(url, headers=self.headers)
        soup = bs4.BeautifulSoup(html.content.decode('gbk'), 'html.parser')
        return soup

    def get_urllist(self, soup):
        urllist = soup.find_all(id="play_0")[0].find_all('a')
        result = []
        for each in urllist:
            result.append('http://www.imomoe.in' + each['href'])
        return result

    def start(self, url):
        soup = self.get_soup(url)
        urllist = self.get_urllist(soup)
        return urllist

def m():
    print("="*30 + '樱花动漫下载程序v1.0.0 by tonysyz' + '='*30)
    print('下载方式：\n1.下载全集\n2.下载单集\n(输入1或2)\n')
    download = downloadVideo()
    choose = input('Your Choice:')
    if choose == '2':
        print("*"*30)
        url = input('请输入网址(例如:http://www.imomoe.in/player/7599-0-1.html)\n网址：')
        download.start(url)
        print("完成下载......")
    if choose == "1":
        print("*"*30)
        getlist = getList()
        url = input('请输入网址(例如:http://www.imomoe.in/view/7599.html)\n网址：')
        urllist = getlist.start(url)
        i = 0
        for each in urllist:
            print('downloading...   %s/%s'%(str(i), len(urllist)))
            download.start(each)
            i += 1
        print("完成下载...")

if __name__ == '__main__':
    while True:
        m()