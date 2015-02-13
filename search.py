import urllib2
import urllib
import threading
from HTMLParser import HTMLParser
import re
import csv
import time


fileLock = threading.Lock()
queueLock = threading.Lock()
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

class search():
	def __init__(self,idList):
		self.idList = idList
	def run(self):
		threads = []
		t0 = time.time()
		numThreads = 3
		for id in range(0,numThreads):
			t = threading.Thread(target=self.searchReleases, args=(self.idList,))
			threads.append(t)
			t.start()
		for i in range(0,numThreads):
			threads[i].join()
		print("Finished in: ")
		print time.time() - t0
	def searchReleases(self,idList):
		exit = False
		with queueLock:
			try:
				id = idList.pop()
			except:
				exit = True
		if exit:
			return
		releases = True
		page = 1
		parser = TagStripper()
		while releases:
			releasesLink = self.seriesIdToReleases(id,page)
			releasesPage = self.getPage(releasesLink)
			releases = self.buildReleasesTable(releasesPage,parser);
			page = page + 1
		self.searchReleases(idList)
		
			
	def seriesIdToReleases(self,seriesId,page=1):
		page = str(page)
		base = "https://www.mangaupdates.com/releases.html?page="+page
		base = base +"&search="
		end = "&stype=series"
		return base + seriesId + end
		
		
	def buildReleasesTable(self,page,parser):
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
			release = self.stripTags(releaseNode,parser)
			row.append(release)
			header = header + 1
			#Dump the list to csv after we get the release info
			if(header == 5):
				with fileLock:
					with open('test.csv','a') as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow(row)
						csvfile.close()
					row = []
			header = header % 5
		return True
		
	def stripTags(self,node,parser):
		parser.feed(node)
		data = parser.get_data()
		parser.flush_buffer()
		return data
	
	def findSeriesID(self,a):
		return a.split("id=")[1]
	
	def getPage(self,url):
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		return response.read()
		
		
		
scraper = search(["1","2","3","4"])
scraper.run()
		
		
		
		
		
		
		
		
		
		
		
		
		