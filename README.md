Core Responsibilities of app.py:
1. Launch the GUI
Initialize the QApplication

Show the PeekAssistant window

Allow user interaction with the switches

2. Define a Macro Trigger
Use a keyboard macro (e.g. Ctrl + Shift + S) or custom global hotkey handler

When pressed, trigger a handler function inside app.py

3. Read State from the GUI
In the macro callback, check:

window.ss_switch.isChecked() → screenshot enabled?

window.prompt_switch.isChecked() → prompt enabled?

4. Conditional Actions
If screenshot is enabled: call a take_screenshot() function and save the image path

If prompt is enabled: show a QInputDialog or custom prompt box to get user input

5. Send API Request
Combine the screenshot and prompt (whichever are active)

Pass to send_prompt_with_image(prompt, image_path) or similar