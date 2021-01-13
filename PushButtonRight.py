from PyQt5 import QtWidgets, Qt, QtCore


class PushButtonRight(QtWidgets.QPushButton):
    left_click = QtCore.pyqtSignal()
    right_click = QtCore.pyqtSignal()

    def __init__(self, string, leftFunc, rightFunc):
        super().__init__(string)
        self.leftFunc = leftFunc
        self.rightFunc = rightFunc

    def mousePressEvent(self, event):
        if event.button() == Qt.Qt.LeftButton:
            self.left_click.emit()
            self.leftFunc(self)
        elif event.button() == Qt.Qt.RightButton:
            self.right_click.emit()
            self.rightFunc(self)

        QtWidgets.QPushButton.mousePressEvent(self, event)
