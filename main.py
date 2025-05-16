# ====================================================
#  Personal Data Dashboard
#  Wersja: 0.0.2
#  Data: 2025-05-16
# ====================================================

import sys
from gui import Ui_MainWindow
from PyQt5 import QtWidgets

import currency
import weather
import news

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # ----------- EXCHANGE SECTION -----------
    def on_show_exchange_click():
        curr_input = ui.exchangeSelectCurr.currentText()
        todays_data = currency.get_cached_live_data(curr_input)

        exchange_chart = currency.get_currency_chart(curr_input)
        if exchange_chart:
            scaled_exchange_chart = exchange_chart.scaled(ui.exchangeCurrChartExch.width(), ui.exchangeCurrChartExch.height(), aspectRatioMode=1)
            ui.exchangeCurrChartExch.setPixmap(scaled_exchange_chart)
        else:
            ui.exchangeCurrChartExch.setText("Failed to load data.")

        if todays_data:
            ui.exchangeToday.setText(f"Todays value: {todays_data} zł")
        else:
            ui.exchangeToday.setText("Failed to load data.")

        ui.exchangeCurrChartExch.update()

    # --- CACHE
    currency.save_offline_data()

    ui.exchangeShowBtn.clicked.connect(lambda: on_show_exchange_click())


    # ----------- WEATHER SECTION -----------
    def on_show_weather_click():
        city_name = ui.weatherSearchBar.text()
        weather_data = weather.get_weather(city_name)

        if weather_data:
            #Today
            ui.weatherTodayIcon.setText(weather_data['today']['weather_desc'])
            ui.weatherTodayTemp.setText(weather_data['today']['temperature'])
            ui.weatherTodayHumidity.setText(weather_data['today']['humidity'])
            ui.weatherTodayPressure.setText(weather_data['today']['humidity'])
            ui.weatherTodayVisibility.setText(weather_data['today']['visibility'])
            ui.weatherTodayWind.setText(weather_data['today']['wind'])

            today_icon = weather.get_weather_icon(weather_data['today']['icon'], weather_data['tomorrow']['icon'])
            if today_icon:
                ui.weatherTodayIcon.setPixmap(today_icon)
            else:
                ui.weatherTodayIcon.setText("Can't load icon.")
            #Tomorrow
        else:
            ui.weatherToday.setText("Failed to load data.")

    ui.weatherSearchBtn.clicked.connect(lambda: on_show_weather_click())

    # ----------- NEWS SECTION -----------
    
    MainWindow.show()
    sys.exit(app.exec_())
main()