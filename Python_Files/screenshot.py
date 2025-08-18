# screenshot.py (using mss instead of PIL.ImageGrab)
import sys
import os
import uuid
from PyQt5 import QtWidgets, QtGui, QtCore
import mss
import mss.tools

TEMP_FOLDER = os.path.join(os.getcwd(), ".peek_cache")
os.makedirs(TEMP_FOLDER, exist_ok=True)

class SnippingWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
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
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 100))
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

        # Capture region with mss
        with mss.mss() as sct:
            monitor = {
                "top": y1,
                "left": x1,
                "width": x2 - x1,
                "height": y2 - y1
            }
            img = sct.grab(monitor)
            filename = os.path.join(TEMP_FOLDER, f"{uuid.uuid4()}.png")
            mss.tools.to_png(img.rgb, img.size, output=filename)

        print("Saved to:", filename)
        self.close()

def snip():
    app = QtWidgets.QApplication(sys.argv)
    window = SnippingWidget()
    window.show()
    app.exec_()

if __name__ == "__main__":
    snip()
