# Screen Highlighter Overlay (PyQt5)

A lightweight, fullscreen annotation tool built with Python and PyQt5 that lets you **draw over your entire screen**, change highlighter color, adjust opacity, take screenshots, and toggle between drawing and interacting with underlying windows.

---

## Features

- **Draw over your live desktop** using transparent ink
- **Floating toolbox** with:
  - Color picker + quick color buttons
  - Clear all
  - Save screenshot (`PNG`)
  - Toggle click-through mode (drawing vs. interacting)
  - Opacity slider
  - Exit button
- **Global Hotkeys**
  - `F8` — Show/Hide the overlay and toolbox
  - `F9` — Enable/Disable drawing mode (toggle click-through)
- **Multi-color support** (Yellow, Green, Pink, or custom)
- **Works on Linux/X11**

---

## Requirements

Install dependencies using pip:

```bash
pip install PyQt5 pynput pyautogui
```

---

## How to Run

1. Save the code as `highlighter.py`
2. Open a terminal and run:

```bash
python highlighter.py
```

---

## How to Use

| Action                      | How To Do It                                |
|----------------------------|---------------------------------------------|
| **Draw on screen**         | Click and drag with mouse                   |
| **Pick color**             | Use toolbox buttons or "Pick Color" dialog  |
| **Adjust opacity**         | Use the opacity slider                      |
| **Clear everything**       | Click "Clear All" in the toolbox            |
| **Save screenshot**        | Click "Save Screenshot" (includes your drawing + background) |
| **Exit**                   | Click "Exit" or press `Ctrl+C` in terminal  |
| **Toggle overlay (F8)**    | Show/hide the overlay and toolbox globally  |
| **Toggle drawing (F9)**    | Enable or disable interaction (click-through mode) |

---

## Click-Through Mode (Draw/Interact Toggle)

When enabled (via F9 or the "Toggle Click-Through" button), the overlay becomes **click-through**:
- You can interact with windows under the overlay
- Useful for scrolling web pages or clicking buttons
- Press F9 again to return to drawing mode

---

## Screenshot Saving

- Click **"Save Screenshot"**
- Captures your full screen **with** any drawing over it
- Saves as: `highlighted_screen.png` in the same folder

---

## Notes

- This is optimized for **Linux/X11**
- Wayland is not officially supported (PyQt5 limitations with transparency/click-through)
- Screenshot functionality uses `pyautogui` — it must run in an environment that supports it (no Wayland or headless)

---

## Roadmap Ideas (Feel free to expand!)

- [ ] Undo/Redo
- [ ] Save/load multiple drawings
- [ ] Export transparent overlay only (no background)
- [ ] Stylus pressure support
- [ ] Global tray icon

---

## Credits

Built with love using Python, PyQt5, and a lot of trial-and-error across window managers.
