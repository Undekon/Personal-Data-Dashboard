# ====================================================
#  Personal Data Dashboard
#  Wersja: 0.0.1
#  Data: 2025-05-15
# ====================================================

import sys
from gui import Ui_MainWindow
from PyQt5 import QtWidgets

import currency

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # ----------- EXCHANGE SECTION -----------
    def on_show_exhange_click():
        curr_input = ui.exchange_select_curr.currentText()
        todays_data = currency.get_api_data(curr_input)

        exchange_chart = currency.get_currency_chart(curr_input)
        if exchange_chart:
            scaled_exchange_chart = exchange_chart.scaled(ui.exchange_curr_chart_exch.width(), ui.exchange_curr_chart_exch.height(), aspectRatioMode=1)
            ui.exchange_curr_chart_exch.setPixmap(scaled_exchange_chart)
        else:
            ui.exchange_curr_chart_exch.setText("Failed to load data.")

        if todays_data:
            ui.exchange_today.setText(f"Todays value: {todays_data} zł")
        else:
            ui.exchange_today.setText("Failed to load data.")

        ui.exchange_curr_chart_exch.update()

    ui.exchange_show_exchange.clicked.connect(lambda: on_show_exhange_click())


    # ----------- WEATHER SECTION -----------

    # ----------- NEWS SECTION -----------
    
    MainWindow.show()
    sys.exit(app.exec_())
main()