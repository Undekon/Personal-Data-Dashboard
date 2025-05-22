# ====================================================
#  Personal Data Dashboard
#  Wersja: 0.0.4
#  Data: 2025-05-22
# ====================================================

import sys
from gui import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
import requests
from io import BytesIO


import currency
import weather
import news

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.newsArticleFrameTemplate.hide()

    # ----------- EXCHANGE SECTION -----------
    def on_show_exchange_click(default_curr=None):
        curr_input = default_curr or ui.exchangeSelectCurr.currentText()
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
    def on_show_weather_click(default_city = None):
        city_name = default_city or ui.weatherSearchBar.text()
        city_name.capitalize()
        weather_data = weather.get_weather(city_name)

        if weather_data:
            #Today
            ui.weatherTodayIcon.setText(weather_data['today']['weather_desc'])
            ui.weatherTodayTemp.setText(f"{weather_data['today']['temperature']}°C")
            ui.weatherTodayHumidity.setText(f"{weather_data['today']['humidity']} %")
            ui.weatherTodayPressure.setText(f"{weather_data['today']['pressure']} hPa")
            ui.weatherTodayVisibility.setText(f"{weather_data['today']['visibility']} km")
            ui.weatherTodayWind.setText(f"{weather_data['today']['wind']} km/h")
            ui.weatherCityName.setText(city_name)

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
    def create_article(title, link, img, source):
        # Clone template settings
        article_frame = QtWidgets.QFrame()
        article_frame.setMinimumSize(ui.newsArticleFrameTemplate.size())
        article_frame.setMaximumSize(ui.newsArticleFrameTemplate.maximumSize())
        article_frame.setStyleSheet(ui.newsArticleFrameTemplate.styleSheet())

        #copy template content
        article_image = QtWidgets.QLabel(article_frame)
        article_image.setGeometry(QtCore.QRect(10, 10, 100, 100))
        article_image.setAlignment(QtCore.Qt.AlignCenter)
        article_image.setStyleSheet(ui.newsArticleImage.styleSheet())

        #load image
        if not img or img in ['None', '', None, 'null' , 'none']:
            article_image.setText("No image.")
        else:
            try:
                response = requests.get(img)
                img_data = BytesIO(response.content)
                pixmap = QtGui.QPixmap()
                pixmap.loadFromData(img_data.read())
                pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                article_image.setPixmap(pixmap)
            except Exception as e:
                article_image.setText("No image.")

        article_title = QtWidgets.QLabel(article_frame)
        article_title.setGeometry(QtCore.QRect(120, 10, 341, 51))
        article_title.setText(f'<a href="{link}" style="text-decoration: none; color: white; font: 10pt Arial;">{title}</a>')
        article_title.setOpenExternalLinks(True)
        article_title.setWordWrap(True)
        article_title.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        article_source = QtWidgets.QLabel(article_frame)
        article_source.setGeometry(ui.newsArticleSource.geometry())
        article_source.setText(f"Source: {source}")
        article_source.setStyleSheet(ui.newsArticleSource.styleSheet())

        #add new article
        scroll_layout = ui.newsScrollAreaWidgetContents.layout()
        if not scroll_layout:
            scroll_layout = QtWidgets.QVBoxLayout(ui.newsScrollAreaWidgetContents)
            ui.newsScrollAreaWidgetContents.setLayout(scroll_layout)
        scroll_layout.addWidget(article_frame)


    def on_submit_news_click(default_category = None):
        category = default_category or ui.newsCategoryInput.currentText().lower()
        news_list = news.get_news(category)

        #clear all news
        for article in ui.newsScrollAreaWidgetContents.children():
            if isinstance(article, QtWidgets.QFrame) and article != ui.newsArticleFrameTemplate:
                article.deleteLater()

        if news_list:
            for article in news_list[:50]:
                title = article['title']
                link = article['link']
                img = article['image_url']
                source = article['source_url']

                create_article(title, link, img, source)
                print(f"{title}\n{link}\n{img}\n{source}\n\n")
        else:
            error_label = QtWidgets.QLabel("Can't load news.")
            error_label.setStyleSheet("color: white; font-size: 14p;")
            ui.newsScrollAreaWidgetContents.layout().addWidget(error_label)

    ui.newsSubmitBtn.clicked.connect(lambda: on_submit_news_click())
    

    #  ----------- Default settings on program start  ----------- 
    on_show_weather_click("Warsaw")
    on_show_exchange_click("EUR")
    on_submit_news_click("top")

    MainWindow.show()
    sys.exit(app.exec_())
main()