import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QColorDialog, QVBoxLayout, QMainWindow, QSlider, QLabel
)
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
from pynput import keyboard
import pyautogui


class Overlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screen Highlighter")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self.drawing = False
        self.last_point = QPoint()
        self.lines = []
        self.pen_color = QColor(255, 255, 0, 120)
        self.opacity = 1.0
        self.click_through = False

        self.update_click_through()

    def update_click_through(self):
        if self.click_through:
            self.setWindowFlags(self.windowFlags() | Qt.WindowTransparentForInput)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowTransparentForInput)
        self.showFullScreen()

    def toggle_click_through(self):
        self.click_through = not self.click_through
        self.update_click_through()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.click_through:
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.lines.append((self.last_point, event.pos(), self.pen_color))
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        pen = QPen(self.pen_color, 10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        for start, end, color in self.lines:
            pen.setColor(color)
            painter.setPen(pen)
            painter.drawLine(start, end)

    def set_pen_color(self, color):
        self.pen_color = QColor(color.red(), color.green(), color.blue(), 120)

    def set_opacity(self, value):
        self.opacity = value / 100.0
        self.update()

    def clear_canvas(self):
        self.lines = []
        self.update()

    def save_screenshot(self):
        self.hide()
        QApplication.processEvents()
        screenshot = pyautogui.screenshot()
        screenshot.save("highlighted_screen.png")
        self.show()


class ToolBox(QWidget):
    def __init__(self, overlay):
        super().__init__()
        self.overlay = overlay
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: rgba(50, 50, 50, 220); border-radius: 8px; color: white;")
        layout = QVBoxLayout()

        color_btn = QPushButton("Pick Color")
        color_btn.clicked.connect(self.pick_color)
        layout.addWidget(color_btn)

        yellow_btn = QPushButton("Yellow")
        yellow_btn.clicked.connect(lambda: self.overlay.set_pen_color(QColor(255, 255, 0)))
        layout.addWidget(yellow_btn)

        green_btn = QPushButton("Green")
        green_btn.clicked.connect(lambda: self.overlay.set_pen_color(QColor(0, 255, 0)))
        layout.addWidget(green_btn)

        pink_btn = QPushButton("Pink")
        pink_btn.clicked.connect(lambda: self.overlay.set_pen_color(QColor(255, 105, 180)))
        layout.addWidget(pink_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.overlay.clear_canvas)
        layout.addWidget(clear_btn)

        save_btn = QPushButton("Save Screenshot")
        save_btn.clicked.connect(self.overlay.save_screenshot)
        layout.addWidget(save_btn)

        toggle_btn = QPushButton("Toggle Click-Through")
        toggle_btn.clicked.connect(self.overlay.toggle_click_through)
        layout.addWidget(toggle_btn)

        layout.addWidget(QLabel("Opacity"))
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(10)
        slider.setMaximum(100)
        slider.setValue(100)
        slider.valueChanged.connect(self.overlay.set_opacity)
        layout.addWidget(slider)

        layout.addWidget(QLabel("Hotkeys:"))
        layout.addWidget(QLabel("F8: Show/Hide Overlay"))
        layout.addWidget(QLabel("F9: Enable/Disable Drawing"))

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(QApplication.instance().quit)
        layout.addWidget(exit_btn)

        self.setLayout(layout)
        self.move(100, 100)
        self.resize(180, 360)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.overlay.set_pen_color(color)


def start_hotkey_listener(overlay, toolbox):
    def on_press(key):
        try:
            if key == keyboard.Key.f8:
                if overlay.isVisible():
                    overlay.hide()
                    toolbox.hide()
                else:
                    overlay.showFullScreen()
                    toolbox.show()
            elif key == keyboard.Key.f9:
                overlay.toggle_click_through()
        except Exception as e:
            print("Hotkey error:", e)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    overlay = Overlay()
    overlay.showFullScreen()

    toolbox = ToolBox(overlay)
    toolbox.show()

    threading.Thread(target=start_hotkey_listener, args=(overlay, toolbox), daemon=True).start()

    sys.exit(app.exec_())
