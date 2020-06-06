import jzjxtlib.read_file as rd
import jzjxtlib.get_answer as gt
import jzjxtlib.save_answer as sv

a = gt.GetAnswer()
print("*"*50 + "\n")
print("学科网精准教学通考试破解程序 Version 1.0.1 by tonysyz\n")
print("*"*50)
print("Please Choose:")

while True:
    c = input("1.homework\n2.exam\n3.reset_cookie\n4.quit\nYour Choice:")
    if c == "1":
        x = input("1.get answer url by web\n2.get answer by phone\n3.quit\n")
        if x == "1":
            '''
            homeworkid = input("homeworkid:\n")
            classid = input("classid:\n")
            if classid != "xxxxx":
                print("Attention: If you are not the author of this software, please go to web to get cookies of your account and save your cookies by 'reset cookies' in the program...")
                try:
                    file0 = open("cookie.txt","r")
                except FileNotFoundError:
                    print("please reset your cookie and do not delete 'cookie.txt'")
                else:
                    cookie = file0.readlines()[0]
                    a.cookie = cookie
                    try:
                        a.tryurl(homeworkid, classid)
                    except TypeError:
                        print("homework has not begun or has been finished......")
                    else:
                        print(a.tryurl(homeworkid, classid))
            else:
                try:
                    a.tryurl(homeworkid, classid)
                except TypeError:
                    print("homework has not begun or has been finished......")
                else:
                    print(a.tryurl(homeworkid, classid))
            '''
        elif x == "2":
            filename = input("if you have got it on your phone, please enter your file name:\n")
            cfg = rd.get_config(filename)
            url = rd.get_url(filename)
            l = rd.get_stu_and_cls(url)
            a.change_config(l[3], l[1], cfg)
            html = a.get_homework_by_url(url)
            answer = a.get_selfsubmit_answer(html)
            path = a.hurl(html)
            print("\n" + "*"*20)
            print(path)
            print("\n" + "*"*20)
            print(answer)
            print("\n" + "*"*20)
            ch = input("\nsave_answer?\n1.Yes\n2.No\n")
            if ch == "1":
                sv.save(answer, a.get_homework_title(html))
        elif x == "3":
            break
    elif c == "2":
        choose = input("1.get answer from request.txt(suggested)\n2.get answer from url\n3.get answer from attr\n4.help\n5.quit\nYourChoice:")
        if choose.isdigit() == False:
            print("please enter the number!!!")
        elif choose.isdigit() == True:
            n = int(choose)
            if n == 1:
                filename = input("please enter your file name:\n")
                cfg = rd.get_config(filename)
                url = rd.get_url(filename)
                l = rd.get_stu_and_cls(url)
                a.change_config(l[3], l[1], cfg)
                html = a.get_homework_by_url(url)
                answer = a.get_answer(html)
                print("\n" + "*"*20)
                print(answer)
                print("\n" + "*"*20)
                ch = input("\nsave_answer?\n1.Yes\n2.No\n")
                if ch == "1":
                    sv.save(answer, a.get_homework_title(html))

            elif n == 2:
                url = input("please enter your url:\n")
                html = a.get_homework_by_url(url)
                answer = a.get_answer(html)
                print(answer)
            elif n == 3:
                homeworkid = input("\nhomewoekid:\n")
                sign = input("\nsign:\n")
                html = a.get_homework(homeworkid, sign)
                answer = a.get_answer(html)
            elif n == 4:
                print("\n" + "*"*20)
                print("https://github.com/tonysyz/xkwjzjxt_pojie")
            elif n ==5:
                break
            else:
                print("enter error!!!")
    elif c == "3":
        file0 = open(r"cookie.txt", "w")
        i = input("cookie:\n")
        file0.write(i)
        file0.close()
    elif c == "4":
        break
    else:
        print("enter error!!!")