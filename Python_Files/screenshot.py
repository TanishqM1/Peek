# screenshot.py
import os, uuid, mss, mss.tools
from PyQt5 import QtWidgets, QtGui, QtCore

def get_temp_folder():
    appdata = os.getenv("APPDATA") or os.path.expanduser("~/.config")
    folder = os.path.join(appdata, "Peek", "cache")
    os.makedirs(folder, exist_ok=True)
    return folder

TEMP_FOLDER = get_temp_folder()

class SnippingWidget(QtWidgets.QWidget):
    def __init__(self, on_finished=None):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.on_finished = on_finished

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
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
        x1, y1 = min(self.begin.x(), self.end.x()), min(self.begin.y(), self.end.y())
        x2, y2 = max(self.begin.x(), self.end.x()), max(self.begin.y(), self.end.y())
        self.hide()
        QtWidgets.QApplication.processEvents()

        if x2 > x1 and y2 > y1:
            with mss.mss() as sct:
                monitor = {"top": y1, "left": x1, "width": x2 - x1, "height": y2 - y1}
                img = sct.grab(monitor)
                filename = os.path.join(TEMP_FOLDER, f"{uuid.uuid4()}.png")
                mss.tools.to_png(img.rgb, img.size, output=filename)
                if self.on_finished:
                    self.on_finished(filename)

        self.close()

def start_snip(on_finished=None):
    """Launch snipping overlay inside the running Qt app."""
    widget = SnippingWidget(on_finished=on_finished)
    widget.show()
    widget.raise_()
    widget.activateWindow()
    return widget
