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
        self.setFixedSize(32, 18)
        self.setStyleSheet("""
            QCheckBox::indicator {
                width: 32px;
                height: 18px;
                border-radius: 9px;
                background-color: #555;
            }
            QCheckBox::indicator:checked {
                background-color: #2196f3;
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
                background-color: rgba(30, 30, 30, 235);
                border-radius: 14px;
            }
            QLabel {
                color: white;
            }
        """)

        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(12, 6, 12, 6)
        frame_layout.setSpacing(12)

        # Title
        title = QLabel("PeekAI")
        title.setStyleSheet("font-weight: bold; font-size: 13px; color: white;")
        title.setAlignment(Qt.AlignVCenter)
        frame_layout.addWidget(title, alignment=Qt.AlignVCenter)

        # Screenshot switch row
        self.ss_switch = ToggleSwitch()
        ss_layout = QHBoxLayout()
        ss_layout.setSpacing(6)
        ss_label = QLabel("Screenshot")
        ss_label.setAlignment(Qt.AlignVCenter)
        ss_label.setStyleSheet("font-weight: bold; font-size: 11px; color: white;")
        ss_layout.addWidget(ss_label)
        ss_layout.addWidget(self.ss_switch)
        frame_layout.addLayout(ss_layout)

        # Prompt switch row
        self.prompt_switch = ToggleSwitch()
        prompt_layout = QHBoxLayout()
        prompt_layout.setSpacing(6)
        prompt_label = QLabel("Prompt")
        prompt_label.setAlignment(Qt.AlignVCenter)
        prompt_label.setStyleSheet("font-weight: bold; font-size: 11px; color: white;")
        prompt_layout.addWidget(prompt_label)
        prompt_layout.addWidget(self.prompt_switch)
        frame_layout.addLayout(prompt_layout)

        frame.setLayout(frame_layout)
        outer_layout.addWidget(frame)
        self.setLayout(outer_layout)

        self.setFixedSize(320, 44)
        self.move(180, 60)

    # --- interactions ---
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
