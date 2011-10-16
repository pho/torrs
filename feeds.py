import feedparser
import re
import urllib


class NyaaSearcher():
  def search(self, term):
    print("Searching nyaa.eu for {}".format(term))

    offset = 1
    f = feedparser.parse(urllib.request.urlopen('http://www.nyaa.eu/?page=rss&term={0}&offset={1}'.format(term, offset)))
    print(f['items'])
    while len(f['items']) > 0:
      for item in f['items']:
        yield item['title'], item['link']
      offset += 1
      f = feedparser.parse(urllib.request.urlopen('http://www.nyaa.eu/?page=rss&term={0}&offset={1}'.format(term, offset)))


sources = {
    'inshuheki' : 'http://www.nyaa.eu/?page=rss&user=84109',
    }

series = []

class Serie:
  __slots__ = ["nombre", "editores", "temporada", "capitulo"]

  def __init__(self, nombre, temporada=1, capitulo=1, editores=[]):
    self.nombre = nombre
    self.temporada = temporada
    self.capitulo = capitulo
    self.editores = editores

  def ultimocap(self):
    return (self.temporada, self.capitulo)

series.append(Serie('Horizon', editores=['inshuheki', 'noone']))


#for key in sources.keys():
#  f = feedparser.parse(urllib.request.urlopen(sources[key]))
#  for item in f['items']:
#    print(item['title'])
#    print(item['link'])

if __name__ == '__main__':
  n = NyaaSearcher()
  for a in n.search('inshuheki'):
    print(a)

