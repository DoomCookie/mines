from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon
from PyQt5.QtCore import Qt, QPoint, QSize


class minesUI:

    def __init__(self, window, level):
        self.window = window
        self.level = level
        self.levels = {
            'Beginer': {'x': 9, 'y': 9, 'mines': 10, 'size': 30},
            'Intermediate': {'x': 16, 'y': 16, 'mines': 40, 'size': 30},
            'Expert': {'x': 30, 'y': 16, 'mines': 99, 'size': 30},
            'Superhuman': {'x': 50, 'y': 50, 'mines': 500, 'size': 19}
        }
    def create(self):
        x, y, mines, size = self.levels['Beginer'].values()
        self.window.vertL = QVBoxLayout()
        self.window.horL = QHBoxLayout()
        self.window.lcd_mines = QLCDNumber()
        self.window.lcd_flags = QLCDNumber()
        self.window.lcd_mines.display(mines)
        self.window.horL.addWidget(self.window.lcd_mines)
        self.window.btn = QPushButton()
        self.window.btn.setMinimumSize(QSize(30,30))
        self.window.btn.geometry().setSize(QSize(30,30))
        self.window.btn.setIcon(QIcon('smile-1.png'))
        self.window.horL.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding))
        self.window.horL.addWidget(self.window.btn)
        self.window.horL.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding))
        self.window.horL.addWidget(self.window.lcd_flags)
        self.window.vertL.addLayout(self.window.horL)
        self.window.grid = QGridLayout()
        self.window.grid.setSpacing(0)
        self.window.vertL.addLayout(self.window.grid)
        self.window.vertL.setStretch(1,90)
        positions = [(i,j) for i in range(y) for j in range(x)]
        for position in positions:
            button = QPushButton('')
            button.setMinimumSize(QSize(size,size))
            self.window.grid.addWidget(button, *position)
        self.window.centralwidget.setLayout(self.window.vertL)
