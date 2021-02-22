from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

from minesUI import minesUI
from minesEng import minesEng
from minesScore import MinesScore

from PyQt5 import uic
import sys

# словарь уровней
levels = {
    'Новичок': 'Beginer',
    'Любитель': 'Intermediate',
    'Эксперт': 'Expert',
    'Суперчеловек': 'Superhuman'
}


class MinesGame(QMainWindow):
    """
        Класс основной игры
        Содержит в себе объект для отрисовки интерфейса и объект "движка" игры
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('mines.ui', self)
        self.level = 'Beginer'
        self.minesUI = minesUI(self)
        self.minesEng = minesEng(self)
        self.initUI()

        # Запуск таймера при запуске игры.
        self.tmr = QTimer()
        self.tmr.setInterval(1000)
        self.tmr.timeout.connect(self.updateTime)
        self.tmr.start()
        self.timer = 0

        #self.minesEng.get_win() метод для тестирования(мгновенная победа при запуске)


    def start_time(self):
        """
            Метод, запускающий таймер для подсчёта времени в игре.
        """
        self.lcd_times.display(0)
        self.timer = 0
        self.tmr.start()


    def show_score(self, item):
        """
            Метод, открывающий окно с рейтингом игр.
        """
        self.score = MinesScore()
        self.score.show()


    def updateTime(self):
        """
            Метод, увеличивающий количество секунд и отображающий его на экране.
        """
        self.timer += 1
        self.lcd_times.display(self.timer)


    def initUI(self):
        """
            Метод, запускающий создание интерфейса и запуск движка игры.
        """
        self.minesUI.initUI(self.change_dif)
        self.minesEng.init_field()


    def change_dif(self, item):
        """
            Метод смены сложности.
        """
        self.level = levels[item.text()]
        self.restart()


    def restart(self):
        """
            Метод для перезапуска игры.
        """
        self.minesUI.restart()
        self.minesEng.init_field()
        self.start_time()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MinesGame()
    ex.show()
    sys.exit(app.exec_())
