import urllib2
import urllib
from bs4 import BeautifulSoup

url = 'https://www.mangaupdates.com/search.html'
values = {'search' : 'ao haru ride'}
data = urllib.urlencode(values)
req = urllib2.Request(url, data)

response = urllib2.urlopen(req)
the_page = response.read()

soup=BeautifulSoup(the_page)

print(soup.body)
