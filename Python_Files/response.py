from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QTextBrowser, QDesktopWidget
from PyQt5.QtCore import Qt
import re

class ResponsePopup(QDialog):
    def __init__(self, response_text: str):
        super().__init__()
        self.setWindowTitle("AI Response")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.init_ui(self.format_text(response_text))
        self.adjust_position_and_size()

    def init_ui(self, html_text):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        container = QDialog()
        container.setStyleSheet("""
            QDialog {
                background-color: rgba(30, 30, 30, 245);
                border: 1px solid #444;
                border-radius: 12px;
            }
            QTextBrowser {
                background-color: transparent;
                color: #dddddd;
                border: none;
                padding: 12px;
                font-size: 14px;
                font-family: "Segoe UI", "Helvetica Neue", sans-serif;
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

        response_view = QTextBrowser()
        response_view.setOpenExternalLinks(True)
        response_view.setHtml(html_text)
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

    def format_text(self, text: str) -> str:
        # Escape HTML
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        # Code blocks (```code```)
        text = re.sub(r"```(?:\w*\n)?(.*?)```", r"<pre style='background-color:#1e1e1e;color:#c5c8c6;padding:8px;border-radius:6px;'>\1</pre>", text, flags=re.DOTALL)

        # Inline code (`code`)
        text = re.sub(r"`([^`\n]+)`", r"<code style='background-color:#2d2d2d;padding:2px 4px;border-radius:4px;'>\1</code>", text)

        # Bold+Italic (***text***)
        text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<b><i>\1</i></b>", text)

        # Bold (**text**)
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

        # Italic (*text*)
        text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)

        # Headers
        text = re.sub(r"^### (.*)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
        text = re.sub(r"^## (.*)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
        text = re.sub(r"^# (.*)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)

        # Blockquotes
        text = re.sub(r"^> (.*)$", r"<blockquote style='margin:4px 0;padding-left:10px;border-left:2px solid #888;'>\1</blockquote>", text, flags=re.MULTILINE)

        # Horizontal rules
        text = re.sub(r"^(---|\*\*\*)$", r"<hr>", text, flags=re.MULTILINE)

        # Bullet list
        text = re.sub(r"^- (.*)$", r"<li>\1</li>", text, flags=re.MULTILINE)
        if "<li>" in text:
            text = re.sub(r"(<li>.*?</li>)", r"<ul>\1</ul>", text, flags=re.DOTALL)

        # Numbered list
        text = re.sub(r"^\d+\. (.*)$", r"<li>\1</li>", text, flags=re.MULTILINE)
        if "<li>" in text and "<ul>" not in text:
            text = re.sub(r"(<li>.*?</li>)", r"<ol>\1</ol>", text, flags=re.DOTALL)

        # Line breaks
        text = text.replace("\n", "<br>")

        return f"<div>{text}</div>"

