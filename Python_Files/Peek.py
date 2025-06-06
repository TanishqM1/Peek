# app.py
import sys
import os
import subprocess
import threading
import keyboard
from PyQt5.QtWidgets import QApplication, QShortcut, QDialog
from PyQt5.QtGui import QKeySequence
from gui import PeekAssistant
from prompt import PromptDialog  # custom prompt window
from api_request import chat_with_gpt
from PyQt5.QtGui import QIcon
from response import ResponsePopup

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, Qt


TEMP_FOLDER = os.path.join(os.getcwd(), ".peek_cache")

# function to toggle window visibility (ctrl h)
def toggle_visibility():
    if window.isVisible():
        window.hide()
    else:
        window.show()

def togglescreenshot():
    window.ss_switch.toggle()

def toggleprompt():
    window.prompt_switch.toggle()

def force_focus(widget):
    widget.raise_()
    widget.activateWindow()
    widget.setFocus()


class HotkeyDispatcher(QObject): #dispatcher so we can listen for f4 globally, outside of window focus.
    f4_triggered = pyqtSignal()


# function to get latest screenshot (prompt prep)
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

# checking f4 logic (levers and information needed).
def run_f4_logic():
    print("[Qt] Running F4 logic")
    screenshot_enabled = window.ss_switch.isChecked()
    prompt_enabled = window.prompt_switch.isChecked()
    print(f"Switches: screenshot={screenshot_enabled}, prompt={prompt_enabled}")
    window.raise_()
    window.setFocus()

    # CASE: both switches are ON
    if screenshot_enabled and prompt_enabled:
        print("[F4] Launching screenshot.py...")
        toggle_visibility()
        subprocess.run([sys.executable, "Python_Files\\screenshot.py"])

        image_path = get_latest_screenshot()
        if not image_path:
            print("No screenshot found.")
            return

        dialog = PromptDialog()
        dialog.move(window.pos())
        dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        dialog.show()
        QTimer.singleShot(100, lambda: force_focus(dialog))  # delay helps event loop catch up
        
        if dialog.exec_():
            prompt = dialog.prompt
            print(f"Prompt: {prompt}")
            print(f"Screenshot path: {image_path}")
        
            response = chat_with_gpt(prompt=prompt, image_path=image_path)
            print(response)
            popup = ResponsePopup(response)
            popup.exec_()
        

        else:
            print("Prompt cancelled.")
        toggle_visibility()

    # CASE: screenshot only!
    elif screenshot_enabled and not prompt_enabled:
        print("[F4] Screenshot only mode")
        toggle_visibility()
        subprocess.run([sys.executable, "Python_Files\\screenshot.py"])
        image_path = get_latest_screenshot()

        response = chat_with_gpt(prompt="Please Solve This", image_path=image_path)
        print(response)
        popup = ResponsePopup(response)
        popup.exec_()

        if not image_path:
            print("No screenshot was saved.")
            return
        print(f"[F4] Screenshot saved to: {image_path}")
        toggle_visibility()

    # CASE: prompt only!
    elif prompt_enabled and not screenshot_enabled:
        print("[F4] Prompt only mode")
        toggle_visibility()
        dialog = PromptDialog()
        dialog.move(window.pos())
        dialog.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        dialog.show()
        QTimer.singleShot(100, lambda: force_focus(dialog))  # delay helps event loop catch up


        if dialog.exec_():
            prompt = dialog.prompt
            print(f"[F4] User prompt: {prompt}")

            response = chat_with_gpt(prompt=prompt)
            print(response)
            popup = ResponsePopup(response)
            popup.exec_()
        else:
            print("Prompt cancelled or empty.")
        toggle_visibility()
    else:
        print("Both Switches Are Off!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Icon.ico"))
    window = PeekAssistant()
    window.show()

    #initialize dispatcher
    dispatcher = HotkeyDispatcher()
    dispatcher.f4_triggered.connect(run_f4_logic)

    # Listen globally for ctrl+h
    def hotkeys():
        keyboard.add_hotkey('ctrl+h', toggle_visibility)
        keyboard.add_hotkey('ctrl+s', togglescreenshot)
        keyboard.add_hotkey('ctrl+p', toggleprompt)
        keyboard.add_hotkey('f4', lambda: dispatcher.f4_triggered.emit())
    threading.Thread(target=hotkeys, daemon=True).start()

    # local f4 hotkey. (must be run by the same thread as PyQT, otherwise it will crash.)
    # this means, the f4 hotkey will only run if that window is in focus.
    # a workaround, though not optimized is having a global f4 key, and running the logic using the same thread if pressed manually.
    # f4_shortcut = QShortcut(QKeySequence("F4"), window)
    # f4_shortcut.activated.connect(run_f4_logic)

    sys.exit(app.exec_())
