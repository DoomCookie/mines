from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon
from PyQt5.QtCore import Qt, QPoint, QSize, QTime, QTimer

from minesUI import minesUI
from minesEng import minesEng
from minesScore import MinesScore

from PyQt5 import uic
import sys

levels = {
    'Новичок': 'Beginer',
    'Любитель': 'Intermediate',
    'Эксперт': 'Expert',
    'Суперчеловек': 'Superhuman'
}

class MinesGame(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mines.ui', self)
        self.level = 'Beginer'
        self.minesUI = minesUI(self)
        self.minesEng = minesEng(self)
        self.initUI()

        self.tmr = QTimer()
        self.tmr.setInterval(1000)
        self.tmr.timeout.connect(self.updateTime)
        self.tmr.start()
        self.timer = 0

        #self.minesEng.get_win()



    def start_time(self):
        self.lcd_times.display(0)
        self.timer = 0
        self.tmr.start()

    def show_score(self, item):
        self.score = MinesScore()
        self.score.show()

    def updateTime(self):
        self.timer += 1
        self.lcd_times.display(self.timer)

    def initUI(self):
        self.minesUI.initUI(self.change_dif)
        self.minesEng.init_field()



    def change_dif(self, item):
        self.level = levels[item.text()]
        self.restart()

    def restart(self):
        self.minesUI.restart()
        self.minesEng.init_field()
        self.start_time()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinesGame()
    ex.show()
    sys.exit(app.exec_())
