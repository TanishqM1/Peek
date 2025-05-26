import sys
import keyboard
from PyQt5.QtWidgets import QApplication
from gui import PeekAssistant

def toggle_visibility():
    if window.isVisible():
        window.hide()
    else:
        window.show()

def Execute():
    screenshot_enabled = window.ss_switch.isChecked()
    prompt_enabled = window.prompt_switch.isChecked()
    
    # You can store them in variables, send them to a function, or log them
    print(f"F4 pressed → Screenshot: {screenshot_enabled}, Prompt: {prompt_enabled}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Launch the GUI
    window = PeekAssistant()
    window.show()

    # Register macros
    keyboard.add_hotkey('ctrl+h', toggle_visibility)
    keyboard.add_hotkey('f4', Execute)

    # Start the event loop
    sys.exit(app.exec_())
