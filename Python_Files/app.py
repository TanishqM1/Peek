from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
from Python_Files.screenshot import start_snip
from Python_Files.api_request import chat_with_gpt_image
import sys

def handle_capture(image_path):
    prompt, ok = QInputDialog.getText(None, "Ask ChatGPT", "Enter your question about the screenshot:")
    if ok and prompt.strip():
        reply = chat_with_gpt_image(prompt.strip(), image_path)

        msg = QMessageBox()
        msg.setWindowTitle("ChatGPT Response")
        msg.setText(reply)
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_snip(callback=handle_capture)
