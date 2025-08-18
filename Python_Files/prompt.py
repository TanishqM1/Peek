from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, QPoint

class PromptDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prompt")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.prompt = None
        self.dragging = False
        self.offset = QPoint()

        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
            }
            QFrame#Container {
                background-color: rgba(30, 30, 30, 200);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
            }
            QTextEdit {
                background-color: transparent;
                color: white;
                border: none;
                padding: 8px;
                font-size: 13px;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2196f3;
                color: white;
            }
        """)

        self.init_ui()

    def init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        # ---- One container frame ----
        container = QFrame()
        container.setObjectName("Container")
        container_layout = QHBoxLayout(container)  # horizontal so text + buttons share one row
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(6)

        # --- Textbox (expands left) ---
        self.textbox = QTextEdit()
        self.textbox.setPlaceholderText("Enter your prompt here...")
        self.textbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox.textChanged.connect(self.adjust_textbox_height)
        container_layout.addWidget(self.textbox, stretch=1)  # take up most space

        # --- Buttons inline to the right ---
        self.no_btn = QPushButton("X")
        self.yes_btn = QPushButton("Yes")
        self.no_btn.clicked.connect(self.reject)
        self.yes_btn.clicked.connect(self.accept_prompt)
        container_layout.addWidget(self.no_btn)
        container_layout.addWidget(self.yes_btn)

        outer_layout.addWidget(container)

        self.adjust_textbox_height()
        self.textbox.setFocus()

    def adjust_textbox_height(self):
        doc_height = self.textbox.document().size().height()
        max_height = 250
        self.textbox.setFixedHeight(min(int(doc_height + 20), max_height))
        self.resize(self.width(), self.textbox.height() + 40)

    def accept_prompt(self):
        text = self.textbox.toPlainText().strip()
        if text:
            self.prompt = text
            self.accept()

    # --- Keyboard shortcuts ---
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.accept_prompt()
        elif event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)

    # Drag-to-move
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
