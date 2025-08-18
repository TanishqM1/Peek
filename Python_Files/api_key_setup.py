import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QWidget
)
from PyQt5.QtCore import Qt

def get_appdata_path():
    appdata = os.getenv("APPDATA") or os.path.expanduser("~/.config")
    path = os.path.join(appdata, "Peek")
    os.makedirs(path, exist_ok=True)
    return path

def get_config_file():
    return os.path.join(get_appdata_path(), "config.json")

class ApiKeyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Peek Setup")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.api_key = None
        self.init_ui()

    def init_ui(self):
        # Main layout for the dialog
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container background (the small translucent window)
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 20, 220);
                border-radius: 14px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(12)

        # Title
        label = QLabel("Enter your OpenAI API key")
        label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        container_layout.addWidget(label)

        # Input field
        self.textbox = QLineEdit()
        self.textbox.setEchoMode(QLineEdit.Password)
        self.textbox.setPlaceholderText("sk-...")
        self.textbox.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0,0,0,210);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #2196f3;
            }
        """)
        container_layout.addWidget(self.textbox)

        # Buttons row
        btn_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        ok_btn = QPushButton("Save")
        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.accept_key)

        for btn in (cancel_btn, ok_btn):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0,0,0, 240);
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 14px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #2196f3;
                    color: white;
                }
            """)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        container_layout.addLayout(btn_layout)

        # Add container into dialog
        layout.addWidget(container)

        # Set dialog size so container is just bigger than content
        self.setFixedSize(360, 190)

        # Transparent outside background
        self.setStyleSheet("""
            QDialog {
                background-color: transparent;
            }
        """)

    def accept_key(self):
        key = self.textbox.text().strip()
        if key:
            self.api_key = key
            self.save_key(key)
            self.accept()

    def save_key(self, key: str):
        config_file = get_config_file()
        config = {"api_key": key}
        with open(config_file, "w") as f:
            json.dump(config, f, indent=4)
