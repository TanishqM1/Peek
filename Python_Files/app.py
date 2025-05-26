# app.py
import sys
import os
import time
import keyboard
import subprocess
from PyQt5.QtWidgets import QApplication, QInputDialog
from gui import PeekAssistant
from PyQt5.QtCore import QMetaObject, Qt, Q_ARG, QTimer

TEMP_FOLDER = os.path.join(os.getcwd(), ".peek_cache")

def toggle_visibility():
    if window.isVisible():
        window.hide()
    else:
        window.show()

def get_latest_screenshot():
    files = sorted(
        [f for f in os.listdir(TEMP_FOLDER) if f.endswith(".png")],
        key=lambda x: os.path.getmtime(os.path.join(TEMP_FOLDER, x)),
        reverse=True
    )
    return os.path.join(TEMP_FOLDER, files[0]) if files else None

def Execute():
    screenshot_enabled = window.ss_switch.isChecked()
    prompt_enabled = window.prompt_switch.isChecked()

    if screenshot_enabled and prompt_enabled:
        print("F4 → Screenshot and Prompt enabled")

        # Step 1: Run old screenshot script (blocking)
        subprocess.run([sys.executable, "Python_Files\screenshot.py"])

        # Step 2: Get the latest screenshot file
        image_path = get_latest_screenshot()
        if not image_path:
            print("No screenshot found.")
            return

        # Step 3: Use QTimer to safely prompt user from main thread
        def show_prompt():
            prompt, ok = QInputDialog.getText(window, "Ask ChatGPT", "Enter your question:")
            if ok and prompt.strip():
                print(f"Prompt: {prompt.strip()}")
                print(f"Screenshot path: {image_path}")
                # TODO: send to GPT here
            else:
                print("Prompt cancelled.")

        QTimer.singleShot(0, show_prompt)


    else:
        print("F4 → One or both toggles OFF")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PeekAssistant()
    window.show()

    keyboard.add_hotkey('ctrl+h', toggle_visibility)
    keyboard.add_hotkey('f4', Execute)

    sys.exit(app.exec_())
