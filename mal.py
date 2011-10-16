import sys
from time import sleep
from PyQt4 import QtGui
from PyQt4 import QtCore


from feeds import NyaaSearcher

class ItemList(QtGui.QListWidgetItem):
  def __init__(self, title, torrent):
    super(ItemList, self).__init__()
    self.title = title
    self.torrent = torrent

    self.setText(title)
    self.setToolTip(torrent)



class Window(QtGui.QWidget):
  def __init__(self):
    super(Window, self).__init__()
    self.setGeometry(100, 100, 600, 600)
    self.setWindowTitle("lol")

    self.textedit = QtGui.QLineEdit()
    self.buscador = QtGui.QComboBox()
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
    n = NyaaSearcher()
    for i,t in n.search(self.textedit.text()):
      self.lista.addItem(ItemList(i, t))

  def selected(self, i):
    print(i.torrent)


def main():
  app = QtGui.QApplication(sys.argv)
  w = Window()
  w.show()
  sys.exit(app.exec_())

main()
