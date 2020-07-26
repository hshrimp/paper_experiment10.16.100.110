# import sys
# print sys.path
# # sys.path.append('../')
# print sys.path
import jieba
import jieba.analyse
from optparse import OptionParser

# USAGE = "usage: python extract_tags.py [userdict.txt] -k [top k]"
#
# parser = OptionParser(USAGE)
# parser.add_option("-k", dest="topK")
# opt, args = parser.parse_args()
# print ('parser= ',parser)
# print 'opt=',opt
# print 'args=',args
# if len(args) < 1:
#     print 'usage=',USAGE
#     sys.exit(1)
#
# file_name = args[0]
#
# if opt.topK is None:
#     topK = 10
# else:
#     topK = int(opt.topK)

content = open('userdict.txt', 'rb').read()
print(' content=', content)
tags = jieba.analyse.extract_tags(content, topK=2)

print ",".join(tags)
