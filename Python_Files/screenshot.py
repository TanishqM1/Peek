import sys
import os
import uuid
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import ImageGrab

# Create cache folder
TEMP_FOLDER = os.path.join(os.getcwd(), ".peek_cache")
os.makedirs(TEMP_FOLDER, exist_ok=True)

class SnippingWidget(QtWidgets.QWidget):
    def __init__(self, callback=None):
        super().__init__()
        self.callback = callback
        self.setWindowTitle("Snip")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 100))  # Dim
        pen = QtGui.QPen(QtGui.QColor("gray"), 2)
        painter.setPen(pen)
        painter.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        self.hide()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        filename = os.path.join(TEMP_FOLDER, f"{uuid.uuid4()}.png")
        img.save(filename)
        print("Saved to:", filename)
        self.close()

        # 🔁 Trigger callback with file path
        if self.callback:
            self.callback(filename)

def start_snip(callback):
    app = QtWidgets.QApplication(sys.argv)
    window = SnippingWidget(callback)
    window.show()
    app.exec_()
