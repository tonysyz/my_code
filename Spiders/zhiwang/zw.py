from selenium import webdriver
import time
from lxml import etree
import random
import xlsxwriter
import os

a = input("姐姐要搜索什么呢？\n>>")
browser = webdriver.Edge()
browser.get("https://kns.cnki.net/kns/brief/default_result.aspx")
time.sleep(3)
browser.find_element_by_class_name("rekeyword").send_keys(a) # Enter Keyword!
browser.find_element_by_class_name("researchbtn").click() # Search it!
time.sleep(3)

def get_page(browser, alter):
    browser.switch_to_frame("iframeResult")
    if alter == 0:
        browser.find_element_by_class_name("class_grid_display_num")\
            .find_elements_by_xpath("""//a[contains(text(),"50")]""")[0].click()
    titles = browser.find_elements_by_class_name("fz14")
    authers = browser.find_elements_by_xpath("""//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr//td[@class="author_flag"]""")
    origins = browser.find_elements_by_xpath("""//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr//td[4]""")[1:]
    time_ = browser.find_elements_by_xpath("""//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr//td[5]""")[1:]
    database = browser.find_elements_by_xpath("""//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr//td[6]""")[1:]
    quoted = browser.find_elements_by_xpath("""//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr//td[7]""")[1:]
    download = browser.find_elements_by_xpath("""//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr//td[8]""")[1:]
    read = browser.find_elements_by_xpath("""//*[@id="ctl00"]/table/tbody/tr[2]/td/table/tbody/tr//td[9]""")[1:]
    def get_text(target):
        new = []
        for each in target:
            new.append(each.text)
        return new
    final = [get_text(titles), get_text(authers), get_text(origins), \
        get_text(time_), get_text(database), get_text(quoted), get_text(download), get_text(read)]
    # print(final)
    return final

def turn_page(browser):
    # print(browser.find_elements_by_xpath("""//div//a[contains(text(),"下一页")]"""))
    browser.find_elements_by_xpath("""//div//a[contains(text(),"下一页")]""")[0].click()
    browser.switch_to.default_content()

i = 0
result_ = []
while True:
    try:
        result_.append(get_page(browser, i))
    except KeyboardInterrupt:
        print("强制结束")
    try:
        turn_page(browser)
        time.sleep(random.randint(2,8))
    except:
        print('!')
        w = input("输入验证码(0)还是爬完了(1)？\n>>")
        if w == "0":
            time.sleep(30)
            turn_page(browser)
        elif w == "1":
            break
        else:
            print("请输入正确数字\n")
    i += 1
    print("page:{}\tnumber:{}".format(i, i*50))

workbook = xlsxwriter.Workbook('new_excel.xlsx')
worksheet = workbook.add_worksheet('sheet1')


def new_(result_, i):
    new = []
    for each in result_:
        new += each[i]
    return new
headings = ["标题", "作者", "源", "时间", "数据库", "引用", "下载", "阅读"]
titles = new_(result_, 0)
authers = new_(result_, 1)
origins = new_(result_, 2)
time_ = new_(result_, 3)
database = new_(result_, 4)
quoted = new_(result_, 5)
download = new_(result_, 6)
read = new_(result_, 7)

def write(sheet, content, i):
    for i in range(len(content)):
        sheet.write(0, i, content[i])

worksheet.write_row('A1',headings)
worksheet.write_column('A2', titles)
worksheet.write_column('B2', authers)
worksheet.write_column('C2', origins)
worksheet.write_column('D2', time_)
worksheet.write_column('E2', database)
worksheet.write_column('F2', quoted)
worksheet.write_column('G2', download)
worksheet.write_column('H2', read)
workbook.close()