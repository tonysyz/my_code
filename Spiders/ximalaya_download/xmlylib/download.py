import requests
import os

class Download():
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}

    def make_file(self, title):
        for each in ["/", "\\", '"', "'", "*", ">", "<", "|"]:
                title = title.replace(each, " ")
        title = title.replace("?", "？")
        title = title.replace(":", "：")
        try:
            os.mkdir("专辑 %s" % title)
        except:
            os.chdir(".\专辑 %s" % title)
        else:
            os.chdir(".\专辑 %s" % title)

    def download(self, url):
        m4a = requests.get(url, self.headers)
        return m4a.content

    def save_file(self, m4a, name):
        for each in ["/", "\\", '"', "'", "*", ">", "<", "|"]:
                name = name.replace(each, " ")
        name = name.replace("?", "？")
        name = name.replace(":", "：")
        with open("%s.m4a" % name, "wb") as f:
            f.write(m4a)
            f.close()

    def download_img(self, url):
        content = requests.get(url, headers=self.headers).content
        with open("专辑封面.jpg", "wb") as file:
            file.write(content)
            file.close()
