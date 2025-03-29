import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt


class WeightPrizeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AcBuy calc")
        self.setGeometry(100, 100, 500, 400)

        # Set Dark Mode Theme
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; font-family: Arial; }
            QLabel { font-size: 14px; }
            QLineEdit { background-color: #1E1E1E; color: white; border: 1px solid #333; padding: 5px; border-radius: 5px; }
            QPushButton { background-color: #007ACC; color: white; border-radius: 5px; padding: 8px; font-size: 14px; }
            QPushButton:hover { background-color: #005F99; }
            QTextEdit { background-color: #1E1E1E; color: white; border: 1px solid #333; padding: 5px; font-family: Courier; }
        """)

        # Layout
        layout = QVBoxLayout()

        # Labels and Inputs
        self.total_weight_label = QLabel("Total Weight (leave blank to sum parts):")
        layout.addWidget(self.total_weight_label)

        self.total_weight_input = QLineEdit()
        layout.addWidget(self.total_weight_input)

        self.total_prize_label = QLabel("Total Prize (€):")
        layout.addWidget(self.total_prize_label)

        self.total_prize_input = QLineEdit()
        layout.addWidget(self.total_prize_input)

        self.parts_label = QLabel("Parts (comma-separated):")
        layout.addWidget(self.parts_label)

        self.parts_input = QLineEdit()
        layout.addWidget(self.parts_input)

        # Calculate Button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        # Results Box
        self.results_box = QTextEdit()
        self.results_box.setReadOnly(True)
        layout.addWidget(self.results_box)

        self.setLayout(layout)

    def calculate(self):
        try:
            total_prize = float(self.total_prize_input.text())
            parts = list(map(float, self.parts_input.text().split(',')))

            if self.total_weight_input.text().strip():
                total_weight = float(self.total_weight_input.text())
                if abs(sum(parts) - total_weight) > 1e-6:
                    raise ValueError("The parts do not sum up to the total weight.")
            else:
                total_weight = sum(parts)

            # Display results
            self.results_box.setPlainText("Part Weight (g)\tPrize (€)\n")
            self.results_box.append("================================")

            for part in parts:
                part_prize = (part / total_weight) * total_prize
                self.results_box.append(f"{part:.2f} g\t{part_prize:.2f} €")

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Enable Dark Mode (Optional)
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(18, 18, 18))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 224, 224))
    app.setPalette(dark_palette)

    window = WeightPrizeCalculator()
    window.show()
    sys.exit(app.exec())
