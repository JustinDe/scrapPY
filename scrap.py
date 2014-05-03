from lxml import html
from urlparse import urlparse
import requests

urlsMaster = []
titles = []
h1s = []
h2s = []

seedPage = 'http://philhoyt.com'
parsed_uri = urlparse(seedPage)
seedDomain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
curPage = requests.get(seedPage)
tree = html.fromstring(curPage.text)
urls = tree.xpath('//a/@href')

def buildURLMaster(linkArray):
	global urlsMaster
	for itm in linkArray:
		parsed_uri = urlparse(itm)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		if domain == seedDomain:
			urlsMaster.append(itm)

def buildDics(linkArray):
	global titles, h1s, h2s
	titles = dict.fromkeys(linkArray,[])
	h1s = dict.fromkeys(linkArray,[])
	h2s = dict.fromkeys(linkArray,[])

def pageScrape(inLink):
	global titles
	transLink = inLink
	curPage = requests.get(inLink)
	tree = html.fromstring(curPage.text)
	titles[inLink].append(tree.xpath('//title/text()'))
	h1s[inLink].append(tree.xpath('//h1/a/text()'))
	h1s[inLink].append(tree.xpath('//h1/text()'))
	h2s[inLink].append(tree.xpath('//h2/a/text()'))
	h2s[inLink].append(tree.xpath('//h2/text()'))
	
def linkStep(linkArray):
	for itm in linkArray:
		pageScrape(itm)

buildURLMaster(urls)
buildDics(urlsMaster)
linkStep(urlsMaster)

print "titles: " + str(titles)
print "\n"
print "h1s: " + str(h1s)
print "\n"
print "h2s: " + str(h2s)