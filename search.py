import urllib2
import urllib
from bs4 import BeautifulSoup
from multiprocessing import Pool


pool = Pool(10)
p.map(getChapters,[[0,100],[0,200]])

def getChapters(start,stop)
	# Define a start and stop
	# till N
	for chapter in list:
		results = searchManga(chapter)
		scanner = parseResults(results)
	
		



def searchManga(manga):
	url = 'https://www.mangaupdates.com/search.html'
	values = {'search' : manga}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	soup=BeautifulSoup(the_page)
	return soup
	
def parseResults(soup):
	# Look for results
	# Record them
	# do somethign with them
	return 1
	
