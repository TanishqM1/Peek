#  PeekAssistant — Lightweight AI Overlay

A minimal, desktop-only assistant that lets you instantly capture screenshots, enter prompts, or both — and get real-time answers via GPT-4o.

---

##  Current Functionality

PeekAssistant enables users to:

-  **Take screenshots** using a snipping tool overlay
-  **Enter prompts** to send questions or context
-  **Combine screenshot + prompt** for full context AI requests
-  **Toggle features** using global or in-focus hotkeys
-  **Stay out of your way** with a transparent, minimal UI and frameless design

All input is formatted and sent to the OpenAI API using GPT-4o, returning intelligent responses based on the visual and/or textual context provided. 
The goal of PeekAssitant is to be a 'stay-out-of-your-way' desktop agent that can be be used using only hotkeys, anywhere on your desktop.

---

##  Hotkeys

| Hotkey            | Action                                  |
|-------------------|------------------------------------------|
| `F4`              | Activate Peek logic (screenshot/prompt)  |
| `Ctrl + Alt + Q`  | Exit the application                     |
| `Ctrl + H`        | Toggle visibility of PeekAssistant       |
| `Ctrl + s`        | Toggle Screenshot switch                 |
| `Ctrl + p`        | Toggle Prompt switch                     |

---

##  Upcoming Features & Fixes

###  UI Design
 
- Dynamic positioning and animation for popups
- Preventing window clutter during snips/prompts
- Allowing out-of-focus functionality for the PeekAssistant window.

###  Backend & Functionality

- Working on optimizing prompt & image parameters through various prompt preparation techniques to ensure accurate results 
- Working seamlessly in with apps in **Borderless Fullscreen**.
- Error handling and input validation

### 💡 Future Ideas

- Support for switching between AI models (Claude, Gemini, GPT)
- “Advanced Mode” for prompt tuning (temperature, type of problem, saved project history, etc.)
- Ability to save screenshots/files as "prompt sessions"
- Response history sidebar or persistent thread mode
- Continued UI development, and minimalistic, easy to use design!

### Minimal Changes

- Add loading feedback for long API responses.
- File cleanup mechanism for .peek_cache to prevent buildup.
- Error popups (e.g., if no screenshot is captured or API fails).
- UI animation or subtle transitions to enhance user experience.

---
