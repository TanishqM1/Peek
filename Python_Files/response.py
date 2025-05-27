from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QDesktopWidget
from PyQt5.QtCore import Qt

class ResponsePopup(QDialog):
    def __init__(self, response_text: str):
        super().__init__()
        self.setWindowTitle("AI Response")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.init_ui(response_text)
        self.adjust_position_and_size()

    def init_ui(self, text):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        container = QDialog()
        container.setStyleSheet("""
            QDialog {
                background-color: rgba(30, 30, 30, 245);  /* Slightly more opaque */
                border: 1px solid #444;
                border-radius: 12px;
            }
            QTextEdit {
                background-color: transparent;
                color: #dddddd;
                border: none;
                padding: 12px;
                font-size: 14px;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
                line-height: 1.6;
                letter-spacing: 0.2px;
            }
            QPushButton {
                background-color: transparent;
                color: #aaa;
                font-size: 16px;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        inner_layout = QVBoxLayout(container)
        inner_layout.setContentsMargins(10, 10, 10, 10)
        inner_layout.setSpacing(5)

        top_bar = QHBoxLayout()
        top_bar.addStretch()
        close_btn = QPushButton("✕")
        close_btn.clicked.connect(self.close)
        top_bar.addWidget(close_btn)
        inner_layout.addLayout(top_bar)

        response_view = QTextEdit()
        response_view.setReadOnly(True)
        response_view.setText(text)
        response_view.setWordWrapMode(True)
        inner_layout.addWidget(response_view)

        outer_layout.addWidget(container)

    def adjust_position_and_size(self):
        screen = QDesktopWidget().availableGeometry()
        width = 500
        height = screen.height() - 100
        self.setFixedSize(width, height)

        x = screen.right() - width - 20
        y = screen.top() + 50
        self.move(x, y)
