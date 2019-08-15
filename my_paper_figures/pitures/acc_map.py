import numpy as np
from pylab import xlim,ylim
from matplotlib import pyplot as plt

x = range(0,500)
y = []
with open('/home/wshong/Desktop/实验结果quora/mpsc/mpsc_acc','r') as fi:
    for acc in fi.readlines():
        y.append(float(acc))
        #print(float(acc))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
#plt.legend('mpsc')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/arci/arci_acc','r') as fi:
    for acc in fi.readlines():
        y.append(float(acc))
        #print(float(acc))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
#plt.legend('arci')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/mvlstm/mvlstm_acc','r') as fi:
    for acc in fi.readlines():
        y.append(float(acc))
        #print(float(acc))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
#plt.legend('mvlstm')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/matchpyramid/matchpyramid_acc','r') as fi:
    for acc in fi.readlines():
        y.append(float(acc))
        #print(float(acc))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/matchsrnn/matchsrnn_acc','r') as fi:
    for acc in fi.readlines():
        y.append(float(acc))
        #print(float(loss))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
plt.hold

plt.grid(True)

plt.legend(['MPSC','ARC-I','MV-LSTM','MatchPyramid','MatchSRNN'])
plt.xlabel('Iter')
plt.ylabel('Accuracy')
plt.savefig('acc.eps', format='eps')
plt.show()
