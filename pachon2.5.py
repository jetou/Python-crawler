# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

class book:     #豆瓣书籍的类
	def __init__(self, types, page):
		self.baseUrl = 'http://www.douban.com/tag/'
		self.types = types
		self.filename = 'doubanbook.txt'
		self.page = page

	def getContents(self): #爬取源代码
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

	def writetext(self, items): #写入txt
		for item in items:
			print item[0],item[1]
			files = open(self.filename,'a')
			files.write(item[0])
			files.write(item[1])
			files.write('\n')
			files.close()

	def strat(self): #启动函数
		self.writetext(self.getContents())
		print u"""出现乱码为正常现象，在与本脚本相同的文件夹下会多出一个,
doubanbook.txt的文件里面有所爬书籍，如你把本脚本放在桌面,
文件便会出现在桌面"""
		print u"结束输入 'O' , 联系作者输入 'A'"
		end = raw_input('>')
		if end == 'A':
			print u"QQ邮箱:1021644861@qq.com"
			raw_input('>')
		else:
			print "over"

#------------------------------------------------class-------------------------

class movie:     #豆瓣近期热门电影的类
	def __init__(self):
		self.baseUrl = 'http://movie.douban.com/chart'
		self.filename = 'doubanmovie.txt'

	def gethtml(self):
		try:
			url = self.baseUrl
			user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
			headers = { 'User-Agent' : user_agent }
			request = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(request)
			content = response.read()
			pattern = re.compile('<a class="nbg".*?title=(.*?)>.*?<span style=.*?>(.*?)</span>.*?<p class="pl">(.*?)</p>.*?<span class="rating_nums">(.*?)</span>',re.S)
			items = re.findall(pattern, content)
			return items
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"豆瓣链接错误，错误原因", e.reason
				return None

	def gettext(self,items): #写入txt
		for item in items:
			print item[0],item[1],item[2]
			files = open(self.filename,'a')
			files.write(item[0])
			files.write(item[1])
			files.write('\n')   #在写入的文件中加入换行符
			files.write(item[2])
			files.write('\n')
			files.write("评分")
			files.write(item[3])
			files.write('\n\n')
			files.close()

	def strat(self):
		self.gettext(self.gethtml())
		print u"近期热门的新电影爬取完毕，是否需要获取书籍。"
		print u"输入任意键结束，'V'爬取书籍"
		fir = raw_input('>')
		if fir == 'V':
			bookstyle()
		else:
			print "over"

#-------------------class---------------------------------------------------

class TOPmove:   #豆瓣总电影top类
	def __init__(self, page):
		self.baseurl = 'http://movie.douban.com/top250?start='
		self.page = page
		self.filename = 'dbTOPmove.txt'

	def html(self):
		try:
			url = self.baseurl + str(self.page) + '&filter=&type='
			user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'
			headers = { 'User-Agent' : user_agent }
			request = urllib2.Request(url, headers = headers)
			response = urllib2.urlopen(request)
			content = response.read()
			pattern = re.compile('<em.*?class="">(.*?)</em>.*?<span.*?class="title">(.*?)</span>.*?<p.*?class="">\s(.*?)<br>.*?\s(.*?)</p>.*?<em>(.*?)</em>.*?<span.*?class="inq">(.*?)</span>', re.S)
			items = re.findall(pattern, content)
			return items
		except urllib2.URLError, e:
			if hasattr(e, "reason"):
				print u"豆瓣链接错误，错误原因", e.reason
				return None

	def wtext(self,items):
		remove = re.compile('&nbsp| {4}|;')  #在获取的排名中去除 &nbsp ； 空格
		for item in items:
			print (' '.join(map(lambda s: re.sub(remove,'',s),item)))
			files = open(self.filename,'a')
			files.write((' '.join(map(lambda s: re.sub(remove,'',s),item))))
			files.write('\n')
			files.write('\n')
			files.close()

	def strat(self):
		self.wtext(self.html())
		print u"豆瓣电影TOP爬取完毕"
		print u"输入任意键结束，'V'爬取书籍"
		fir = raw_input('>')
		if fir == 'V':
			bookstyle()
		else:
			print "over"




#---------------------------------------------------------------book--
def bookstyle():    #豆瓣爬取得书籍目录
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
		print"###################################"
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
	script = book(types,page)
	script.strat()
#-------------------------------------------movies----------------------------

def optmove():    #选择要爬热门还是top
	print u"你想爬近期热门电影还是总电影top？"
	print u"热门电影输入 'H', 总TOP输入 'T'"
	opt = raw_input('>')
	while opt != 'H' and opt != 'T':
		print u"输入有误，热门电影输入 'H', 总TOP输入 'T'"
		opt = raw_input('>')
	if opt == "H":
		moviestyle()
	else:
		topmove()

def topmove():
	print u"获取豆瓣电影TOP250"
	print u"每页top25部影，共10页要爬第几页？"
	pages = input(">")
	if pages == 1:
		page = 0
	elif pages > 1 and pages <= 10:
		page = (pages - 1) * 25
	else:
		page = (10 - 1) * 25
	topmove = TOPmove(page)
	topmove.strat()

def moviestyle():
	print u'获取热门新片排行'
	movies = movie()
	movies.strat()

#--------------------------------------------start-----------------------------
print "##############################################"
print u"名字：豆瓣图书电影爬虫机器人"
print u"版本：2.0"
print u"作者：jetou"
print u"说明：按照指令操作即可"
print u"功能：输入豆瓣图书和电影的分类和页数爬取豆瓣书单并保存txt文件"
print "##############################################"
print u"要爬豆瓣书籍或者是豆瓣电影呢？'book' or 'movie'?"
classify = raw_input('book or movie?')
while classify != 'book' and classify != 'movie' :   #if not book or movie
	print u"无效指令请输入book or movie"
	classify = raw_input('>')
if classify == 'book':
	bookstyle()
else:
	optmove()



# except urllib2.URLError, e:
# 	if hasattr(e,"code"):
# 		print e.code
# 	if hasattr(e,"reason"):
# 		print e.reason
