from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class PromptDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prompt")
        self.resize(322, 80)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 6px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: white;
                border-radius: 6px;
                padding: 6px;
                font-size: 12px;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 2px 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)

        self.prompt = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        self.textbox = QTextEdit()
        self.textbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox.setPlaceholderText("enter additional information for ai prompt")


        self.textbox.setFixedHeight(40)
        self.textbox.setSizePolicy(
            self.textbox.sizePolicy().horizontalPolicy(),
            self.textbox.sizePolicy().Expanding
        )
        self.textbox.textChanged.connect(self.adjust_textbox_height)
        layout.addWidget(self.textbox)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)

        cancel_btn = QPushButton("X")
        ok_btn = QPushButton("OK")

        cancel_btn.setFixedSize(40, 18)
        ok_btn.setFixedSize(40, 18)

        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.accept_prompt)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def adjust_textbox_height(self):
        doc_height = self.textbox.document().size().height()
        new_height = int(doc_height + 10)
        self.textbox.setFixedHeight(new_height)
        self.resize(self.width(), new_height + 50)

    def accept_prompt(self):
        text = self.textbox.toPlainText().strip()
        if text:
            self.prompt = text
            self.accept()
    

