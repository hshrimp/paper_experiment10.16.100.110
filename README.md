# paper_experiment10.16.100.110
学校服务器上的论文相关实验

## gloveEvaluate
该项目是对glove词向量的评估

## hyperopt_test
该项目是利用hyperopt这个包，对论文实验模型进行自动化的超参数搜索。
有一定效果，在一定程度上能够搜索出目前模型最佳的超参数。


## jieba/jieba_test
该项目主要是对jieba这个包的使用，使用jieba对百度百科的语料进行切分，并做了多线程的尝试
由于百度百科语料太大，还做了一些语料切分，以及切分完分词好再合并的工作。
最后是拿这些分好的词去训练glove模型及评估。


## MatchZoo_quora2
该项目是自己论文设计的深度学习模型MPSC在数据集quora上的训练及评估.
借助MatchZoo这个框架，感谢MatchZoo，框架下面还有好多文本匹配模型哦。


## MatchZoo_quora_filterStopwords
和MatchZoo_quora2差不多，这两个有一个是过滤了停用词，一个没有过滤停用词，忘了哪一个是哪一个了。
结论是没有过滤停用词的模型比较优秀，大概是使用的文本匹配数据集中句子都是短文本，很多停用词其实是很关键的词语。
详情见我的论文 MPSC: A Multiple-Perspective Semantics-Crossover Model for Matching Sentences

论文地址：https://ieeexplore.ieee.org/document/8710322
![avatar](https://ieeexplore.ieee.org/mediastore_new/IEEE/content/media/6287639/8600701/8710322/peng2-2915937-large.gif)
模型效果还可以，具体见论文，欢迎批评指正哦，也欢迎引用。


## my_first_keras_programe
论文实验的一些初步想法和初始模型。


## my_paper_figures
用来绘画论文中一些图。


## my_paper_model
论文实验的一些初步想法和模型


## pca
使用pca算法降维，也是当时做论文的一个想法


## 实验结果quora
论文模型的一些实验结果数据


## 总结
正真要做学术还是要下很大功夫的，做一个有效果的模型出来，前前后后经历了两个学期的实验，花了大量的功夫和时间，不容易啊。
毕业了，找时间总结下。也把自己所做的东西分享出来，做实验的过程本就借鉴了很多大神的工作，巨人的肩膀上。感谢！！！
