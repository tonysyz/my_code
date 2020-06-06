
def get_config(file_title):
    openfile = open("%s.txt" % file_title, "r")
    lines = openfile.readlines()
    dic = {}
    for count in range(len(lines)-1):
        if count >= 1:
            key = lines[count].split(":")[0]
            arg = lines[count].split(":")[-1][:-1]
            dic[key] = arg[1:]
        if count == len(lines):
            break
    result = dic
    return result

def get_url(file_title):
    openfile = open("%s.txt" % file_title, "r")
    lines = openfile.readlines()
    url = lines[0][4:-10]
    return url

def get_stu_and_cls(url):
    l = url.split("&")
    studentid = l[0].split("=")[-1]
    homeworkid = l[1].split("=")[-1]
    classid = l[2].split("=")[-1]
    sign = l[0].split("=")[-1]
    return [studentid, homeworkid, classid, sign]


if __name__ == "__main__":
    file_title = input("请输入文件名:(txt格式,不要带后缀名!):\n")
    result = get_config(file_title)
    print(result)