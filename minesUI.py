from PyQt5.QtWidgets import QPushButton, QGridLayout
from PyQt5.QtWidgets import QSpacerItem, QVBoxLayout, QHBoxLayout, QLCDNumber
from PyQt5.QtWidgets import QSizePolicy, QAction, QButtonGroup
from PyQt5.QtCore import QSize

from PushButtonRight import PushButtonRight


class minesUI:
    """
        Класс отрисовки всего интерфейса.
    """
    num_cells = [
        'media/t0.png',
        'media/t1.png',
        'media/t2.png',
        'media/t3.png',
        'media/t4.png',
        'media/t5.png',
        'media/t6.png',
        'media/t7.png',
        'media/t8.png'
    ]
    faces = [
        'media/face0.png',
        'media/face1.png',
        'media/face2.png',
        'media/face3.png'
    ]
    mines_ic = [
        'media/t-1.png',
        'media/t-2.png',
        'media/t-5.png',
    ]
    flags = [
        'media/t-3.png',
        'media/t-4.png',
        'media/t-6.png'
    ]


    def __init__(self, window):
        self.window = window
        self.level = window.level
        self.levels = {
            'Beginer': {'x': 9, 'y': 9, 'mines': 10, 'size': 30},
            'Intermediate': {'x': 16, 'y': 16, 'mines': 40, 'size': 30},
            'Expert': {'x': 30, 'y': 16, 'mines': 99, 'size': 30},
            'Superhuman': {'x': 47, 'y': 47, 'mines': 500, 'size': 19}
        }


    def initUI(self, func):
        self.create_background()
        self.create_field()
        self.create_toolbar(func)


    def create_background(self):
        """
            Метод, который создаёт весь интерфейс кроме, поля для игры.
        """
        self.x, self.y, self.mines, self.size = self.levels[self.level].values()
        self.window.vertL = QVBoxLayout()
        self.window.horL = QHBoxLayout()
        self.window.lcd_mines = QLCDNumber()
        self.window.lcd_times = QLCDNumber()
        self.window.lcd_mines.display(self.mines)
        self.window.horL.addWidget(self.window.lcd_mines)
        self.window.btn = QPushButton()
        self.window.btn.clicked.connect(self.window.restart)
        self.window.btn.setMinimumSize(QSize(30,30))
        self.window.btn.geometry().setSize(QSize(30,30))
        self.window.btn.setStyleSheet('border-image: url(media/face0.png);')
        self.window.horL.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding))
        self.window.horL.addWidget(self.window.btn)
        self.window.horL.addSpacerItem(QSpacerItem(1,1,QSizePolicy.Expanding))
        self.window.horL.addWidget(self.window.lcd_times)
        self.window.vertL.addLayout(self.window.horL)
        self.window.grid = QGridLayout()
        self.window.grid.setSpacing(0)
        self.window.vertL.addLayout(self.window.grid)
        self.window.vertL.setStretch(1,90)
        self.window.centralwidget.setLayout(self.window.vertL)
        self.window.setGeometry(20,50,0,0)
        self.window.setFixedSize(0,0)


    def create_field(self):
        """
            Метод, создающий основное поле для игры.
        """
        positions = [(i,j) for i in range(self.y) for j in range(self.x)]
        self.window.btn_grp = QButtonGroup()
        i = 0
        for position in positions:
            button = PushButtonRight(str(), self.window.minesEng.push, self.window.minesEng.flag)
            i += 1
            self.window.btn_grp.addButton(button)
            button.setMinimumSize(QSize(self.size, self.size))
            button.geometry().setSize(QSize(self.size,self.size))
            button.setStyleSheet('border-image: url(media/t-3.png);')
            self.window.grid.addWidget(button, *position)


    def restart(self):
        """
            Метод, для перезапуска игры.
            Удаляет все кнопки с поля, и добавляет их заново.
        """
        # НЕ ОПТИМИЗИРОВАННО!!! так как, если клеток много, то программа подвисает на некоторое время
        self.window.btn.setStyleSheet(f'border-image: url(media/face0.png);')
        self.window.hide()
        positions = [(i,j) for i in range(self.y) for j in range(self.x)]
        for position in positions:
            self.window.grid.itemAtPosition(*position).widget().deleteLater()
        self.x, self.y, self.mines, self.size = self.levels[self.window.level].values()
        self.window.lcd_mines.display(self.mines)
        self.window.setFixedSize(0,0)
        self.create_field()
        self.window.show()


    def create_toolbar(self, func):
        """
            Метод, создающий меню выбора сложности и кнопку для показа рекордов.
        """
        dif = self.window.menuBar.addMenu('Сложность')
        dif.addAction('Новичок')
        dif.addAction('Любитель')
        dif.addAction('Эксперт')
        dif.addAction('Суперчеловек')
        dif.triggered[QAction].connect(func)
        dif = self.window.menuBar.addAction('Таблица рекордов')
        dif.triggered.connect(self.window.show_score)
