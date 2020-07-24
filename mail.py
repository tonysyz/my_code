import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time
import win32api, win32con
from tqdm import tqdm

def send_file(path):

    msg_from = 'wwwwww@163.com'
    passward = 'wwwwwww'
    msg_to = 'wwwwwwwwww@163.com'

    t = time.localtime()
    subject = '{}-{}-{}_{}:{}:{} Files'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    content = '<html><body><h1>基于Python的HTML邮件发送</h1>'\
    '<h2>Programmed by <a href="https://www.cnblogs.com/tonysyz/">tony_syz</a> on <a href="http://python.org/">Python</a></h2> <br/>'\
    '<h3>Hi,欢迎关注博客<a href="https://www.cnblogs.com/tonysyz/">tony_syz</a>，个人感觉里面几篇文章还是很有用的，<br/>还有我的<a href="https://space.bilibili.com/562400796">Bilibili</a><br/></h3>'\
    '<h3>以及推荐一些大佬们的<a href="https://space.bilibili.com/66806831/favlist?fid=839410231&ftype=create">manim(超赞的数学动画！)</a></h3><br/>'\
    '<h3>发送邮件的程序的源代码戳这里--><a href="https://github.com/tonysyz/my_code">tonysyz的GitHub</a>，欢迎follow！</h3><br/>'\
    '<h4>使用愉快wwwwww</h4><br/>'\
    '</body></html>'

    #msg = MIMEText(content,'html','utf-8')
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to

    #添加html内容
    msg.attach(MIMEText(content,'html','utf-8'))

    files = []
    d=[]
    e=[]
    f=[]
    #添加附件
    for a,b,c in os.walk(path):
        d.append(a)
        e.append(b)
        f.append(c)
    filenames = []
    print('获取文件目录...\n')
    for each in d:
        for e in f[d.index(each)]:
            filenames.append(e)
            files.append('{}\\{}'.format(each, e))
    print('添加文件...\n')
    for each in tqdm(files, ncols=66):
        with open(each,'rb') as f:
            mime = MIMEBase('image','jpg',filename=filenames[files.index(each)])
            mime.add_header('Content-Disposition','attachment',filename=filenames[files.index(each)])
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            msg.attach(mime)
    print('uploading...\n')
    try:
        s = smtplib.SMTP('smtp.163.com',25)
        s.login(msg_from,passward)
        print('log_in as tony_syz@163.com')
        s.sendmail(msg_from,msg_to,msg.as_string())
        win32api.MessageBox(0, '发送成功!', "tony_syz", win32con.MB_OK)
    except smtplib.SMTPException as e:
        win32api.MessageBox(0, 'Error:'+e, "tony_syz", win32con.MB_ICONWARNING)
    finally:
        s.quit()

if __name__ == '__main__':
    i = win32api.MessageBox(0, '是否发送至邮箱？', "tony_syz", win32con.MB_YESNO)
    if i == 6:
        send_file(r'.\\')