# Since you have ID's this is unneeded
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
		releasesLink = buildReleasesPage(parse.group(0))
		releasesPage = getPage(releasesLink)
		releases = buildReleasesTable(releasesPage,parser);
		print(releases);
		
		
# Since you have ID's this is unneeded
def buildReleasesPage(homeUrl,page=1):
	#print(home_url)
	base = "https://www.mangaupdates.com/releases.html?page="+page
	base = base +"&search="
	seriesId = findSeriesID(homeUrl)
	end = "&stype=series"
	return base + seriesId + end