from sqlite3 import connect
from os import path, getlogin
from PyQt5.QtCore import QDateTime, QTime


class minesDB:
    """
        Класс для работы с базой данных.
    """
    def __init__(self):
        self.db = 'db/minesDB.sqlite' # файл с баззой данных
        # если файл существует то мы его открываем, если нет, то создаём.
        if not path.isfile(self.db):
            self.con = connect(self.db)
            self.cur = self.con.cursor()
            self.cur.execute("""CREATE TABLE player_score(
                            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            player_name TEXT NOT NULL,
                            player_difficult TEXT NOT NULL,
                            player_time INTEGER NOT NULL,
                            player_date DATE NOT NULL)""")
        else:
            self.con = connect(self.db)
            self.cur = self.con.cursor()


    def add_result(self, dif, time):
        """
            Метод добавления результата игры в базу данных.
            Принимает время и сложность.
        """
        date = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        s = time % 60
        m = (time // 60) % 60
        h = time // 3600
        tm = QTime(h, m, s).toString("hh:mm:ss")
        self.cur.execute(f"""
                            INSERT INTO player_score(
                                player_name,
                                player_difficult,
                                player_time,
                                player_date
                            ) VALUES(
                                '{getlogin()}',
                                '{dif}',
                                '{tm}',
                                '{date}'
                            )
                            """)
        self.con.commit()


    def get_score(self, dif):
        """
            Метод, который достаёт из бд все данные по заданной сложности.
            Принимает сложность.
            Возвращает список записей в базе данных.
        """
        res = self.cur.execute(f"""
                                    select player_name, player_difficult, player_time, player_date
                                    from player_score where
                                    player_difficult = '{dif}'
                                    """).fetchall()
        return res


    def __del__(self):
        """
            Деструктор, который закрывает базу данных, при закрытии приложения.
        """
        self.con.close()
