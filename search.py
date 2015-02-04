import urllib2
import urllib
from multiprocessing import Pool
from HTMLParser import HTMLParser

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
	print(attrs)
			
        
 
parser = MyHTMLParser()

def searchManga(manga):
	url = 'https://www.mangaupdates.com/search.html'
	values = {'search' : manga}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	soup = parser.feed(the_page)
	return soup
	
def parseResults(soup):
	results = soup.find_all('a');
	for link in results:
		if 'key1' in link.keys():
			print(link['title'])
	return 1
	
		
results = searchManga("Ao haru ride")
#parseResults(results)
