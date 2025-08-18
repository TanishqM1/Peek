import sys
import os
import json
import subprocess
import threading
import keyboard
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt

from gui import PeekAssistant


# ---------- Config handling ----------
def get_appdata_path():
    appdata = os.getenv("APPDATA") or os.path.expanduser("~/.config")
    path = os.path.join(appdata, "Peek")
    os.makedirs(path, exist_ok=True)
    return path

def get_config_file():
    return os.path.join(get_appdata_path(), "config.json")

def load_config():
    config_file = get_config_file()
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# ---------- Focus helper ----------
def force_focus(widget):
    widget.raise_()
    widget.activateWindow()
    widget.setFocus()

# ---------- Hotkey dispatcher ----------
class HotkeyDispatcher(QObject):
    f4_triggered = pyqtSignal()

# ---------- Peek main ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Icon.ico"))

    # Load API key
    config = load_config()
    api_key = config.get("api_key")
    if not api_key:
        from api_key_setup import ApiKeyDialog
        dialog = ApiKeyDialog()
        if dialog.exec_():
            api_key = dialog.api_key
        else:
            QMessageBox.warning(None, "Peek", "No API key entered. Exiting.")
            sys.exit(0)
    os.environ["CHATGPT_KEY"] = api_key

    # Launch assistant
    window = PeekAssistant()
    window.show()

    # Hotkey dispatcher
    dispatcher = HotkeyDispatcher()

    # ----- Hotkey functions -----
    def toggle_visibility():
        if window.isVisible():
            window.hide()
        else:
            window.show()
            force_focus(window)

    def togglescreenshot():
        window.ss_switch.toggle()
        force_focus(window)

    def toggleprompt():
        window.prompt_switch.toggle()
        force_focus(window)

    def run_f4_logic():
        print("[Qt] Running F4 logic")
        screenshot_enabled = window.ss_switch.isChecked()
        prompt_enabled = window.prompt_switch.isChecked()
        print(f"Switches: screenshot={screenshot_enabled}, prompt={prompt_enabled}")

        window.raise_()
        window.setFocus()

        # Screenshot + prompt
        if screenshot_enabled and prompt_enabled:
            print("[F4] Screenshot + Prompt")
            toggle_visibility()
            subprocess.run([sys.executable, "screenshot.py"])  # capture screenshot

            # find latest screenshot
            temp_folder = os.path.join(os.getcwd(), ".peek_cache")
            files = [f for f in os.listdir(temp_folder) if f.endswith(".png")]
            if not files:
                print("No screenshot found.")
                toggle_visibility()
                return
            latest = max(files, key=lambda x: os.path.getmtime(os.path.join(temp_folder, x)))
            image_path = os.path.join(temp_folder, latest)

            dialog = PromptDialog()
            dialog.move(window.pos())
            dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            dialog.show()
            QTimer.singleShot(100, lambda: force_focus(dialog))

            if dialog.exec_():
                prompt = dialog.prompt
                response = chat_with_gpt(prompt=prompt, image_path=image_path)
                popup = ResponsePopup(response)
                popup.exec_()
            toggle_visibility()

        # Screenshot only
        elif screenshot_enabled:
            print("[F4] Screenshot only")
            toggle_visibility()
            subprocess.run([sys.executable, "screenshot.py"])
            temp_folder = os.path.join(os.getcwd(), ".peek_cache")
            files = [f for f in os.listdir(temp_folder) if f.endswith(".png")]
            if not files:
                print("No screenshot found.")
                toggle_visibility()
                return
            latest = max(files, key=lambda x: os.path.getmtime(os.path.join(temp_folder, x)))
            image_path = os.path.join(temp_folder, latest)

            response = chat_with_gpt(prompt="Please solve this", image_path=image_path)
            popup = ResponsePopup(response)
            popup.exec_()
            toggle_visibility()

        # Prompt only
        elif prompt_enabled:
            print("[F4] Prompt only")
            toggle_visibility()
            dialog = PromptDialog()
            dialog.move(window.pos())
            dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
            dialog.show()
            QTimer.singleShot(100, lambda: force_focus(dialog))

            if dialog.exec_():
                prompt = dialog.prompt
                response = chat_with_gpt(prompt=prompt)
                popup = ResponsePopup(response)
                popup.exec_()
            toggle_visibility()

        else:
            print("[F4] Both switches off!")

    dispatcher.f4_triggered.connect(run_f4_logic)

    # Global hotkeys
    def hotkeys():
        keyboard.add_hotkey("ctrl+h", toggle_visibility)
        keyboard.add_hotkey("ctrl+s", togglescreenshot)
        keyboard.add_hotkey("ctrl+p", toggleprompt)
        keyboard.add_hotkey("f4", lambda: dispatcher.f4_triggered.emit())

    threading.Thread(target=hotkeys, daemon=True).start()

    sys.exit(app.exec_())
