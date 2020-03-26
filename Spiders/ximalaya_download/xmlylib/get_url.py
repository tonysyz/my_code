import requests

class GetUrl():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        }
        #self.url = "https://www.ximalaya.com/revision/play/v1/audio?id=&ptype=1"

    def audiourl(self, aid):
        url = "https://www.ximalaya.com/revision/play/v1/audio?id=%s&ptype=1" % aid
        return url


    def getjson(self, url):
        j = requests.get(url, headers=self.headers).json()
        aurl = j["data"]["src"]
        return aurl

if __name__ == "__main__":
    get = GetUrl()
    aid = input("输入音频id：")
    url = get.audiourl(aid)
    aurl = get.getjson(url)
    print(aurl)