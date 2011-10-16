import sys
from time import sleep
from PyQt4 import QtGui
from PyQt4 import QtCore


class Item(QtGui.QFrame):
  def __init__(self):
    super(Item, self).__init__()
    self.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Raised)

    layout = QtGui.QHBoxLayout(self)
    
    layout.addWidget(QtGui.QRadioButton("Yeah"))
    layout.addWidget(QtGui.QPushButton("Add"))

class ItemList(QtGui.QListWidget):
  def __init__(self):
    super(ItemList, self).__init__()

class Window(QtGui.QWidget):
  def __init__(self):
    super(Window, self).__init__()
    self.setGeometry(100, 100, 300, 600)
    self.setWindowTitle("lol")

    self.layout = QtGui.QAbstractScrollArea(self)

    self.box = QtGui.QBoxLayout(QtGui.QBoxLayout.Direction(2), self)

    self.box.addWidget(Item())
    self.box.addWidget(Item())
    self.box.addWidget(Item())
    self.box.addWidget(Item())
    self.box.addWidget(Item())
    self.box.addStretch()

    self.addButton = QtGui.QPushButton("Add button!")
    self.addButton.clicked.connect(self.add)


  def add(self):
    print("Click!")
    self.box.addWidget(Item())


def main():
  app = QtGui.QApplication(sys.argv)
  w = Window()
  w.show()
  sys.exit(app.exec_())

main()
