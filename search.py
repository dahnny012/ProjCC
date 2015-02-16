import urllib2
import urllib
import threading
from HTMLParser import HTMLParser
import re
import csv
import time
import io,os,sys


fileLock = threading.Lock()
queueLock = threading.Lock()
logLock = threading.Lock()
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
	def __init__(self,idList=None):
		self.idList = idList
		self.filename = "default"
	def readFile(self,filename):
		with open(filename, 'rb') as file:
			lines = [line.rstrip('\n') for line in file]
			self.idList = lines
		print("File: " + filename)
		self.filename = re.sub('\.[A-Za-z]+$', '', filename)
	def run(self):
		threads = []
		t0 = time.time()
		numThreads = 20
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
			releases = self.buildReleasesTable(releasesPage,parser,id);
			page = page + 1
		self.log(id)
		self.searchReleases(idList)
		
			
	def seriesIdToReleases(self,seriesId,page=1):
		page = str(page)
		base = "https://www.mangaupdates.com/releases.html?page="+page
		base = base +"&search="
		end = "&stype=series"
		return base + seriesId + end
		
		
	def buildReleasesTable(self,page,parser,id):
		#Find table of releases
		iterr = re.finditer("<td class='text pad'(.)*</td>",page)
		header = 0
		row = [id]
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
					with open(self.filename+'.csv','a') as csvfile:
						writer = csv.writer(csvfile)
						writer.writerow(row)
						csvfile.close()
					row = [id]
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
		#print("Creating request")
		req = urllib2.Request(url)
		#print("Attempting to open")
		response = urllib2.urlopen(req)
		#print("Attempting to read")
		page = response.read()
		return page
	def log(self,id):
		with logLock:
			with open(self.filename+".log",'a') as file:
				file.write(id + "\n")
				file.close()
	
scraper = search()
scraper.readFile("seriesIDs001.txt")
scraper.run()
		
		
		
		
		
		
		
		
		
		
		
		
		
