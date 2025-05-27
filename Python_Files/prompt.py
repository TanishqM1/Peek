from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
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
                background-color: rgba(30, 30, 30, 180);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
            }
            QTextEdit {
                background-color: rgba(0,0,0,210);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
                padding: 6px;
                font-size: 13px;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
            }
            QPushButton {
                background-color: rgba(0,0,0, 240);
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 10px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        self.textbox = QTextEdit()
        self.textbox.setPlaceholderText("Enter your prompt here...")
        self.textbox.textChanged.connect(self.adjust_textbox_height)
        layout.addWidget(self.textbox)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        no_btn = QPushButton("X")
        yes_btn = QPushButton("Yes")
        no_btn.clicked.connect(self.reject)
        yes_btn.clicked.connect(self.accept_prompt)
        btn_layout.addWidget(no_btn)
        btn_layout.addWidget(yes_btn)
        layout.addLayout(btn_layout)

        self.adjust_textbox_height()

    def adjust_textbox_height(self):
        doc_height = self.textbox.document().size().height()
        self.textbox.setFixedHeight(int(doc_height + 20))
        self.resize(self.width(), self.textbox.height() + 60)

    def accept_prompt(self):
        text = self.textbox.toPlainText().strip()
        if text:
            self.prompt = text
            self.accept()

    # Drag-to-move functionality
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
