import sys
import pyautogui
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QPalette, QColor


class AutoTyperApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Auto Typer")
        self.setGeometry(100, 100, 400, 250)

        # Set dark theme
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: Arial; }
            QLabel { font-size: 14px; }
            QLineEdit { background-color: #1E1E1E; color: white; border: 1px solid #333; padding: 5px; border-radius: 5px; }
            QPushButton { background-color: #007ACC; color: white; border-radius: 5px; padding: 8px; font-size: 14px; }
            QPushButton:hover { background-color: #005F99; }
        """)

        # Layout
        layout = QVBoxLayout()

        self.label = QLabel("Enter Sentence:")
        layout.addWidget(self.label)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        self.label2 = QLabel("How many times?")
        layout.addWidget(self.label2)

        self.num_input = QLineEdit()
        self.num_input.setPlaceholderText("Enter a number")
        layout.addWidget(self.num_input)

        # Start Button
        self.start_button = QPushButton("Start Typing")
        self.start_button.clicked.connect(self.start_countdown)
        layout.addWidget(self.start_button)

        # Countdown Status
        self.status_label = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_countdown(self):
        self.word = self.text_input.text()
        try:
            self.num = int(self.num_input.text())
            if not self.word or self.num <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid sentence and a positive number.")
            return

        self.countdown = 3
        self.status_label.setText(f"Starting in {self.countdown}...")
        self.start_button.setDisabled(True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)

    def update_countdown(self):
        self.countdown -= 1
        if self.countdown == 0:
            self.timer.stop()
            self.status_label.setText("⌨️ Typing now...")  # ✅ Now updates correctly!
            QTimer.singleShot(500, self.start_typing)  # Small delay before typing
        else:
            self.status_label.setText(f"Starting in {self.countdown}...")

    def start_typing(self):
        for _ in range(self.num):
            pyautogui.typewrite(self.word)
            pyautogui.press("enter")

        self.status_label.setText("✅ Completed!")
        self.start_button.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Enable Dark Mode in Windows (Optional)
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 224, 224))
    app.setPalette(dark_palette)

    window = AutoTyperApp()
    window.show()
    sys.exit(app.exec())