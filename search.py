import urllib2
import urllib
from threading import Thread
from HTMLParser import HTMLParser
import re
import csv
import time



class TagStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self,data):
		self.fed.append(data)
	def get_data(self):
		return " ".join(self.fed)
	def flush_buffer(self):
		self.fed = []

def searchManga(manga):
	parser = TagStripper()
	url = 'https://www.mangaupdates.com/search.html'	
	values = {'search' : manga,'stype':'title'}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	parse = re.search("https://www.mangaupdates.com/series\.html\?id=[0-9]+",the_page);
	if(parse != None):
		#releasesLink = buildReleasesPage(parse.group(0))
		releasesLink = seriesIdToReleases("60271")
		releasesPage = getPage(releasesLink)
		releases = buildReleasesTable(releasesPage,parser);
		print(releases);
		
def searchReleases(id):
	releases = True
	page = 1
	parser = TagStripper()
	while releases:
		releasesLink = seriesIdToReleases(id,page)
		releasesPage = getPage(releasesLink)
		releases = buildReleasesTable(releasesPage,parser);
		print(releases);
		page = page + 1
	
		
def seriesIdToReleases(seriesId,page=1):
	page = str(page)
	base = "https://www.mangaupdates.com/releases.html?page="+page
	base = base +"&search="
	end = "&stype=series"
	return base + seriesId + end
	

def buildReleasesPage(homeUrl,page=1):
	#print(home_url)
	base = "https://www.mangaupdates.com/releases.html?page="+page
	base = base +"&search="
	seriesId = findSeriesID(homeUrl)
	end = "&stype=series"
	return base + seriesId + end
	
	
def buildReleasesTable(page,parser):
	iterr = re.finditer("<td class='text pad'(.)*</td>",page)
	index = 0
	row = []
	try:
		iterr.next().start(0)
	except Exception, e:
		return False
	for m in iterr:
		releaseNode = page[m.start(0):m.end(0)]
		release = stripTags(releaseNode,parser)
		row.append(release)
		index = index + 1
		if(index == 5):
			with open('test.csv','a') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(row)
			print(row)
			row = []
		index = index % 5
	return True
	
def stripTags(node,parser):
	parser.feed(node)
	data = parser.get_data()
	parser.flush_buffer()
	return data

def findSeriesID(a):
	return a.split("id=")[1]

def getPage(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	return response.read()
	


threads = []
releases = ["1","2","3","4","5"]
t0 = time.time()
for i in range(5):
	t = Thread(target=searchReleases, args=(releases[i],))
	threads.append(t)
	t.start()
	
threads[0].join()
threads[1].join()
threads[2].join()
threads[3].join()
threads[4].join()
print("Finished in: ")
print time.time() - t0