import os
import re

cur_dir = '/storage/emulated/0'
internal = '/storage/emulated/0'


def gbk2utf8(str):
    return bytes(str, encoding='gbk').decode('utf8')


def listdir(dir):
    r = os.popen('adb shell ls '+dir)
    res = r.readlines()

    # 对返回值做编码处理
    text = []
    for i in res:
        if i != '\n':
            text.append(gbk2utf8(re.sub(r'\n', '', i)))

    if re.search(r'No such file or directory', text[0]) is None:
        cur_dir = cur_dir_tmp
        print(text)
        return text
    else:
        print('文件或目录不存在')
        return None


def pull():
    filelist = listdir(cur_dir)
    while(1):
        name = input("请输入文件名(s搜索e退出)")
        if name == 's':
            pat = input("请输入匹配字段")
            for i in filelist:
                if re.search(r''+pat, i) is not None:
                    print(i)
            continue
        if name == 'e':
            break
        if name not in filelist:
            print("没有此文件")
        else:
            os.system('adb pull '+cur_dir+'/'+name +
                      ' C:\\Users\\quietboy\\Desktop'+'\\'+name)
            print("请等待...")


def extractapk():
    r = os.popen('adb shell pm list packages')
    res = r.readlines()
    text = []
    for i in res:
        if i != '\n':
            text.append(re.sub(r'\n', '', i))
    for i in text:
        print(i)
    while(1):
        name = input("请输入包名(s搜索e退出)")
        if name == 's':
            pat = input("请输入匹配字段")
            for i in text:
                if re.search(r''+pat, i) is not None:
                    print(i)
            continue
        if name == 'e':
            break
        r = os.popen('adb shell pm path '+name)
        apppath = r.readline().strip()[8:]
        if apppath == '':
            print("没有此app")
        else:
            os.system('adb pull '+apppath +
                      ' C:\\Users\\quietboy\\Desktop'+'\\'+name+'.apk')
            print("请等待...")


if __name__ == '__main__':
    cur_dir_tmp = ''
    listdir(cur_dir)
    while(1):
        print('1.下一级 2.上一级 3.传输到电脑 4.自定义路径 5.返回到主目录 6.当前目录文件 7.提取apk')
        c = input()
        if c == '1':
            d = input()
            cur_dir_tmp = cur_dir+'/'+d
            listdir(cur_dir_tmp)
        elif c == '3':
            pull()
        elif c == '5':
            cur_dir = internal
            listdir(cur_dir)
        elif c == '6':
            listdir(cur_dir)
        elif c == '7':
            extractapk()
# adb shell pm list package
