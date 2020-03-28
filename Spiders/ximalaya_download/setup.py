import os
import requests
import bs4
import xmlylib.get_url as gu
import xmlylib.get_list as gl
import xmlylib.download as do
import tqdm

'''
'有声书'
'音乐'
'相声评书'
'段子'
'情感生活'
'娱乐'
'影视'
'儿童'
'历史'
'商业'
'财经'
'人文'
'教育培训'
'IT科技'
'外语'
'头条'
'二次元'
'戏曲'
'旅游'
'健康养生'
'时尚'
'生活'
'广播剧'
'粤语'
'法律课堂'
'党员学习园地'
'品牌之声'
'汽车'
'闽南语'
'''
list_ty = [
    '有声书',
    '音乐',
    '相声评书',
    '段子',
    '情感生活',
    '娱乐',
    '影视',
    '儿童',
    '历史',
    '商业',
    '财经',
    '人文',
    '教育培训',
    'IT科技',
    '外语',
    '头条',
    '二次元',
    '戏曲',
    '旅游',
    '健康养生',
    '时尚',
    '生活',
    '广播剧',
    '粤语',
    '法律课堂',
    '党员学习园地',
    '品牌之声',
    '汽车',
    '闽南语',
]
dic_ty = {
    "有声书": "youshengshu",
    "音乐": "yinyue",
    "相声评书": "xiangsheng",
    "段子": "yule",
    "情感生活": "qinggan",
    "娱乐": "yule",
    "影视": "yingshi",
    "儿童": "ertong",
    "历史": "lishi",
    "商业财经": "shangye",
    "人文": "renwen",
    "教育培训": "jiaoyu",
    "IT科技": "keji",
    "外语": "waiyu",
    "头条": "toutiao",
    "二次元": "erciyuan",
    "戏曲": "xiqu",
    "旅游": "lvyou",
    "健康养生": "jiankang",
    "时尚生活": "shishang",
    "广播剧": "guangbojv",
    "粤语": "yueyu",
    "法律课堂": "falvketang",
    "党员学习园地": "dangtuanke",
    "品牌之声": "pinpai",
    "汽车": "qiche",
    "闽南语": "minnanyu",
}

class DownloadList():
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}

    def downloadlist(self, aid, ty):
        print("\n加载中...\nLoading...\n")
        gtl = gl.GetList()
        aul = gtl.get_all_list(aid, ty)
        aul_id = aul[0]
        aul_title = aul[1]
        print("下载列表：\n")
        for each in range(len(aul_id)):
            print("%s\t%s\n" % (str(each+1), aul_title[each]))
        album_info = gtl.getinfo(aid, ty)
        title = album_info[1]
        print("\n专辑分类：" + album_info[2])
        print("\n专辑更新信息：" + album_info[3])
        print("\n播放量：" + album_info[4])
        print("\n" + album_info[5])
        print("\n正在获取下载地址中...请耐心等待...")
        geturl = gu.GetUrl()
        url_list = []
        for each in aul_id:
            url_list.append(geturl.getjson(geturl.audiourl(each)))
        downl = do.Download()
        downl.make_file(title)
        downl.download_img(album_info[0])
        print("\n开始下载...\n")
        for each in tqdm.tqdm(range(len(url_list)), ncols=66):
            m4a = downl.download(url_list[each])
            downl.save_file(m4a, "%s %s" % (title, aul_title[each]))
            print("\n\n第%s首\t%s 下载成功..." % (str(each+1), aul_title[each]))
        os.chdir("..\\")
        print("\n下载完成，请继续使用")

def start():
    download = DownloadList()
    print("="*30 + "\n\n喜马拉雅专辑下载工具v1.0.0 by tonysyz\n\n" + "="*30 + "\n说明：本程序下载仅限于网页上可以播放的有声资源，若需要下载Vip资源，请前往购买。\n")
    aid = input("·请输入专辑id：")
    print("-"*30)
    a = 0
    for each in list_ty:
        a += 1
        print(str(a) + "." + each)
    ty = input("·请输入类别：")
    ty = int(ty) - 1
    ty = dic_ty[list_ty[ty]]
    print("==="*20)
    download.downloadlist(aid, ty)

if __name__ == "__main__":
    while True:
        pay = input("是否为付费？\n1.Yes\n2.No\n请选择：")
        if pay == "2":
            start()
        if pay == "1":
            print("Buy it yourself!")
