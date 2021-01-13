from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon
from PyQt5.QtCore import Qt, QPoint, QSize

from minesUI import minesUI
from minesEng import minesEng

from PyQt5 import uic
import sys

levels = {
    'Новичок': 'Beginer',
    'Любитель': 'Intermediate',
    'Эксперт': 'Expert',
    'Суперчеловек': 'Superhuman'
}

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mines.ui', self)
        self.level = 'Beginer'
        self.minesUI = minesUI(self)
        self.minesEng = minesEng(self)
        self.initUI()

    def initUI(self):
        self.minesUI.initUI(self.change_dif)
        self.minesEng.init_field()
        


    def change_dif(self, item):
        self.level = levels[item.text()]
        self.restart()

    def restart(self):
        self.minesUI.restart()
        self.minesEng.init_field()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
