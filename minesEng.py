from random import randint

class minesEng:

    def __init__(self, window):
        self.window = window
        self.status = {
            'nothing': 0,
            'mine': 1
        }


    def init_field(self):
        self.height = self.window.minesUI.y
        self.width = self.window.minesUI.x
        self.count_mines = self.window.minesUI.mines
        self.field = [[self.status['nothing'] for x in range(self.width)] for y in range(self.height)]
        mines = self.count_mines
        self.mines = []
        while mines != 0:
            n = randint(0, self.height - 1)
            m = randint(0, self.width - 1)
            if self.field[n][m] != self.status['mine']:
                self.field[n][m] = self.status['mine']
                self.mines.append(n * self.width + m)
                mines -= 1

#-------------------------------------------------------------------------------
        self.draw(self.field)

    def draw(self,field):
        """
        Отрисовка игрового поля.
        Принимает поле.
        """
        for line in field:
            for cell in line:
                print(cell, end=' ')
            print()
#-------------------------------------------------------------------------------

    def push(self, item):
        ind = self.window.grid.indexOf(item)
        y, x = (self.window.grid.getItemPosition(ind))[:2]
        neighs = self.get_neigh(x,y)
        if self.field[y][x] == self.status['mine']:
            print('Вы проиграли')
        self.update(x, y)
        # item.setFlat(True)
        # for neigh in neighs:
        #     self.window.grid.itemAt(neigh).widget().setFlat(True)

    def update(self, x, y):
        ind = y * self.width + x
        btn = self.window.grid.itemAt(ind).widget()

        if not btn.isFlat() and not btn.text() == 'F':
            btn.setFlat(True)
            self.watch_neigh(x, y, buffer=set())


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
                    #neigh.append(i * self.width + j)
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
                btn.setFlat(True)
                for n_neigh, m_neigh in neigh:
                    self.watch_neigh(m_neigh, n_neigh, buffer)
            else:
                btn.setFlat(True)
                btn.setText(f"{count_mines}")
