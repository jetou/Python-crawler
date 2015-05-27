# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class douban:
	def __init__(self, types, page):
		self.baseUrl = 'http://www.douban.com/tag/'
		self.types = types
		self.filename = 'doubanbook.txt'
		self.page = page

	def getContents(self):
		try:
			#if self.page == 0:
			url = self.baseUrl + self.types + '/book'
			#else:
			#	url = self.baseUrl + self.types + '/book?start=' + str(self.page)
			user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.65 Safari/537.36'
			headers = { 'User-Agent' : user_agent}
			request = urllib2.Request(url,headers = headers)
			response = urllib2.urlopen(request)
			content = response.read()  #.decode('utf-8')
			pattern = re.compile('<a href=.*?class="title".*?target="_blank">(.*?)</a>.*?>(.*?)</div>',re.S)
			items = re.findall(pattern,content)
			return items
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"豆瓣链接错误，错误原因", e.reason
				return None

	def writetext(self, items):
		for item in items:
			print item[0],item[1]
			files = open(self.filename,'a')
			files.write(item[0])
			files.write(item[1])
			files.write('\n')
			files.close()

	def strat(self):
		items = script.getContents()
		script.writetext(items)


print "##############################################"
print u"名字：豆瓣图书爬虫机器人"
print u"版本：1.2"
print u"作者：jetou"
print u"说明：按照指令操作即可"
print u"功能：输入豆瓣图书的分类和页数爬取豆瓣书单并保存txt文件"
print "##############################################"
print u"请输入你要爬的书籍类型,查看所有类型输入 'V' "
booktypes = raw_input(u">")
while booktypes == 'V':
	print "###########################################"
	print   u"小说	外国文学	文学	随笔"
	print   u"中国文学	经典	散文	日本文学"
	print   u"村上春树	童话	诗歌	杂文"
	print   u"王小波	张爱玲	儿童文学	古典文学"
	print	u"余华	名著	钱钟书	当代文学"
	print	u"鲁迅	外国名著	诗词	茨威格"
	print	u"米兰·昆德拉	杜拉斯	港台"
	print	u"流行 · · · · · ·"
	print	u"                              "
	print	u"漫画	绘本	推理	青春"
	print	u"言情	科幻	悬疑	东野圭吾"
	print	u"武侠	韩寒	奇幻	日本漫画"
	print	u"耽美	亦舒	三毛	安妮宝贝"
	print	u"网络小说	郭敬明	穿越	推理小说"
	print	u"金庸	轻小说	几米	阿加莎·克里斯蒂"
	print	u"幾米	张小娴	魔幻	青春文学"
	print	u"J.K.罗琳	高木直子	沧月	古龙"
	print	u"科幻小说	落落	张悦然	蔡康永"
	print	u"文化 · · · · · ·"
	print	u"                              "
	print	u"历史	心理学	哲学	传记"
	print	u"文化	社会学	设计	艺术"
	print	u"政治	社会	建筑	宗教"
	print	u"电影	数学	政治学	回忆录"
	print	u"思想	国学	中国历史	音乐"
	print	u"人文	戏剧	人物传记	绘画"
	print	u"艺术史	佛教	军事	西方哲学"
	print	u"近代史	二战	自由主义	考古"
	print	u"美术"
	print	u"生活 · · · · · ·"
	print   u"                              "
	print	u"爱情	旅行	生活	励志"
	print	u"成长	摄影	心理	女性"
	print	u"职场	美食	游记	教育"
	print	u"灵修	情感	健康	手工"
	print	u"养生	两性	家居	人际关系"
	print	u"自助游"
	print	u"经管 · · · · · ·"
	print
	print	u"经济学	管理	经济	金融"
	print	u"商业	投资	营销	理财"
	print	u"创业	广告	股票	企业史"
	print	u"策划"
	print	u"科技 · · · · · ·"
	print   u"                            "
	print	u"科普	互联网	编程	科学"
	print	u"交互设计	用户体验	算法	web"
	print	u"科技	UE	通信	UCD"
	print	u"交互	神经网络	程序"
	print "###########################################"
	booktypes = raw_input(u">")
strs = unicode(booktypes, 'gbk') #windows输入的是GBK编码先转换为unicode
strs = strs.encode('UTF-8') #再将unicode转换为UTF-8
types = urllib.quote(strs)

print u"请输入你要爬的书籍排名页数(TOP15一页)"
bookpage = input(u">")
if bookpage == 1:
	page = 0
else:
	page = (bookpage - 1) * 15

script = douban(types,page)
script.strat()




# except urllib2.URLError, e:
# 	if hasattr(e,"code"):
# 		print e.code
# 	if hasattr(e,"reason"):
# 		print e.reason