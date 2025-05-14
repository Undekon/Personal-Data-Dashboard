import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextBrowser, QComboBox, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QMainWindow, QGridLayout
)
from PyQt5.QtGui import QFont

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personalny Dashboard Danych")
        self.setGeometry(100, 100, 1000, 600)

        # Główne okno centralne
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Układ główny siatki
        grid = QGridLayout()
        central_widget.setLayout(grid)

        # Dodaj sekcje
        self.weather_section = self.weather_ui()
        self.currency_section = self.currency_ui()
        self.news_section = self.news_ui()

        # Ustawienia układu:
        # | Pogoda       | Wiadomości         |
        # | Kursy walut  | (ciąg dalszy)      |

        grid.addLayout(self.weather_section, 0, 0)  # rząd 0, kolumna 0
        grid.addLayout(self.currency_section, 1, 0)  # rząd 1, kolumna 0
        grid.addLayout(self.news_section, 0, 1, 2, 1)  # rząd 0–1, kolumna 1 (rozciąga się na 2 wiersze)

    def weather_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🌤 Sprawdź pogodę")
        title.setFont(QFont("Arial", 14))
        layout.addWidget(title)

        input_layout = QHBoxLayout()
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Wpisz miasto...")
        self.weather_button = QPushButton("Pobierz")
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.weather_button)
        layout.addLayout(input_layout)

        self.weather_output = QTextBrowser()
        layout.addWidget(self.weather_output)

        layout.addWidget(QLabel("Wykres pogody (miejsce)"))

        return layout

    def currency_ui(self):
        layout = QVBoxLayout()

        title = QLabel("💱 Kursy walut")
        title.setFont(QFont("Arial", 14))
        layout.addWidget(title)

        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["EUR", "USD", "CHF", "GBP"])
        self.currency_button = QPushButton("Pobierz kursy")

        combo_layout = QHBoxLayout()
        combo_layout.addWidget(self.currency_combo)
        combo_layout.addWidget(self.currency_button)
        layout.addLayout(combo_layout)

        self.currency_table = QTableWidget(0, 2)
        self.currency_table.setHorizontalHeaderLabels(["Waluta", "Kurs"])
        layout.addWidget(self.currency_table)

        layout.addWidget(QLabel("Wykres kursów (miejsce)"))

        return layout

    def news_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📰 Najnowsze wiadomości")
        title.setFont(QFont("Arial", 14))
        layout.addWidget(title)

        self.news_button = QPushButton("Pobierz wiadomości")
        layout.addWidget(self.news_button)

        self.news_browser = QTextBrowser()
        layout.addWidget(self.news_browser)

        return layout

# Uruchomienie aplikacji
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec_())
