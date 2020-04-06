import os

dirlist = os.listdir()
input_list = []
for each in dirlist:
    if 'm3u8' in each:
        input_list.append(each)

output = []
for each in input_list:
    if ' ' in each:
        print('error\n\n'+each+'\n\n')
    output.append(each.split('.')[0]+'.mp4')

bat = '''@echo off
echo Start Process...
'''

for each in range(len(input_list)):
    bat += 'ffmpeg -i %s %s\n' % (input_list[each], output[each])
bat += 'pause'

with open('process.bat', 'w') as f:
    f.write(bat)
    f.close()
