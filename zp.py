import os
import zipfile
import xlrd
import time
try:
    from xlutils.copy import copy
except:
    os.system(r'pip install xlutils -i http://mirrors.aliyun.com/pypi/simple/')
    time.sleep(10)
    from xlutils.copy import copy
import shutil

def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files

def get_zipfile_list(file_list):
    l = []
    for each in file_list:
        if '.zip' in each:
            l.append(each)
    return l

def zip_out(zip):
    zf = zipfile.ZipFile(zip)
    zip_list = zf.namelist()
    zl = []
    for zip_file in zip_list:
        try:
            zip_file = zip_file.encode('cp437').decode('gbk')
        except:
            zip_file = zip_file.encode('utf-8').decode('utf-8')
        zl.append(zip_file)
    for i in range(len(zl)):
        zf.extract(zip_list[i], path='.\\{}\\'.format(zip[:-4]))
        try:
            os.rename('.\\{}\\{}'.format(zip[:-4], zip_list[i]), '.\\{}\\{}'.format(zip[:-4], zl[i]))
        except FileExistsError as e:
            # print('File Exist')
            pass
        os.popen("del .\\{}\\{}".format(zip[:-4], zip_list[i]))
    zf.close()
    zn = []
    for each in zl:
        zn.append('.\\'+zip[:-4]+'\\'+each)
    return [zip[-4], zn]

def get_zipingshiping(path):
    wb = xlrd.open_workbook(path)
    try:
        s = wb.sheet_by_index(2)
    except:
        s = wb.sheet_by_index(0)
    ziping = s.cell(3,1).value
    shiping = s.cell(4,1).value
    return [ziping, shiping]

def fill_in(path1, name, ziping, shiping):
    book = xlrd.open_workbook(path1)
    s = book.sheet_by_index(0)
    c = s.col_values(1)
    try:
        n = c.index(name)
    except ValueError:
        print('姓名错误')
        return 0
    wb = copy(book)
    ws = wb.get_sheet(0)
    ws.write(n,2,ziping)
    ws.write(n,3,shiping)
    wb.save(path1)

def get_unfilled_list(path):
    book = xlrd.open_workbook(path)
    s = book.sheet_by_index(0)
    c = s.col_values(1)
    # i = 0
    list0 = []
    for a in range(len(s.col_values(2))):
        if s.col_values(3)[a] == '' or s.col_values(2)[a] == '':
            # print(str(i)+'\t'+c[a]+' not filled in...')
            # i+=1
            list0.append(c[a])
    return list0

def get_unfilled_list0(path):
    book = xlrd.open_workbook(path)
    s = book.sheet_by_index(0)
    c = s.col_values(1)
    list0 = []
    for a in range(len(s.col_values(2))):
        if s.col_values(3)[a] == '' and s.col_values(2)[a] == '':
            list0.append(c[a])
    return list0

def dirs(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return dirs

def get_dict(path):
    # print(path)
    names = file_name(path)
    result = {
        'gys':0,
        'gyx':0,
        'ges':0,
        'gex':0,
    }
    for each in names:
        # print(each)
        file = '.\\{}\\{}'.format(path, each)
        wb = xlrd.open_workbook(file)
        try:
            s3 = wb.sheet_by_index(2)
        except:
            try:
                s3 = wb.sheet_by_index(1)
            except:
                s3 = wb.sheet_by_index(0)
        social_service = {
            'school': s3.cell(10,1).value,
            'class': s3.cell(10,3).value,
            'name': s3.cell(11,1).value,
            'time': s3.cell(12,1).value,
            'location': s3.cell(12,3).value,
            'unit': s3.cell(13,1).value,
            'content': s3.cell(14,1).value,
            'comment': s3.cell(15,1).value,
        }
        social_practice = {
            'school': s3.cell(20,1).value,
            'class': s3.cell(20,3).value,
            'name': s3.cell(21,1).value,
            'id': s3.cell(21,3).value,
            'location': s3.cell(22,1).value,
            'time': s3.cell(22,3).value,
            'u': s3.cell(23,1).value,
            'content': s3.cell(24,1).value,
            'comment': s3.cell(25,1).value,
        }
        study = {
            'school': s3.cell(30,1).value,
            'class': s3.cell(30,3).value,
            'name': s3.cell(31,1).value,
            'id': s3.cell(31,3).value,
            'title': s3.cell(32,1).value,
            'responsibility': s3.cell(33,1).value,
            'result': s3.cell(33,3).value,
            'finished_time': s3.cell(34,1).value,
            'teacher': s3.cell(34,3).value,
            'members': s3.cell(35,1).value,
            'content': s3.cell(36,1).value,
            'comment': s3.cell(37,1).value,
        }
        p = []
        for i in range(41,49):
            try:
                o = s3.cell(i,0).value
                if o != '':
                    p.append(
                        {
                            'name': o,
                            'prize_name': s3.cell(i,1).value,
                            'level': s3.cell(i,2).value,
                            'unit': s3.cell(i,3).value,
                            'date': s3.cell(i,4).value,
                        }
                    )
            except IndexError:
                break

        r = {
            'social_service': social_service,
            'social_practice': social_practice,
            'study': study,
            'prize': p,
        }
        if '高一' in each:
            if '上' in each:
                result.update({'gys': r})
            elif '下' in each:
                result.update({'gyx': r})
        elif '高二' in each:
            if '上' in each:
                result.update({'ges': r})
            elif '下' in each:
                result.update({'gex': r})
    return result

def fill_in_all(gys, path, nn):
    book = xlrd.open_workbook(path,formatting_info=True)
    wb = copy(book)
    sh_1s = wb.get_sheet(nn)
    # gys = dic['gys']
    # gyx = dic['gyx']
    # ges = dic['ges']
    # gex = dic['gex']
    ss_1s = gys['social_service']
    sh_1s.write(10,1,ss_1s['school'])
    sh_1s.write(10,3,ss_1s['class'])
    sh_1s.write(11,1,ss_1s['name'])
    sh_1s.write(12,1,ss_1s['time'])
    sh_1s.write(12,3,ss_1s['location'])
    sh_1s.write(13,1,ss_1s['unit'])
    sh_1s.write(14,1,ss_1s['content'])
    sh_1s.write(15,1,ss_1s['comment'])

    sp_1s = gys['social_practice']
    sh_1s.write(20,1,sp_1s['school'])
    sh_1s.write(20,3,sp_1s['class'])
    sh_1s.write(21,1,sp_1s['name'])
    sh_1s.write(21,3,sp_1s['id'])
    sh_1s.write(22,1,sp_1s['location'])
    sh_1s.write(22,3,sp_1s['time'])
    # print(sp_1s['u'])
    sh_1s.write(23,1,sp_1s['u'])
    sh_1s.write(24,1,sp_1s['content'])
    sh_1s.write(25,1,sp_1s['comment'])

    if nn == 1 or nn == 3:
        st_1s = gys['study']
        sh_1s.write(30,1,st_1s['school'])
        sh_1s.write(30,3,st_1s['class'])
        sh_1s.write(31,1,st_1s['name'])
        sh_1s.write(31,3,st_1s['id'])
        sh_1s.write(32,1,st_1s['title'])
        sh_1s.write(33,1,st_1s['responsibility'])
        sh_1s.write(33,3,st_1s['result'])
        sh_1s.write(34,1,st_1s['finished_time'])
        sh_1s.write(34,3,st_1s['teacher'])
        sh_1s.write(35,1,st_1s['members'])
        sh_1s.write(36,1,st_1s['content'])
        sh_1s.write(37,1,st_1s['comment'])

        pr_1s = gys['prize']
        for i in range(len(pr_1s)):
            n = pr_1s[i]
            # print(n['name'])
            sh_1s.write(41+i,0,n['name'])
            sh_1s.write(41+i,1,n['prize_name'])
            sh_1s.write(41+i,2,n['unit'])
            sh_1s.write(41+i,3,n['date'])
    else:
        pr_1s = gys['prize']
        for i in range(len(pr_1s)):
            n = pr_1s[i]
            # print(n['name'])
            sh_1s.write(30+i,0,n['name'])
            sh_1s.write(30+i,1,n['prize_name'])
            sh_1s.write(30+i,2,n['unit'])
            sh_1s.write(30+i,3,n['date'])

    wb.save(path)

if __name__ == "__main__":
    # try:
    #     print(get_dict("syz"))
    # except xlrd.biffh.XLRDError:
    #     print('Close the file')
    dirs_ = dirs(r'E:\zp')
    ex = []
    for each in dirs_:
        e = '.\\{}.xls'.format(each)
        shutil.copy('class_name_term.xls', e)
        try:
            fill_in_all(get_dict(each)['gys'], '.\{}.xls'.format(each), 0)
        except IndexError as ee:
            ex.append(each)
        try:
            fill_in_all(get_dict(each)['gyx'], '.\{}.xls'.format(each), 1)
        except IndexError as ee:
            ex.append(each)

        try:
            fill_in_all(get_dict(each)['ges'], '.\{}.xls'.format(each), 2)
        except IndexError as ee:
            ex.append(each)
        try:
            fill_in_all(get_dict(each)['gex'], '.\{}.xls'.format(each), 3)
        except IndexError as ee:
            ex.append(each)
        # dic = get_dict('.\\{}\\'.format(each))
        ex = list(set(ex))
    print('格式错误：')
    print(ex)
'''
if __name__ == "__main__":
    f = file_name('E:\\zp')
    z = get_zipfile_list(f)
    l = []
    i = 0
    for each in z:
        l.append(zip_out(each)[1])
    for each in l:
        for e in each:
            zs = get_zipingshiping(e)
            name = e.split('\\')[1]
            if '高二' in e:
                if '上' in e:
                    i += 1
                    fill_in('23shang2.xls', name, zs[0], zs[1])
                    print(str(i)+'\t'+name+'高二上学期录入...')
                if '下' in e:
                    i += 1
                    fill_in('23xia2.xls', name, zs[0], zs[1])
                    print(str(i)+'\t'+name+'高二下学期录入...')
            if '高一' in e:
                if '上' in e:
                    i += 1
                    fill_in('23_1.xls', name, zs[0], zs[1])
                    print(str(i)+'\t'+name+'高一上学期录入...')
                if '下' in e:
                    i += 1
                    fill_in('23_2.xls', name, zs[0], zs[1])
                    print(str(i)+'\t'+name+'高一下学期录入...')

    gys = get_unfilled_list('23_1.xls')
    gyx = get_unfilled_list('23_2.xls')


    print('?缺少高一上')
    for each in gys:
        if each not in gyx:
            print(each)
    print('?缺少高一下')
    for each in gyx:
        if each not in gys:
            print(each)
    print('?缺少高一')
    i = 0
    for each in gyx:
        if each in gys:
            print(str(i)+'\t'+each)
            i+=1

    print('-'*10)
    print('高二上')
    a1 = get_unfilled_list('23shang2.xls')
    print('-'*10)
    print('高二下')
    a2 = get_unfilled_list0('23xia2.xls')
    print('-'*10)
    print('?缺少高二下')
    for each in a2:
        if each not in a1:
            print(each)

    print('?缺少高二上')
    for each in a1:
        if each not in a2:
            print(each)
    print('?缺少高二')
    i = 0
    for each in a1:
        if each in a2:
            print(str(i)+'\t'+each)
            i+=1
    i = 0
    print('?缺少all')
    for each in a1:
        if each in a2 and each in gys and each in gyx:
            print(str(i)+'\t'+each)
            i+=1'''