import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class ToggleSwitch(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setChecked(False)
        self.setFixedSize(30, 16)
        self.setStyleSheet("""
            QCheckBox::indicator {
                width: 30px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border-radius: 8px;
                background-color: #555;
            }
            QCheckBox::indicator:checked {
                border-radius: 8px;
                background-color: #00c853;
            }
        """)


class PeekAssistant(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PeekAssistant")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.dragging = False
        self.offset = None
        self.pressed_keys = set()
        self.required_keys = {Qt.Key_Control, Qt.Key_Alt, Qt.Key_Q}

        self.init_ui()

    def init_ui(self):
        outer_layout = QHBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        frame.setObjectName("BackgroundFrame")
        frame.setStyleSheet("""
            QFrame#BackgroundFrame {
                background-color: rgba(49, 49, 49, 240);
                border-radius: 10px;
            }
            QLabel {
                color: white;
            }
        """)

        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(12, 6, 12, 6)
        frame_layout.setSpacing(8)

        # Bold, smooth title
        title = QLabel("PeekAI")
        title.setStyleSheet("font-weight: bold; font-size: 13px; color: white;")
        title.setAlignment(Qt.AlignVCenter)
        frame_layout.addWidget(title, alignment=Qt.AlignVCenter)

        # Screenshot switch (label + switch)
        self.ss_switch = ToggleSwitch()
        ss_layout = QHBoxLayout()
        ss_layout.setSpacing(3)
        ss_label = QLabel("Screenshot")
        ss_label.setFixedWidth(70)
        ss_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        ss_label.setStyleSheet("font-weight: bold; font-size: 11px; color: white;")
        ss_layout.addWidget(ss_label)
        ss_layout.addWidget(self.ss_switch)
        frame_layout.addLayout(ss_layout)

        # Prompt switch (label + switch)
        self.prompt_switch = ToggleSwitch()
        prompt_layout = QHBoxLayout()
        prompt_layout.setSpacing(3)
        prompt_label = QLabel("Prompt")
        prompt_label.setFixedWidth(70)
        prompt_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        prompt_label.setStyleSheet("font-weight: bold; font-size: 11px; color: white;")
        prompt_layout.addWidget(prompt_label)
        prompt_layout.addWidget(self.prompt_switch)
        frame_layout.addLayout(prompt_layout)

        frame.setLayout(frame_layout)
        outer_layout.addWidget(frame)
        self.setLayout(outer_layout)

        self.setFixedSize(300, 40)
        self.move(180, 60)

    def keyPressEvent(self, event):
        self.pressed_keys.add(event.key())
        if self.required_keys.issubset(self.pressed_keys):
            self.close()

    def keyReleaseEvent(self, event):
        if event.key() in self.pressed_keys:
            self.pressed_keys.remove(event.key())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Icon.ico"))
    window = PeekAssistant()
    window.show()
    sys.exit(app.exec_())

    # The "PeekAssistant" class is our reference to the current window object PeekAI runs within.


