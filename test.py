from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon
from PyQt5.QtCore import Qt, QPoint, QSize

from PyQt5 import uic
import sys

class MyWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        self.initUI()

    def initUI(self):
        self.btn.setIcon(QIcon('smile-1.png'))
        print(dir(self.menuBar))
        dif = self.menuBar.addMenu('Сложность')
        dif.addAction('Новичок')
        dif.addAction('Любитель')
        dif.triggered[QAction].connect(self.print)

    def print(self, item):
        print(item.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
