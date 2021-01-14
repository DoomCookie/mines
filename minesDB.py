import sqlite3
from os import path, getlogin
from PyQt5.QtCore import QDateTime, QTime


class minesDB:

    db = 'minesDB.sqlite'

    def __init__(self):
        if not path.isfile(self.db):
            self.con = sqlite3.connect(self.db)
            self.cur = self.con.cursor()
            self.cur.execute("""CREATE TABLE player_score(
                            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            player_name TEXT NOT NULL,
                            player_difficult TEXT NOT NULL,
                            player_time INTEGER NOT NULL,
                            player_date DATE NOT NULL)""")
        else:
            self.con = sqlite3.connect(self.db)
            self.cur = self.con.cursor()

    def add_result(self, dif, time):
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
        res = self.cur.execute(f"""
                                    select player_name, player_difficult, player_time, player_date
                                    from player_score where
                                    player_difficult = '{dif}'
                                    """).fetchall()
        return res

    def __del__(self):
        self.con.close()


if __name__ == "__main__":
    db = minesDB()
