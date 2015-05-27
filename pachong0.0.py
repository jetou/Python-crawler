# encoding:utf-8
import urllib
import urllib2
import re

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
print u"版本：1.0"
print u"作者：jetou"
print u"说明：按照指令操作即可"
print "##############################################"
print u"##############开始############################"
booktypes = raw_input(u"请输入你要爬的书籍类型")
strs = unicode(booktypes, 'gbk') #windows输入的是GBK编码先转换为unicode
strs = strs.encode('UTF-8') #再将unicode转换为UTF-8
types = urllib.quote(strs)

bookpage = input(u"请输入你要爬的书籍页数")
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