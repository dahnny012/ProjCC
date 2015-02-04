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
		print(attrs.index(1))
			
        
 
parser = MyHTMLParser()

def searchManga(manga):
	url = 'https://www.mangaupdates.com/search.html'
	values = {'search' : manga}
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	the_page = response.read()
	parse = re.search("https://www.mangaupdates.com/series\.html\?id=[0-9]+",the_page);
	if(parse != None):
		print(parse.group(0))
	# Navigate to parse
		url = parse.group(0)
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		print(response)
	
def parseResults(soup):
	results = soup.find_all('a');
	for link in results:
		if 'key1' in link.keys():
			print(link['title'])
	return 1
	
		
results = searchManga("sdfsdfsdfd")
#parseResults(results)
