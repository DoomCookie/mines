from random import randint

WIDTH = 3
HEIGHT = 3
STATUS = {
    'nothing': 0,
    'mine': 1
}
MARKS = {
    'close': '[ ]',
    'open': '   ',
    'flag': ' F ',
    'question': ' ? '
}
NUMBER_OF_MINES = 3


def lose_draw(field, field_for_player):
    """
    Отрисовка игрового поля в случае поражения, с отображением всех мин
    Принимает в качестве аргументов 2 поля: С расположением мин и поле для игрока
    """
    for n in range(HEIGHT):
        for m in range(WIDTH):
            if field[n][m] == STATUS['mine']:
                print(" * ", end=' ')
            else:
                print(field_for_player[n][m], end=' ')
        print()
    print()


def win(field, field_for_player):
    """
    Проверка на победу. Если на карте не осталось закрытых клеток и количество
    флажков на минах равно количеству мин, то это победа.
    Принимает в качестве аргументов 2 поля: С расположением мин и поле для игрока
    Возвращает True или False
    """
    count = 0
    for n in range(HEIGHT):
        for m in range(WIDTH):
            if (field_for_player[n][m] == MARKS['close'] or
                    field_for_player[n][m] == MARKS['question']):
                return False
            if (field_for_player[n][m] == MARKS['flag'] and
                    field[n][m] == STATUS['mine']):
                count += 1
    if count == NUMBER_OF_MINES:
        return True


def get_neigh(field, n, m):
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
            elif ((0 <= i < HEIGHT) and (0 <= j < WIDTH)):
                neigh.append((i, j))
    return neigh


def watch_neigh(field, field_for_player, n, m, buffer=set()):
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
    if (n, m) not in buffer and field[n][m] != STATUS['mine']:
        buffer.add((n, m))
        neigh = get_neigh(field, n, m)
        for n_neigh, m_neigh in neigh:
            if field[n_neigh][m_neigh] == STATUS['mine']:
                count_mines += 1
        if count_mines == 0:
            field_for_player[n][m] = MARKS['open']
            for n_neigh, m_neigh in neigh:
                watch_neigh(field, field_for_player, n_neigh, m_neigh, buffer)
        else:
            field_for_player[n][m] = f" {count_mines} "


def update(field, field_for_player, n, m, mark):
    """
    Функция обновления поля, в которой происходит отлов маркеров а также вызов функции
    для просмотра соседей.
    Если маркер не задан, смотрим на маркер на клетке, если он там стоит сообщаем об этом
    игроку, иначе вызываем функцию обхода соседей.
    Иначе если маркер С - то есть удаление других маркеров и на клетке стоит маркер,
    удаляем этот маркер.
    Во всех остальных случаях, когда клетка закрыта ставим на неё указанный маркер.
    Если клетка открыта ничего не произойдет.
    Принимает в качестве аргументов 2 поля: С расположением мин и поле для игрока,
    строку и столбец клетки, маркер.
    """
    if mark == '':
        if field_for_player[n][m] == MARKS['flag'] or field_for_player[n][m] == MARKS['question']:
            print('На ячейке стоит маркер!\n')
        else:
            watch_neigh(field, field_for_player, n, m)
    elif (mark == 'C' and
          (field_for_player[n][m] == MARKS['flag'] or field_for_player[n][m] == MARKS['question'])):
        print("la")
        field_for_player[n][m] = MARKS['close']
    elif field_for_player[n][m] == MARKS['close']:
        field_for_player[n][m] = f" {mark} "


def step():
    """
    Функция считывает ход игрока и полностью его обрабатывает, чтобы ввод был корректный.
    ничего не принимает.
    Возвращает номер строки, номер столбца и маркер.
    """
    while True:
        player_step = input("""
Введите ваш ход в формате \"n m [F или ? или C]\", где n - номер строки, m - номер \
столбца, а f - флаг, где предположительно мина; ? - ячейка вызывающая \
сомнение; C - Очистить ячейку от метки. Это опциональеый параметр для установки \
метки на ячеку (квадратные скобки ставить не нужно). Если указать ячейку без \
параметра, то она откроется.\n
""").split()
        if len(player_step) == 2:
            n = player_step[0]
            m = player_step[1]
            mark = ''
        elif len(player_step) == 3:
            n = player_step[0]
            m = player_step[1]
            mark = player_step[2]
        else:
            print(
                "Неккоректный ввод: аргументов слишком много или слишком мало." +
                " Пожалуйста повторите ваш ход в коррректной форме"
            )
            continue
        if n.isdigit() and m.isdigit():
            n = int(n) - 1
            m = int(m) - 1
        else:
            print(
                "Неккоректный ввод: Номера строки и/или столбца" +
                " не являются цифрами. Пожалуйста повторите ваш ход в коррректной форме"
            )
            continue
        if not (mark == '?' or mark == 'F' or mark == '' or mark == 'C'):
            print(
                "Неккоректный ввод: Недопустимая метка." +
                " Пожалуйста повторите ваш ход в коррректной форме"
            )
            continue
        if 0 <= n < HEIGHT and 0 <= m < WIDTH:
            return (n, m, mark)
        else:
            print(
                "Неккоректный ввод: Номер столбца или строки не входит в " +
                "допустимый диапазон. Пожалуйста повторите ваш ход в коррректной форме"
            )
            continue


def init(n_player, m_player):
    """
    Функция создания полей, и заполнения минами основываясь на вводе пользователя.
    Принимает номера строки и столбца.
    """
    field_for_player = [[MARKS['close'] for x in range(WIDTH)] for y in range(HEIGHT)]
    field = [[STATUS['nothing'] for x in range(WIDTH)] for y in range(HEIGHT)]
    mines = NUMBER_OF_MINES
    while mines != 0:
        n = randint(0, HEIGHT - 1)
        m = randint(0, WIDTH - 1)
        if field[n][m] != STATUS['mine'] and n != n_player and m != m_player:
            field[n][m] = STATUS['mine']
            mines -= 1
    return field, field_for_player


def draw(field):
    """
    Отрисовка игрового поля.
    Принимает поле.
    """
    for line in field:
        for cell in line:
            print(cell, end=' ')
        print()


def main():
    """
    Главная функция в которой происходит основной процесс игры.
    В цикле происходит проверка условий поражения или победы, если одно из
    них истина, то сообщаем результат и выходим из цикла.
    """
    n, m, mark = step()
    field, field_for_player = init(n, m)
    while True:
        if field[n][m] == STATUS['mine'] and mark == '':
            print('Вы проиграли!\n')
            lose_draw(field, field_for_player)
            break
        update(field, field_for_player, n, m, mark)
        if win(field, field_for_player):
            print('Вы победили\n')
            draw(field_for_player)
            break
        draw(field_for_player)
        n, m, mark = step()


if __name__ == '__main__':
    command = input("Введите команду:\n0 - Выход.\n1 - Начать игру.\n")
    while not (command == '0' or command == '1'):
        print('Комманда была введена неверно, повторите попытку.\n')
        command = input("Введите команду:\n0 - Выход.\n1 - Начать игру.\n")
    while command != '0':
        main()
        command = input("Введите команду:\n0 - Выход.\n1 - Начать игру.\n")
