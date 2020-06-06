import requests
import json
import bs4

class GetAnswer:
    def __init__(self):
        self.h = {
            'DEVICE-SYSTEMVERSION': '9',
            'DEVICE-BRAND': 'Xiaomi',
            'Accept': 'application/json',
            'DEVICE-SYSTEMMODEL': 'Redmi 6',
            'DEVICE-APK-VERSION': '3.7.8.0',
            'User-Token': '9jj1YnPvHft9daeQPGRkpPbPNoJWkcdwGSM01u52pmZZJmReQPMeUAPKuqVBS5QyRb0rJoYlRr4=',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; Redmi 6 MIUI/V11.0.3.0.PCGCNXM)',
            'Host': 'apijqzy.zxxk.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        self.classid = ""
        self.studentid = ""

    def get_homework(self, homeworkid, sign):
        url = "https://apijqzy.zxxk.com/Student/HomeWorks/GetHomeWorkDetailed?studentid=%s&homeworkid=%s&classid=%s&sign=%s" % (self.studentid, homeworkid, self.classid , sign)
        resp = requests.get(url, headers=self.h)
        html = resp.json()
        return html

    def get_homework_by_url(self, url):
        resp = requests.get(url, headers=self.h)
        html = resp.json()
        return html
        
    def get_answer(self, html):
        data = html["Data"]
        try:
            title = data["TRHomeWorkName"]
        except:
            title = "exam_answer"
        ques = data["Question"]
        result = str(title) + "答案:\n"
        e = 0
        for i in range(len(ques)):
            e += 1
            if "</span>" not in ques[i]["QuesAnswer"]:
                result += (str(ques[i]["OrderNumber"]) + "." + ques[i]["QuesAnswer"] + "\n")
            else:
                result += (str(ques[i]["OrderNumber"]) + ".")
                soup = bs4.BeautifulSoup(ques[i]["QuesAnswer"], 'html.parser')
                for each0 in soup.find_all("span", class_="qml-an"):
                        result += (each0.get_text() + "\n")
        return result
    
    def get_homework_title(self, html):
        data = html["Data"]
        return data["TRHomeWorkName"]

    def get_selfsubmit_answer(self, html):
        ques = html["Data"]["Question"]
        result = ""
        for a in range(len(ques)):
            child = ques[a]["ChildQues"]
            for b in range(len(child)):
                order = child[b]["OrderNumber"]
                answer = child[b]["QuesAnswer"]
                result += str(order) + "." + str(answer) + "\n"
        return result

    def hurl(self, a):
        data = a["Data"]
        pathanswer = data["PathAnswer"]
        return pathanswer

    def change_config(self, cla, stu, d):
        self.h = d
        self.classid = cla
        self.studentid = stu
'''
    def tryurl(self, homeworkid, classid):
        url = "http://jqzy.zxxk.com/Student/homework/submitselfanswer?hid=" + str(homeworkid) + "&classid=" + str(classid)
        config = {
            "Host": "jqzy.zxxk.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://jqzy.zxxk.com/student/homework/homeworklist",
            "Connection": "keep-alive",
            "Cookie": self.cookie,
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        html = requests.get(url, headers=config)
        soup = bs4.BeautifulSoup(html.text, features="html.parser")
        ques_url = soup.iframe["src"]
        key = ques_url.split(r"/")[5]
        date = ques_url.split(r"/")[4]
        ans_url = "https://zyfile.zxxk.com/selfword/" + date + "/"+ key +"/answer/A_"+ key +".html"
        ans = requests.get(ans_url)
        
        if ans.status_code == 200:
            return ans_url
        if ans.status_code == 404:
            return "Teacher didn't upload answers, try to get it on phone!"

    def set_cookie(self, cookie):
        self.cookie = cookie
'''



if __name__ == "__main__":
    getanswer = GetAnswer()
    homeworkid = input("请输入作业代码:\n")
    sign = input("请输入签名:\n")
    print("爬取答案中......")
    homework = getanswer.get_homework(str(homeworkid), str(sign))
    ans = getanswer.get_answer(homework)
    print(ans)

