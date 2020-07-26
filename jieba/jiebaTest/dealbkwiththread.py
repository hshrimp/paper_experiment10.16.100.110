# -*- coding:utf-8 -*-
#
import time
# os模块中包含很多操作文件和目录的函数
import os
import re
import threading

# 获取目标文件夹的路径
filedir = '/home/wshong/Desktop/百度百科'
# 获取当前文件夹中的文件名称列表
files = os.listdir(filedir + '/1按300000行切分')
# 要处理的符号
reg1 = re.compile('「')
reg2 = re.compile('」')
reg3 = re.compile('（）')
reg4 = re.compile('<.*?>')


# 对每一篇文档做处理
def player(filename):
    # print file
    file = open(filedir + '/1按300000行切分/' + filename, 'r')
    # file = open(filedir + '/1按300000行切分/bk10', 'r')
    time1 = time.time()
    file2 = open(filedir + '/2去标签test/' + filename, 'w')
    # file2 = open(filedir + '/2去标签/bk10' , 'w')
    for line in file:
        if line.strip() == '':
            continue
        line = reg4.sub(' ', line)
        line = reg1.sub('“', line)
        line = reg2.sub('”', line)
        line = reg3.sub('', line)
        line = line.replace(r'\n', '')
        file2.write(line + '\n')
    # 关闭文件
    file.close()
    file2.close()
    time2 = time.time()
    print time2 - time1, 's'


threads = []
filesrange = range(len(files))
# 创建线程
for i in filesrange:
    t = threading.Thread(target=player, args=(files[i],))
    threads.append(t)

if __name__ == '__main__':
    time1 = time.time()
    # 启动线程
    for i in filesrange:
        threads[i].start()
    # time.sleep(50)
    for i in filesrange:
        threads[i].join()
    time2 = time.time()
    print 'all time is ', time2 - time1, 's'
