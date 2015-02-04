import urllib2
import urllib
from multiprocessing import Pool
from HTMLParser import HTMLParser
import re
##
##pool = Pool(10)
##p.map(getChapters,[[0,100],[0,200]])

#def getChapters(start,stop)
	# Define a start and stop
	# till N
#	for chapter in list:
#		results = searchManga(chapter)
#		scanner = parseResults(results)


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
		if(tag == "td"):
			for attr in attrs:
				if(attr[1] == "text pad"):
					print(attr)
			
        
 
parser = MyHTMLParser()

def searchManga(manga):
	url = 'https://www.mangaupdates.com/search.html'	
	values = {'search' : manga,'stype':'title'}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	parse = re.search("https://www.mangaupdates.com/series\.html\?id=[0-9]+",the_page);
	if(parse != None):
		releases = buildReleasesPage(parse.group(0))
		releases_page = getPage(releases)
		parser.feed(releases_page)
		#should write to a csv but well print for now
		
		
def buildReleasesPage(home_url):
	#print(home_url)
	base = "https://www.mangaupdates.com/releases.html?search="
	seriesId = findSeriesID(home_url)
	end = "&stype=series"
	return base + seriesId + end
	
def findSeriesID(a):
	return a.split("id=")[1]

def getPage(url):
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	return response.read()
results = searchManga("kiss")

#parseResults(results)
