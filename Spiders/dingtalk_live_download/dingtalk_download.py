import requests
import tqdm
import os
requests.packages.urllib3.disable_warnings()

class Download:
    def __init__(self):
        self.headers = {
            'Host': 'aliliving-pre.alicdn.com',
            'Connection': 'keep-alive',
            'Origin': 'https://h5.m.taobao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 dingtalk-win/1.0.0 nw(0.14.7) DingTalk(5.0.11-Release.2) Mojo/1.0.0 Native AppType(release)',
            'Accept': '*/*',
            'Referer': 'https://h5.m.taobao.com/tblive/dingtalk/pc-playback.html',
            # 'Accept-Encoding': 'gzip, deflate, br'
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }

    def download(self):
        title = '''
*********************************
Dingtalk Download Tools v1.2.0
*********************************
During your use, please keep the Internet connected...
Help: Follow the instruction.
Hope you enjoy this program.
*********************************
'''
        print(title)
        m3u8 = input('url:')
        text = self.get_text(m3u8)
        vl = self.get_list(text, m3u8)
        name = self.get_name()
        print('\nStarting...\n')
        self.save_file(name, vl)
        print('\nFinishing...\n')
        self.save_m3u8(text, name)
        print('%s finish download...\nPlease continue...'%name)

    def get_text(self, m3u8):
        m = requests.get(m3u8, verify=False)
        text = m.text.split("\n")
        return text

    def get_list(self, text, m3u8):
        video_list = []
        if 'aliliving-pre.alicdn.com/live_hp' in m3u8:
            url = 'https://aliliving-pre.alicdn.com/live_hp/' # https://aliliving-pre.alicdn.com/live_hp/9421d502-810a-4ed8-bbcc-2326f1291dbc.m3u8
        elif 'dtliving-pre.alicdn.com/live_hp' in m3u8:
            url = 'https://dtliving-pre.alicdn.com/live_hp/'
        elif 'dtliving-pre.alicdn.com/live/' in m3u8:
            url = 'https://dtliving-pre.alicdn.com/live/'
        elif 'aliliving-pre.alicdn.com/live/' in m3u8:
            url = 'https://aliliving-pre.alicdn.com/live/'
        else:
            url = m3u8.split("?")[0].split('-')[0][:-8]
        for each in text:
            if '.ts' in each:
                video_list.append(url+each)
        return video_list

    def get_name(self):
        date = input('Date:')
        subj = input('Subject:')
        others = input('Others:')
        return date + '_' + subj + '_' + others

    def save_file(self, filename, video_list):
        try:
            os.mkdir('.\\%s' % filename)
        except FileNotFoundError:
            os.chdir('.\\%s' % filename)
        except FileExistsError:
            os.chdir('.\\%s' % filename)
        else:
            os.chdir('.\\%s' % filename)
        i = 1
        for each in tqdm.tqdm(video_list,ncols=72):
            video = requests.get(each, verify=False)
            with open(each.split('?')[0].split('/')[-1], 'wb') as video_file:
                for chunk in video.iter_content(chunk_size=512):
                    video_file.write(chunk)
                video_file.close()
            del(video) # This is required, or MemoryError will occur.
            i += 1
        os.chdir('..\\')

    def save_m3u8(self, text, filename):
        new_m3u8 = ''
        for each in range(len(text)):
            if '.ts' in text[each]:
                add_text = "%s\%s"%(filename, text[each].split('?')[0].split('/')[-1])
                new_m3u8 += add_text + '\n'
            else:
                new_m3u8 += text[each] + '\n'

        with open('%s.m3u8' % (filename), 'w') as m3u8_file:
            m3u8_file.write(new_m3u8)
            m3u8_file.close()

if __name__ == '__main__':
    while True:
        download = Download()
        download.download()