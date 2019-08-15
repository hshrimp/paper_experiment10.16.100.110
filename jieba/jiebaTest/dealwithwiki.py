# -*- coding:utf-8 -*-
# file: FileMerage.py
#
import  time
#os模块中包含很多操作文件和目录的函数
import os
import re
#获取目标文件夹的路径
#meragefiledir = os.getcwd()+'/merage5'
meragefiledir = '/home/wshong/Downloads/wikiextractor-master/extracted/AA'
#获取当前文件夹中的文件名称列表
#打开当前目录下的result.txt文件，如果没有则创建
#文件也可以是其他类型的格式，如result.js
file=open(meragefiledir+'/wiki_jian','r')
#向文件中写入字符
#file.write('python\n')
time1=time.time()
reg1=re.compile('「')
reg2=re.compile('」')
reg3=re.compile('（）')
file2=open(meragefiledir+'/wiki_new.txt','w')

for line in file:
    if line.strip()=='':
        continue
    line=reg1.sub('“',line)
    line=reg2.sub('”',line)
    line=reg3.sub('',line)
    file2.write(line+'\n')
#关闭文件
file.close()
file2.close()
time2=time.time()
print time2-time1,'s'

# reg4=re.compile('-\{.*?(zh-hans|zh-cn):([^;]*?);.*?\}-')
# reg='-\{.*?(zh-hans|zh-cn):([^;]*?);.*?\}-'
# line='这些物件的结构性质被探讨于群、环、-{zh-cn:域;zh-tw:体}-等抽象系统中，该些物件事实上也就是这样的系统。此为代数的领域。在此有一个很重要的概念，即广义化至向量空间的向量，它于线性代数中被研究。向量的研究结合了数学的三个基本领域：数量、结构及空间。向量分析则将其扩展至第四个基本的领域内，即变化。'
# li=reg4.match(line)
# li2=re.match(reg,line)
# print li
# print li2

