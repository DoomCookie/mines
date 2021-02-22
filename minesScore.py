from PyQt5.QtWidgets import QMainWindow, QButtonGroup, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import uic

from minesDB import minesDB


class MinesScore(QMainWindow):
    """
        Класс для отрисовки окна с рекордами.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('score.ui', self)
        self.btn_grp = QButtonGroup()
        self.btn_grp.addButton(self.btn_beg)
        self.btn_grp.addButton(self.btn_inter)
        self.btn_grp.addButton(self.btn_exp)
        self.btn_grp.addButton(self.btn_sh)
        self.btn_grp.buttonClicked.connect(self.show_score)
        self.minesDB = minesDB()


    def show_score(self, item):
        """
            Метод, отображающий список рекордов по выбранной сложности.
            Прикреплен к кнопкам, отвечающие за сложности на этом окне.
        """
        for btn in self.btn_grp.buttons():
            btn.setFlat(False)
        item.setFlat(True)
        data = self.minesDB.get_score(item.statusTip())
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
                self.tableWidget.item(i, j).setFlags(Qt.ItemIsEnabled)
