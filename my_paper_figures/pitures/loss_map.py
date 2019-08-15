import numpy as np
from pylab import xlim,ylim
from matplotlib import pyplot as plt

x = range(0,500)
y = []
with open('/home/wshong/Desktop/实验结果quora/mpsc/mpsc_loss','r') as fi:
    for loss in fi.readlines():
        y.append(float(loss))
        #print(float(loss))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
#plt.legend('mpsc')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/arci/arci_loss','r') as fi:
    for loss in fi.readlines():
        y.append(float(loss))
        #print(float(loss))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
#plt.legend('arci')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/mvlstm/mvlstm_loss','r') as fi:
    for loss in fi.readlines():
        y.append(float(loss))
        #print(float(loss))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
#plt.legend('mvlstm')
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/matchpyramid/matchpyramid_loss','r') as fi:
    for loss in fi.readlines():
        y.append(float(loss))
        #print(float(loss))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
#plt.grid(True)  # 添加网格
plt.plot(x, y)  # 绘实线图
plt.hold

y = []
with open('/home/wshong/Desktop/实验结果quora/matchsrnn/matchsrnn_loss','r') as fi:
    for loss in fi.readlines():
        y.append(float(loss))
        #print(float(loss))

#plt.scatter(x, y, marker='s', color='r')  # 绘制散点图
plt.plot(x, y)  # 绘实线图
plt.hold

plt.grid(True)  # 添加网格
plt.legend(['MPSC','ARC-I','MV-LSTM','MatchPyramid','MatchSRNN'])
plt.xlabel('Iter')
plt.ylabel('Loss')
plt.savefig('loss.eps', format='eps')
plt.show()
