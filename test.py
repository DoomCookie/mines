from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtWidgets import QButtonGroup

from PushButtonRight import PushButtonRight

from PyQt5 import uic
import sys

class MyWidget(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        self.initUI()

    def initUI(self):
        #self.btn.setIcon(QIcon('smile-1.png'))
        self.btn.clicked.connect(self.print)
        dif = self.menuBar.addMenu('Сложность')
        dif.addAction('Новичок')
        dif.addAction('Любитель')
        dif.triggered[QAction].connect(self.print)

        self.init_field()

    def push(self,item):
        pass

    def init_field(self):
        self.grd.setSpacing(0)
        positions = [(i,j) for i in range(10) for j in range(10)]
        self.btn_grp = QButtonGroup()
        i = 0
        for position in positions:
            button = PushButtonRight(str(), self.push, self.push)
            i += 1
            self.btn_grp.addButton(button)
            button.setMinimumSize(QSize(30, 30))



            button.setStyleSheet('border-image: url(media/t-3.png);')
            #button.setStyleSheet('border-image: url(media/t-3.png);border-top: 3px transparent;border-bottom: 3px transparent;border-right: 10px transparent;border-left: 10px transparent;')
            self.grd.addWidget(button, *position)

    def print(self, item):
        print(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
