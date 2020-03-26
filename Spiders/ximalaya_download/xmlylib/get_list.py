import requests
import bs4

class GetList():
    def __init__(self):
        self.url = "https://www.ximalaya.com/youshengshu/240506/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}

    def getaid(self):
        aid = input("请输入专辑id：")
        return str(aid)

    def geturl(self, aid, ty):
        return "https://www.ximalaya.com/%s/%s/" % (ty, aid)

    def gethtml(self, url):
        res = requests.get(url, headers=self.headers)
        return res

    def getinfo(self, aid, ty):
        html = requests.get("https://www.ximalaya.com/%s/%s/" % (ty, aid), headers=self.headers)
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        imgurl = "http:" + soup.find_all("img", class_="img lO_")[0]["src"].split("!")[0]
        title = soup.find_all("h1", class_="title lO_")[0].get_text()
        category = soup.find_all("a", class_="cate lO_")[0].get_text()
        time = soup.find_all("span", class_="time lO_")[0].get_text()
        listen = soup.find_all("span", class_="count lO_")[0].get_text()
        try:
            intro = soup.find_all("article", class_="intro aB_")[0].get_text()
        except IndexError:
            intro = "这个专辑莫得简介！"
        listnum = soup.find_all("h2", class_="_Qp")[0].get_text()
        return [imgurl, title, category, time, listen, intro, listnum]

    def getpage(self, html):
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        n = soup.find_all("h2", class_="_Qp")[0].get_text().split("(")[1].split(")")[0]
        n = int(n)
        page = n//30 + 1
        return page

    def getlist(self, html):
        soup = bs4.BeautifulSoup(html.text, 'html.parser')
        aulist = soup.find_all("div", class_="text _Vc")
        aulist_title = []
        for each in aulist:
            aulist_title.append(each.get_text())
        aulist_url = []
        for each in aulist:
            aulist_url.append(each.find_all("a")[0]["href"].split(r"/")[3])
        return [aulist_title, aulist_url]

    def getpages(self, aid, num, ty):
        i = 1
        pagelist = []
        for each in range(num):
            url = "https://www.ximalaya.com/%s/%s/p%s/" % (ty, aid, i)
            pagelist.append(url)
            i += 1
        return pagelist

    def get_all_list(self, aid, ty):
        url = self.geturl(aid, ty)
        html = self.gethtml(url)
        num = self.getpage(html)
        page = self.getpages(aid, num, ty)

        aulist = []
        aulist_title = []
        for each in page:
            html = self.gethtml(each)
            for each in self.getlist(html)[1]:
                aulist.append(each)
        for each in page:
            html = self.gethtml(each)
            for each in self.getlist(html)[0]:
                aulist_title.append(each)
        return [aulist, aulist_title]