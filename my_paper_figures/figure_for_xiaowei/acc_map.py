import numpy as np
from pylab import xlim,ylim
from matplotlib import pyplot as plt

x = [0,100,200,300,400,500]
y = []
with open('/home/wshong/Desktop/实验结果quora/mpsc/mpsc_acc','r') as fi:
    count=0
    for acc in fi.readlines():
        if(count in [0,99,199,299,399,490]):
            y.append(float(acc))
        count+=1
        #print(float(acc))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y, color='k', linestyle=':', marker='o')  # 绘实线图
#plt.legend('mpsc')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/arci/arci_acc','r') as fi:
    count = 0
    for acc in fi.readlines():
        if (count in [0, 99, 199, 299, 399, 499]):
            y.append(float(acc))
        count += 1

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y, color='k', linestyle='-', marker='^')  # 绘实线图
#plt.legend('arci')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/mvlstm/mvlstm_acc','r') as fi:
    count = 0
    for acc in fi.readlines():
        if (count in [0, 99, 199, 299, 399, 499]):
            y.append(float(acc))
        count += 1

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y, color='k', linestyle='--', marker='<')  # 绘实线图
#plt.legend('mvlstm')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/matchpyramid/matchpyramid_acc','r') as fi:
    count = 0
    for acc in fi.readlines():
        if (count in [0, 99, 199, 299, 399, 499]):
            y.append(float(acc))
        count += 1

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y, color='k', linestyle='-.', marker='>')  # 绘实线图
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/matchsrnn/matchsrnn_acc','r') as fi:
    count = 0
    for acc in fi.readlines():
        if (count in [0, 99, 199, 299, 399, 499]):
            y.append(float(acc))
        count += 1

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y, color='k', linestyle='-', marker='v')  # 绘实线图
plt.hold

plt.grid(True)

plt.legend(['MGSC','ARC-I','MV-LSTM','MatchPyramid','MatchSRNN'])
plt.xlabel('Iter')
plt.ylabel('Accuracy')
plt.savefig('mgsc_acc.eps', format='eps')
plt.show()
