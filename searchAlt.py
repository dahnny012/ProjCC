# This is a branch of the original search.py
# This version creates a directory for the scrape
# that contains the log/badID files
# and subdirectories for each series ID
# This is less visually helpful than the original output
# but it should help us "index" the result when we need them later

# Multithreaded MangaUpdates scraper
# Checks whether each series id is valid
# Takes the series name from the series page
# Pulls release information from the release pages

# Encodes data in UTF-8, wraps it in double-quotes, delimits it with commas
# Writes to a csv with the same name as the input file

# Accepts any number of input files as command line arguments
# If no arguments are given, it defaults to "uniqueSeries.txt"
# It expects input files to be plain-text with one series ID per line	

import urllib
import threading
from HTMLParser import HTMLParser
import re
import time
import sys, os
# codecs allows us to write to files in UTF-8
# It is unfortunately incompatible with the csv library
import codecs
# repairUnicode is an outside library (recipe?) I ripped
import repairUnicode

queueLock = threading.Lock()
logLock = threading.Lock()
errorLock = threading.Lock()

extReg     = re.compile('\.[A-Za-z]+$')
nameReg    = re.compile('(?<=<title>Baka\-Updates Manga \- ).+(?=</title>)')
releaseReg = re.compile('<td class=\'text pad\'.*?</td>')
nodeReg    = re.compile('(?<=>).*?(?=<)')

# NOTE: groupReg contains two parenthesized groups
# so we can call group(0) for the entire match,
# or group(1) for the gID and group(2) for the gName
groupReg   = re.compile("((?<=id=)[0-9]+)\' title=\'Group Info\'>(.*?(?=</a>))")


class search():
	def __init__(self, idList=None):
		self.idList     = idList
		self.htmlParser = HTMLParser()
		self.filename   = "uniqueSeries.txt"
		self.dirname    = "uniqueSeries/"

	def readFile(self, filename=None):
		if filename == None:
			filename = self.filename
		with open(filename, 'r') as file:
			self.idList = [line.rstrip('\n') for line in file]
		print("File: %s" % filename)
		self.filename = extReg.sub('', filename)

		# Create the directory if necessary
		# If you want to make a separate directory for each call on the same input
		# You need to change checkFilename as well
		self.dirname  = self.filename + "/"
		if not os.path.exists(self.dirname):
			os.makedirs(self.dirname)

		# Check if the log already exists and append a number to the filename
		self.filename = self.checkFilename(self.filename, "_log.txt")

	# Multithread and wait for them to finish executing
	def run(self):
		t0 = time.time()

		threads = []
		numThreads = 20
		for i in range(numThreads):
			t = threading.Thread(target=self.searchReleases, args=(self.idList,))
			threads.append(t)
			t.start()
		for thread in threads:
			thread.join()

		print("Finished in: %s" % (time.time() - t0))

	# Worker-threads
	def searchReleases(self, idList):
		while True:
			with queueLock:
				try:
					sId = idList.pop()
				except:
					return

			# Hurray for weak typing
			sName = self.checkExists(sId)

			if sName != False:
				releases = True
			else:
				releases = False

			page = 1
			curwd = self.dirname + str(sId) + "/"

			if not os.path.exists(curwd):
				os.makedirs(curwd)
			self.clearFile(curwd + self.filename + ".csv")
			self.writeRow(curwd + self.filename + ".csv", ["SERIES_ID", "SERIES_NAME", "VOLUME", "CHAPTER", "GROUP_NAME", "GROUP_ID"])
			while releases:
				releasesLink = self.seriesIdToReleases(sId, page)
				releasesPage = self.getPage(releasesLink)
				releases = self.buildReleasesTable(releasesPage, sId, sName);
				page += 1
			self.lockWrite(sId, logLock, "_log.txt")
			
	# "An abstraction to hide stuff"
	def seriesIdToReleases(self, sId, page=1):
		page = str(page)
		URL = "https://www.mangaupdates.com/releases.html?page=" + page +"&search=" + sId + "&stype=series"
		return URL

	# Open and close
	def clearFile(self, filename):
		file1 = open(filename, 'w')
		file1.close()

	# If the filename already exists, append a number
	def checkFilename(self, filename, fileExt):
		if os.path.isfile(self.dirname + filename + fileExt):
			count = 0
			while True:
				count += 1
				countStr = str(count)
				if not os.path.isfile(self.dirname + filename + countStr + fileExt):
					return filename + countStr
		else:
			return filename

	# Return the series name from the sId
	# If the page doesn't exist, log it and return False
	def checkExists(self, sId):
		url = "https://www.mangaupdates.com/series.html?id=" + sId
		page = self.getPage(url)
		name = nameReg.search(page)
		if name != None:
			sName = name.group(0)
			return sName
		else:
			print("Bad series ID: " + sId)
			self.lockWrite(sId, errorLock, '_bad.txt')
			return False

		return False
		
	# Scrape one page of releases
	def buildReleasesTable(self, page, sId, sName = None):
		# Converting to a list is an easy way to check len()
		nodes = list(re.finditer("<td class='text pad'(.)*</td>",page))

		if len(nodes) != 0:
			header = 0
			row = [sId]

			# For each table element strip it and add it to the list
			for node in nodes:
				header += 1

				# Skip date
				if header == 1:
					continue
				# Use the name from the series page, not the releases page
				elif header == 2:
					row.append(sName)
				elif header < 5:
					releaseNode = node.group(0)
					release = self.stripTags1(releaseNode)
					row.append(release)

				# header==5 represents the last node in MangaUpdates's table row
				# This means, 1) We call stripTags2 for gNames and gIDs, and
				# 2) We write to the output csv
				elif header == 5:
					releaseNode = node.group(0)
					release = self.stripTags2(releaseNode)

					# Check for cases with group name, but without group id
					if release != False:
						row.extend(release)
					else:
						row.append(self.stripTags1(releaseNode))
					
					self.writeRow(self.dirname + str(sId) + "/" + self.filename + '.csv', row)

					row = [sId]
					header = 0
				else:
					print("header in buildReleasesTable out of range: %d" % header)
					return False
			return True
		else:
			return False

  # Mimic csv.writer().writeRow(), since csv isn't compatible with codecs.open()
	def writeRow(self, filename, row):
		row = [self.encodeStr(item) for item in row]
		rowStr = ",".join(row) + '\n'
		with codecs.open(filename, 'a', 'utf-8') as outFile:
			outFile.write(rowStr)

	# Isolate text from a tr element
	def stripTags1(self, node):
		node = nodeReg.search(node)
		outStr = node.group(0)
		return outStr

	# Isolate group names and ids from a tr element
	def stripTags2(self, node):
		nodes  = list(groupReg.finditer(node))
		if len(nodes) == 0:
			return False
		gIDs   = []
		gNames = []
		outArr = []

		for node in nodes:
			currNum = node.group(1)
			gIDs.append(currNum)
			gNames.append(node.group(2))

		outArr.append(" & ".join(gNames))
		outArr.extend(gIDs)

		return outArr

	# Encode to UTF to wrap the string, then decode back out and repair junk unicode
	def encodeStr(self, inStr):
		try:
			outStr = inStr.encode('utf-8')
			if outStr.find('"') != -1 or outStr.find(',') != -1:
				outStr = outStr.replace('"', '""')
				outStr = '"' + outStr + '"'
			
			outStr = outStr.decode('utf-8')
			outStr = repairUnicode.fix_bad_unicode(outStr)
		except:
			print("Failure to encode: %s" % inStr)
			return ""
		return outStr
	
	def getPage(self, url, recur=0):
		try:
			response = urllib.urlopen(url)
			page = response.read()
		except:
			# It's all good, just keep trying.
			recur += 1
			print("No response. Retry #%d on\n %s" % (recur, url))
			return self.getPage(url, recur)

		try:
			# Decode latin-1 and unescape HTML entities like &lt;
			page = page.decode('iso-8859-1')
			page = self.htmlParser.unescape(page)
		except:
			print("Failure to encode: %s" % url)

		return page

	def lockWrite(self, sId, lock, fileExt):
		with lock:
			with open(self.dirname + self.filename + fileExt, 'a') as outFile:
				outFile.write(sId + "\n")

# Script execution
# Check for commandline arguments
scraper = search()
argLen = len(sys.argv)
if argLen > 1:
	for i in range (1, argLen):
		scraper.readFile(sys.argv[i])
		scraper.run()
else:
	print ("Usage: 'python search.py <filename> [<filename 2> ... <filename n>]'")
	print "Default",
	scraper.readFile()
	scraper.run()
