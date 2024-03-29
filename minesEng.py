from random import randint
from minesDB import minesDB

class minesEng:
    """
        Класс, который просчитывает всю логику игры.
    """
    def __init__(self, window):
        self.window = window
        self.status = {
            'nothing': 0,
            'mine': 1
        }
        self.minesDB = minesDB()


    def init_field(self):
        """
            Метод, который создаёт поле для игры в зависимости от сложности.
            Заполняет поле рандомно минами и сохраняет его в памяти.
        """
        self.lose_game = False
        self.win_game = False
        self.flags = set()
        self.height = self.window.minesUI.y
        self.width = self.window.minesUI.x
        self.count_mines = self.window.minesUI.mines
        self.field = [[self.status['nothing'] for x in range(self.width)] for y in range(self.height)]
        mines = self.count_mines
        self.mines = set()
        while mines != 0:
            n = randint(0, self.height - 1)
            m = randint(0, self.width - 1)
            if self.field[n][m] != self.status['mine']:
                self.field[n][m] = self.status['mine']
                self.mines.add(n * self.width + m)
                mines -= 1

#-------------------------------------------------------------------------------
    # часть кода для дебага
    #
    # отрисовка поля с минами в консоли
    #     print()
    #     self.draw(self.field)
    #
    # def get_win(self): # функция мгновенной победы
    #     for btn in self.window.btn_grp.buttons():
    #         if not btn.isFlat() and self.window.grid.indexOf(btn) not in self.mines:
    #             self.push(btn)
    #         if self.window.grid.indexOf(btn) in self.mines:
    #             self.flag(btn)
    #
    # def draw(self,field): # функция отрисовки поля в консоли с минами
    #     """
    #     Отрисовка игрового поля.
    #     Принимает поле.
    #     """
    #     for line in field:
    #         for cell in line:
    #             print(cell, end=' ')
    #         print()
#-------------------------------------------------------------------------------


    def push(self, item):
        """
            Метод, который вызывается при нажатии левой кнопкой мыши на ячейку поля.
            Проверяет, что игра ещё идет, что на этой клетке нет мины или флага
            после чего расчитывает сколько мин вокруг него.
            Проверяет проиграли или выиграли после совершения хода.
        """
        if not(self.lose_game or self.win_game):
            ind = self.window.grid.indexOf(item)
            y, x = (self.window.grid.getItemPosition(ind))[:2]
            neighs = self.get_neigh(x,y)
            if self.field[y][x] == self.status['mine'] and item.statusTip() != "F":
                self.lose(item)
            if not item.isFlat() and item.statusTip() != "F":
                item.setFlat(True)
                item.setStyleSheet(f'border-image: url({self.window.minesUI.num_cells[0]});')
                self.watch_neigh(x, y, buffer=set())
            self.win()


    def flag(self, item):
        """
            Метод, который вызывается при нажатии правой кнопкой мыши на ячейку поля.
            Проверяет, что игра ещё идет, что эта клетка ещё не открыта
            если флаг стоит, удаляет его, если нет ставит.
            Изменяет количество доступных флагов и делает проверку на победу.
        """
        if not(self.lose_game or self.win_game) and not item.isFlat():
            ind = self.window.grid.indexOf(item)
            y, x = (self.window.grid.getItemPosition(ind))[:2]
            if item.statusTip() != "F" and self.window.minesUI.mines > 0:
                self.flags.add(ind)
                item.setStatusTip('F')
                item.setStyleSheet(f'border-image: url({self.window.minesUI.flags[1]});')
                self.window.minesUI.mines -= 1
            else:
                self.flags.remove(ind)
                item.setStatusTip('')
                item.setStyleSheet(f'border-image: url({self.window.minesUI.flags[0]});')
                self.window.minesUI.mines += 1
            self.window.lcd_mines.display(self.window.minesUI.mines)
            self.win()


    def win(self):
        """
            Метод, который проверяет выиграл ли игрок или нет.
            Смотрит все ли ячеки с минами помечены флагом и открыты ли все остальные.
            Если это так, то останавливате таймер и добавляет результат в базу данных.
        """
        if self.mines == self.flags:
            for btn in self.window.btn_grp.buttons():
                if not btn.isFlat() and btn.statusTip() != 'F':
                    return False
            self.win_game = True
            self.window.btn.setStyleSheet(f'border-image: url({self.window.minesUI.faces[3]});')
            self.window.tmr.stop()
            self.minesDB.add_result(
                self.window.level,
                self.window.timer
            )
            return True


    def lose(self, item):
        """
            Метод, который вызывается в случае поражения.
            Помечает все мины на поле, показывая верно ли были установлены флаги.
        """
        self.lose_game = True
        for mine in self.mines:
            btn = self.window.grid.itemAt(mine).widget()
            btn.setFlat(True)
            if btn == item:
                btn.setStyleSheet(f'border-image: url({self.window.minesUI.mines_ic[1]});')
            elif btn.statusTip() != "F":
                btn.setStyleSheet(f'border-image: url({self.window.minesUI.mines_ic[0]});')
        for flag in self.flags:
            if flag not in self.mines:
                    btn = self.window.grid.itemAt(flag).widget()
                    btn.setStyleSheet(f'border-image: url({self.window.minesUI.mines_ic[2]});')
        self.window.tmr.stop()
        self.window.btn.setStyleSheet(f'border-image: url(media/face2.png);')


    def get_neigh(self, m, n):
        """
        Функция нахождения соседей клетки.
        Принимает поле с минам, номер строки, номер столбца.
        Возвращает список всех кортежей координат соседних клеток.
        """
        neigh = []
        for i in range(n - 1, n + 2):
            for j in range(m - 1, m + 2):
                if i == n and j == m:
                    continue
                elif ((0 <= i < self.height) and (0 <= j < self.width)):
                    neigh.append((i, j))
        return neigh


    def watch_neigh(self, m, n, buffer=set()):
        """
        Рекурсивная функция проверки соседних клеток.
        Если клетки нет в буфере проверенных клеток и на ней нет мины,
        то мы получаем список её соседей, её помещаем в буфер, после чего
        проходим по всем соседям и считаем количество мин вокруг.
        Если мин ноль, открывает эту и клетку, а для всех соседих запускаем рекурсивно
        эту же функцию. Иначе устанавливаем в эту клетку количество мин по соседству.
        Принимает в качестве аргументов 2 поля: С расположением мин, поле для игрока
        номера строки и столбца, Опциональный аргумент буфер, который если его не указать
        по умолчанию будет пустое множество.
        """
        count_mines = 0
        if (n, m) not in buffer and self.field[n][m] != self.status['mine']:
            buffer.add((n, m))
            neigh = self.get_neigh(m, n)
            for n_neigh, m_neigh in neigh:
                if self.field[n_neigh][m_neigh] == self.status['mine']:
                    count_mines += 1
            ind = n * self.width + m
            btn = self.window.grid.itemAt(ind).widget()
            if count_mines == 0:
                if btn.statusTip() != 'F':
                    btn.setFlat(True)
                    btn.setStyleSheet(f'border-image: url({self.window.minesUI.num_cells[0]});')
                for n_neigh, m_neigh in neigh:
                    self.watch_neigh(m_neigh, n_neigh, buffer)
            else:
                if btn.statusTip() != "F":
                    btn.setFlat(True)
                    btn.setStyleSheet(f'border-image: url({self.window.minesUI.num_cells[count_mines]});')
