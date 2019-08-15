# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
# MPSC:map=0.649491	ndcg@3=0.631785	ndcg@5=0.688016
# 只有原语义ndcg@3=0.572775	ndcg@5=0.627452	map=0.599868
# ndcg@5=0.643505	map=0.602383	ndcg@3=0.580659
# 原语义、正向反向：ndcg@5=0.683687	ndcg@3=0.625374	map=0.638055
# map=0.635775	ndcg@5=0.670895	ndcg@3=0.623061
# 原语义、正向ndcg@5=0.670272	map=0.625848	ndcg@3=0.615861
# ndcg@5=0.684149	map=0.639810	ndcg@3=0.628958

name_list = ['MAP', 'NDCG@3', 'NDCG@5']
num_list = [1.5, 0.6, 7.8, 6]
#MPSC1
num_list1 = [0.599868, 0.572775, 0.627452]#
#MPSC3
num_list3=[0.638055,0.625374,0.683687]
#MPSC4
num_list4=[0.639810,0.628958,0.684149]
#MPSC
num_list9=[0.6587,0.6539,0.6959]
x = list(range(len(num_list1)))
total_width, n = 0.8, 4
width = total_width / n

plt.bar(x, num_list1, width=width, label='MGSC@1',  ec=["k","k","k"],fc='w')
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, num_list3, width=width, label='MGSC@3',  fc='w', edgecolor=["k","k","k"], hatch=".....")
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, num_list4, width=width, label='MGSC@4',  fc='w', edgecolor=["k","k","k"], hatch="/////")
for i in range(len(x)):
    x[i] = x[i] + width
plt.bar(x, num_list9, width=width, label='MGSC@9',  fc='w', edgecolor=["k","k","k"], hatch="\\\\\\\\\\")

plt.ylim(0.55,0.7)
#plt.yticks(fontsize=20)
plt.xticks(np.arange(3) + 1.5*width, name_list)
plt.ylabel('Score')
plt.legend()
plt.savefig('mgsc1349.eps', format='eps')
plt.show()