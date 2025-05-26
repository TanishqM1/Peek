# app.py
import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QInputDialog, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QTimer
from gui import PeekAssistant

TEMP_FOLDER = os.path.join(os.getcwd(), ".peek_cache")

def toggle_visibility():
    if window.isVisible():
        window.hide()
    else:
        window.show()

def get_latest_screenshot():
    try:
        files = [f for f in os.listdir(TEMP_FOLDER) if f.endswith(".png")]
        if not files:
            return None
        latest = max(files, key=lambda x: os.path.getmtime(os.path.join(TEMP_FOLDER, x)))
        return os.path.join(TEMP_FOLDER, latest)
    except Exception as e:
        print("Error locating screenshot:", e)
        return None

def run_f4_logic():
    print("[Qt] Running F4 logic")
    screenshot_enabled = window.ss_switch.isChecked()
    prompt_enabled = window.prompt_switch.isChecked()
    print(f"Switches: screenshot={screenshot_enabled}, prompt={prompt_enabled}")

    if screenshot_enabled and prompt_enabled:
        print("[F4] Launching screenshot.py...")
        subprocess.run([sys.executable, "Python_Files\screenshot.py"])

        image_path = get_latest_screenshot()
        if not image_path:
            print("No screenshot found.")
            return

        prompt, ok = QInputDialog.getText(window, "Ask ChatGPT", "Enter your question:")
        if ok and prompt.strip():
            print(f"Prompt: {prompt.strip()}")
            print(f"Screenshot path: {image_path}")
        else:
            print("Prompt cancelled.")
            
    else:
        print("[F4] Skipping – one or both toggles are off")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PeekAssistant()
    window.show()

    # 🔥 Qt-native hotkeys — NO threading issues
    toggle_shortcut = QShortcut(QKeySequence("Ctrl+H"), window)
    toggle_shortcut.activated.connect(toggle_visibility)

    f4_shortcut = QShortcut(QKeySequence("F4"), window)
    f4_shortcut.activated.connect(run_f4_logic)

    sys.exit(app.exec_())
