from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt

class PromptDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PeekPrompt")
        self.setFixedSize(400, 140)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                border: 1px solid #444;
                border-radius: 10px;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 6px;
                font-size: 13px;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #555;
            }
        """)

        self.prompt = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel("Enter Prompt:")
        self.textbox = QLineEdit()
        layout.addWidget(label)
        layout.addWidget(self.textbox)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)

        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept_prompt)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def accept_prompt(self):
        text = self.textbox.text().strip()
        if text:
            self.prompt = text
            self.accept()
