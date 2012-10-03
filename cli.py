import sys
from multiprocessing import Process
import re
import html.parser

try:
  import feedparser
except:
  print("feedparser module missing!")
  #sys.exit(-1)

try:
  import urllib
except:
  print("urrlib module missing!")
  sys.exit(-1)

######### Search Engines ########
## return title, torrent, info ##

def All(term):
  for i in sources:
    if i != "All":
      print("Search on: {}".format(sources[i].__name__))
      for e in sources[i](term):
        yield e

def Nyaa(term):
    #print("Searching nyaa.eu for {}".format(term))
    offset = 1
    f = feedparser.parse(urllib.request.urlopen('http://www.nyaa.eu/?page=rss&term={0}&offset={1}'.format(term, offset)))
    while len(f['items']) > 0:
      for item in f['items']:
        yield item['title'], item['link'], item['summary']
      offset += 1
      f = feedparser.parse(urllib.request.urlopen('http://www.nyaa.eu/?page=rss&term={0}&offset={1}'.format(term, offset)))

def FrozenLayer(term):
    #print("Searching nyaa.eu for {}".format(term))
    f = feedparser.parse(urllib.request.urlopen('http://www.frozen-layer.com/buscar/descargas/todos/{0}?page={1}'.format(term, offset)))
    while len(f['items']) > 0:
      for item in f['items']:
        yield item['title'], item['link'], item['summary']
      offset += 1
      f = feedparser.parse(urllib.request.urlopen('http://www.nyaa.eu/?page=rss&term={0}&offset={1}'.format(term, offset)))

def TokioToshokan(term):
  link = ""
  now = False
  l = []
  class MyParser(html.parser.HTMLParser):
    def __init__(self):
      html.parser.HTMLParser.__init__(self)
      self.now = False
    def handle_starttag(self, tag, attr):
      if tag == 'a' and ('type','application/x-bittorrent') in attr:
        for e in attr:
          if e[0] == 'href':
            self.link = e[1]
            self.now = True
    def handle_data(self, data):
      if self.now == True:
        self.now = False
    #   yield str(data), self.link, self.link
        l.append((data, self.link, self.link))
  p = MyParser()
  s = str(urllib.request.urlopen('http://www.tokyotosho.info/search.php?terms={0}&page={1}'.format(term.replace(" ", "%20"), 1)).read())
  p.feed(s)
  for e in l:
    yield e[0], e[1], e[2]

def Nanikano(term):
  link = ""
  now = False
  l = []
  reg = re.compile("(.*)download.php\?id=(.*)&f=(.*).torrent(.*)")
  for line in (urllib.request.urlopen('http://www.nanikano-fansub.net/trk/torrents.php?search={0}&category=0&active=1'.format(term, 1)).read()).decode("latin1").split("\n"):
    if reg.match(line):
      link = "http://www.nanikano-fansub.net/trk/download.php?id={0}&f={1}.torrent".format(reg.match(line).group(2), reg.match(line).group(3))
      yield urllib.parse.unquote(reg.match(line).group(3)).replace("+", " "), link, "-"

## Add engine here

sources = { 'All': All, 'nyaa.eu' : Nyaa , 'Tokio Toshokan': TokioToshokan, 'Nanikano' : Nanikano }

class Searcher():#QtCore.QThread):
	def __init__(self):
	  #QtCore.QThread.__init__(self) 
	  pass

	def search(self, what, where):
	  for e in sources[where](what):
	    yield e

if __name__ == '__main__':
  n = Searcher()
  for a in n.search(sys.argv[0],'Nanikano'):
    print(a)

