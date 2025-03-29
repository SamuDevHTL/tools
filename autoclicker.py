import sys
import pyautogui
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QPalette, QColor


class AutoClickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Auto Clicker")
        self.setGeometry(100, 100, 400, 300)

        # Dark theme
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: Arial; }
            QLabel { font-size: 14px; }
            QLineEdit, QComboBox { background-color: #1E1E1E; color: white; border: 1px solid #333; padding: 5px; border-radius: 5px; }
            QPushButton { background-color: #007ACC; color: white; border-radius: 5px; padding: 8px; font-size: 14px; }
            QPushButton:hover { background-color: #005F99; }
        """)

        layout = QVBoxLayout()

        self.label_clicks = QLabel("How many clicks?")
        layout.addWidget(self.label_clicks)

        self.num_clicks_input = QLineEdit()
        self.num_clicks_input.setPlaceholderText("Enter a number")
        layout.addWidget(self.num_clicks_input)

        self.label_delay = QLabel("Delay between clicks (seconds):")
        layout.addWidget(self.label_delay)

        self.delay_input = QLineEdit()
        self.delay_input.setPlaceholderText("Enter a number (e.g. 0.1)")
        layout.addWidget(self.delay_input)

        self.label_button = QLabel("Click Type:")
        layout.addWidget(self.label_button)

        self.click_type = QComboBox()
        self.click_type.addItems(["Left Click", "Right Click"])
        layout.addWidget(self.click_type)

        self.start_button = QPushButton("Start Clicking")
        self.start_button.clicked.connect(self.start_countdown)
        layout.addWidget(self.start_button)

        self.status_label = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_countdown(self):
        try:
            self.num_clicks = int(self.num_clicks_input.text())
            self.delay = float(self.delay_input.text())

            if self.num_clicks <= 0 or self.delay < 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter valid numbers.")
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
            self.status_label.setText("🖱️ Clicking now...")
            QTimer.singleShot(500, self.start_clicking)  # Small delay before starting
        else:
            self.status_label.setText(f"Starting in {self.countdown}...")

    def start_clicking(self):
        click_type = "left" if self.click_type.currentText() == "Left Click" else "right"

        for _ in range(self.num_clicks):
            pyautogui.click(button=click_type)
            QTimer.singleShot(int(self.delay * 1000), lambda: None)  # Simulate delay

        self.status_label.setText("✅ Completed!")
        self.start_button.setDisabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Enable Dark Mode (Optional)
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 224, 224))
    app.setPalette(dark_palette)

    window = AutoClickerApp()
    window.show()
    sys.exit(app.exec())
