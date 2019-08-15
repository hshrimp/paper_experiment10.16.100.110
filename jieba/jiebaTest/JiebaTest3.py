#coding=utf-8
import time
import jieba
jieba.enable_parallel(16)

#url = '/home/wshong/Desktop/wiki数据/testsplit/按数据量100M切分/wiki_bysize_ad.txt'
meragefiledir = '/home/wshong/Downloads/wikiextractor-master/extracted/AA'
content = open(meragefiledir+'/5按4760000行划分成2个文档/wiki_newab',"r").read()
# count=0
# for line in content:
#     count+=1
#     if((count>=4760000)&(line.strip()=='')):
#         print count
#         break
#print content
t1 = time.time()
words = list(jieba.cut(content))

t2 = time.time()
tm_cost = t2-t1

log_f = open(meragefiledir+"/wikinew2.txt","w")
for w in words:
    #print 'word=',w,'====================='
    if cmp(w,'\r\n')==0:
        print >> log_f
    else:
        print >> log_f, w.encode("utf-8"), " " ,

log_f.close()

print 'speed' , len(content)/tm_cost, " bytes/second",tm_cost