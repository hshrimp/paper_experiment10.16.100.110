# coding=utf-8
import time
import jieba

# import os

jieba.enable_parallel(16)

# 获取目标文件夹的路径
filedir = '/home/wshong/Desktop/百度百科'
# 获取当前文件夹中的文件名称列表
# files=os.listdir(filedir+'/2去标签')

filename = 'bk021'
content = open(filedir + '/2去标签/' + filename, "r").read()
t1 = time.time()
words = list(jieba.cut(content))
log_f = open(filedir + "/3jieba分词/" + filename, "w")
for w in words:
    if cmp(w, '\r\n') == 0:
        print >> log_f
    else:
        print >> log_f, w.encode("utf-8"), " ",
t2 = time.time()
tm_cost = t2 - t1
log_f.close()
print 'speed', len(content) / tm_cost, " bytes/second", tm_cost
