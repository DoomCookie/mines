from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QPoint, QSize

from PyQt5 import uic
import sys

levels = {
    'Beginer': {'x': 9, 'y': 9, 'mines': 10, 'size': 30},
    'Intermediate': {'x': 16, 'y': 16, 'mines': 40, 'size': 30},
    'Expert': {'y': 16, 'x': 30, 'mines': 99, 'size': 30},
    'Superhuman': {'y': 50, 'x': 50, 'mines': 500, 'size': 19}
}

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mines.ui', self)
        self.initUI()

    def initUI(self):
        self.vertL = QVBoxLayout()

        self.horL = QHBoxLayout()
        self.lcd_mines = QLCDNumber()
        self.lcd_flags = QLCDNumber()
        self.horL.addWidget(self.lcd_mines)
        self.btn = QPushButton()
        self.btn.setMinimumSize(QSize(30,30))
        self.btn.geometry().setSize(QSize(30,30))
        self.horL.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding))
        #print(dir(self.horL))
        self.horL.addWidget(self.btn)
        self.horL.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding))
        self.horL.addWidget(self.lcd_flags)
        self.vertL.addLayout(self.horL)
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.vertL.addLayout(self.grid)
        self.vertL.setStretch(1,90)
        positions = [(i,j) for i in range(16) for j in range(30)]
        for position in positions:
            button = QPushButton('')
            button.setMinimumSize(QSize(30,30))
            self.grid.addWidget(button, *position)
        self.centralwidget.setLayout(self.vertL)


        # print((self.vert.setStretch(1,99)))
        #self.setGeometry(300, 300, 150, 150)
        # print((self.grid.geometry().setSize(QSize(1000,1000))))
        # print((self.btn2.size()))

    def push(self):
        print()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
