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
	
	
def buildReleasesTable(page,parser):
	#Find table of releases
	iterr = re.finditer("<td class='text pad'(.)*</td>",page)
	header = 0
	row = []
	try:
		#If there is a release
		iterr.next().start(0)
	except Exception, e:
		return False
	for m in iterr:
		#For each table element strip it and add it to the list
		releaseNode = page[m.start(0):m.end(0)]
		release = stripTags(releaseNode,parser)
		row.append(release)
		header = header + 1
		#Dump the list to csv after we get the release info
		if(header == 5):
			with open('test.csv','a') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(row)
			row = []
		header = header % 5
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