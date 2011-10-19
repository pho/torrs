import sys

try:
  from PyQt4 import QtGui
  from PyQt4 import QtCore
except:
  print("PyQt4 module missing!")
  sys.exit(-1)

try:
  import feedparser
except:
  print("feedparser module missing!")
  sys.exit(-1)

try:
  import urllib
except:
  print("urrlib module missing!")
  sys.exit(-1)

try:
  from actions import * 
except:
  print("[W] There is no actions defined in actions.py"

######### Search Engines ########
## return title, torrent, info ##

def Nyaa(term):
    #print("Searching nyaa.eu for {}".format(term))
    offset = 1
    f = feedparser.parse(urllib.request.urlopen('http://www.nyaa.eu/?page=rss&term={0}&offset={1}'.format(term, offset)))
    while len(f['items']) > 0:
      for item in f['items']:
        yield item['title'], item['link'], item['summary']
      offset += 1
      f = feedparser.parse(urllib.request.urlopen('http://www.nyaa.eu/?page=rss&term={0}&offset={1}'.format(term, offset)))

## Add engine here

sources = { 'nyaa.eu' : Nyaa , 'frozen-layer' :  Nyaa }

############################ GUI

class ItemList(QtGui.QListWidgetItem):
  def __init__(self, title, torrent, div):
    super(ItemList, self).__init__()
    self.title = title
    self.torrent = torrent
    self.div = div

    self.setText(title)
    self.setToolTip(torrent)

    size = self.sizeHint()
    size.setHeight(25)
    self.setSizeHint(size)

class Window(QtGui.QWidget):
  def __init__(self):
    super(Window, self).__init__()
    self.setGeometry(100, 100, 600, 600)
    self.setWindowTitle("Torrent Finder")

    self.textedit = QtGui.QLineEdit()
    self.buscador = QtGui.QComboBox()
    for k in sources:
      self.buscador.addItem(k, sources[k])
    self.botonBuscar = QtGui.QPushButton("Q")
    self.botonBuscar.clicked.connect(self.buscar)

    header = QtGui.QHBoxLayout()
    header.addWidget(self.textedit)
    header.addWidget(self.buscador)
    header.addWidget(self.botonBuscar)

    self.lista = QtGui.QListWidget(self)
    self.lista.itemClicked.connect(self.selected)

    box = QtGui.QVBoxLayout()
    box.addLayout(header)
    box.addWidget(self.lista)

    self.setLayout(box)

  def add(self):
    print("Click!")
    self.box.addWidget(Item())

  def buscar(self):
    self.lista.clear()
    self.lista.scrollToTop()
    for i,t,d in sources[self.buscador.currentText()](self.textedit.text()):
      self.lista.addItem(ItemList(i, t, d))

  def selected(self, i):
    msg = QtGui.QMessageBox()
    msg.setWindowTitle("Torrent Selected!")
    msg.setIcon(1) # X Error (?)
    msg.setText(i.title)
    msg.setDetailedText("Torrent: {}\n\nInfo: {}".format(i.torrent, i.div))
    msg.addButton("Cancel", 1)
    msg.addButton("Download!", 0)
    
    if msg.exec_() == 1:
      # Add to actions.py the method you want to call when "download" is selected
      download(i)


def main():
  app = QtGui.QApplication(sys.argv)
  w = Window()
  w.show()
  w.textedit.setText("no horizon")
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()

