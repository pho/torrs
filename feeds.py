import feedparser
import re
import urllib

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


for key in sources.keys():
  f = feedparser.parse(urllib.request.urlopen(sources[key]))
  for item in f['items']:
    print(item['title'])
    print(item['link'])

