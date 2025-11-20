# 🔍 PeekAssistant — Lightweight AI Overlay

A minimal, **desktop-only** assistant that lets you instantly capture screenshots, enter prompts, or both — and get real-time answers via **GPT-4o**.

PeekAssistant is designed to be a 'stay-out-of-your-way' desktop agent that can be used using only **hotkeys**, anywhere on your desktop. Its **transparent/translucent background** ensures it remains non-intrusive. You can see a demo/installation of the app at peekassistant.vercel.app

---

##  Tech Stack

PeekAssistant is built using a robust, cross-platform architecture:

* **Python:** The core programming language.
* **LLM APIs:** Primary integration with **OpenAI's GPT-4o** for high-quality, multimodal AI responses.
* **PyQt5:** Used for creating the minimal, frameless, and highly customizable desktop UI.

---

##  Key Features

PeekAssistant enables users to leverage AI instantly through **dynamic prompting** and **screenshot capture within any application**.

* **Take Screenshots** 📸: Use a built-in snipping tool overlay to capture specific regions of your screen.
* **Enter Prompts** 💬: Send questions or context via a minimal text input.
* **Combined Context** ✨: Seamlessly **combine a screenshot + a textual prompt** for full-context AI requests.
* **Hotkeys Only** ⌨️: Activate the core logic and toggle features using global or in-focus hotkeys.
* **Non-Intrusive Design** 👻: A transparent, minimal UI and frameless design ensure it stays out of your way.

All input is formatted and sent to the OpenAI API using **GPT-4o**, returning intelligent responses based on the visual and/or textual context provided.

---

##  Getting Started (Beta)

To use the application (beta):

1.  Clone the repository.
2.  Create a **`.env`** file in the root directory (or launch Peek.exe, it will prompt you for a key).
3.  Add your OpenAI API key as an environment variable: `CHATGPT_KEY = "[your_key]"`.
4.  Run `Peek.py` to launch the application.

---

## 🔑 Hotkeys

| Hotkey | Action |
| :--- | :--- |
| `F4` | Activate Peek logic (screenshot/prompt/both) |
| `Ctrl + Alt + Q` | Exit the application |
| `Ctrl + H` | Toggle visibility of PeekAssistant |
| `Ctrl + s` | Toggle Screenshot switch |
| `Ctrl + p` | Toggle Prompt switch |

---


### 🛠️ Backend & Functionality

* Optimized & image parameters for accurate results.
* Enhancing compatibility to work seamlessly in **Borderless Fullscreen** applications.
* Improved error handling and input validation.
* Add **loading feedback** for long API responses.
* File cleanup mechanism for `.peek_cache` to prevent buildup.
* Error popups (e.g., if no screenshot is captured or API fails).

### 🎨 UI Design

* Dynamic positioning and animation for popups.
* Preventing window clutter during snips/prompts.
* Allowing out-of-focus functionality for the PeekAssistant window.
* UI animation or subtle transitions to enhance user experience.
