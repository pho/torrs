import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import feedparser, urllib


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
    msg.setIcon(1) # X Error (?)
    msg.setText(i.title)
    msg.setDetailedText("Torrent: {}\n\nInfo: {}".format(i.torrent, i.div))
    msg.addButton("Cancel", 1)
    msg.addButton("Download!", 0)
    
    if msg.exec_() == 1:
      print("ACTION!")


def main():
  app = QtGui.QApplication()
  w = Window()
  w.show()
  w.textedit.setText("no horizon")
  sys.exit(app.exec_())

main()

