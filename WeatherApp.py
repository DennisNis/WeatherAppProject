import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFrame, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta, timezone

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter City Name:", self)
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("e.g. Kota Kinabalu")
        self.find_button = QPushButton("Find", self)
        self.temperature_label = QLabel(self)
        self.weather_image = QLabel(self)
        self.weather_description = QLabel(self)
        self.background_widget = QFrame(self)

        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon("weather assets/clear.png"))
        self.setWindowTitle("Weather App")

        #Widgets
        background_widget = QVBoxLayout(self.background_widget)
        background_widget.setContentsMargins(20, 20, 20, 20)
        background_widget.setSpacing(20)

        background_widget.addWidget(self.city_label)
        background_widget.addWidget(self.city_input)
        background_widget.addWidget(self.find_button)
        background_widget.addWidget(self.temperature_label)
        background_widget.addWidget(self.weather_image)
        background_widget.addWidget(self.weather_description)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addWidget(self.background_widget)
        self.setLayout(main_layout)


        #Alignment
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignLeft)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.weather_image.setAlignment(Qt.AlignCenter)
        self.weather_description.setAlignment(Qt.AlignCenter)

        #Shadow at the edges
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(0)
        shadow.setXOffset(6)
        shadow.setYOffset(6)  # Shadow falls slightly below the frame
        shadow.setColor(Qt.gray)
        self.background_widget.setGraphicsEffect(shadow)

        #ID for widgets, texts, and image
        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.find_button.setObjectName('find_button')
        self.temperature_label.setObjectName('temperature_label')
        self.weather_image.setObjectName('weather_image')
        self.weather_description.setObjectName('weather_description')
        self.background_widget.setObjectName('background_widget')


        self.setStyleSheet("""
        
            QFrame#background_widget{
                background-color: hsl(196, 70%, 70%);
                border-radius: 15px;
                padding-left: 15px;
                padding-right: 15px;
                border: 2px solid transparent;
                
                
            }        
            
            QLabel, QPushButton{
                font-family: calibri;  
            }
            
            QPushButton#find_button:hover{
                background-color: hsl(0, 0%, 60%);
                color: hsl(0, 0%, 17%);  
            }
            
            QLabel#city_label{
                font-family: calibri;
                font-size: 35px;
                border-radius: 7px;
                color: hsl(217, 2%, 20%);
                font-weight: bold;
            }
            
            QLineEdit#city_input{
                font-size: 30px;
                font-family: calibri;
                color: hsl(217, 2%, 25%);
                border-radius: 10px;
                font-weight: bold;
                padding-left: 15px;
                padding-right: 15px;
            }    
            
            QLineEdit#city_input::placeholder{
                 color: hsl(44, 1%, 0%);     
                 
            }         
            
            QPushButton#find_button{
                 color: hsl(0, 0%, 70%);
                 border: none;
                 border-radius: 15px;
                 padding: 5px 15px;
                 font-size: 25px; 
                 background-color: hsl(0, 0%, 80%);
                 font-weight: bold;
            }     
                              
            QLabel#temperature_label{
                 font-size: 40px;
                 font-family: calibri;
                 font-weight: bold;
                 color: hsl(217, 2%, 20%);
            }
            
            QLabel#weather_image{
                 font-size: 10px;
                   
            }
            QLabel#weather_description{
                font-size: 40px;
                font-weight: bold;
                font-family: calibri;
                color: hsl(217, 2%, 20%);
                
            }  
        """)

        self.find_button.clicked.connect(self.get_weather_button)


    def get_weather_button(self):

        api_key = "bea0a032bab53dceea0281261c8cb6b4"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"


        try:
            response = requests.get(url)
            response.raise_for_status()#raise if there are any http errors
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as httperror:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease Try Again Later.")
                case 401:
                    self.display_error("Invalid API Key.")
                case 403:
                    self.display_error("Forbidden\nAccess Denied.")
                case 404:
                    self.display_error("Invalid Input")
                case 500:
                    self.display_error("Internal Server Error\nPlease Try Again Later.")
                case 502:
                    self.display_error("Bad Gateway\nInvalid Response From The Server.")
                case 503:
                    self.display_error("Servic\nServer Is Under Maintenance.")
                case 504:
                    self.display_error("Bad Gateway\nPlease Check Your Internet Connection.")
                case _:
                    self.display_error(f"???{httperror}???")

        except requests.exceptions.ConnectionError:
            self.display_error("No Internet")

        except requests.exceptions.Timeout:
            self.display_error("Server Timeout")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects\nTry Again Later")


        except requests.exceptions.RequestException as req_error:
            self.display_error(f"{req_error}""???")


    def display_error(self, message):

        self.temperature_label.setText(message)
        self.weather_image.clear()#Clear the image
        self.weather_description.clear()#Clear the desc

    def display_weather(self, get_data):
        temperature = get_data["main"]["temp"]
        convert_to_celsius = temperature - 273.15
        description = get_data["weather"][0]["description"]
        weather_id = get_data["weather"][0]["id"]
        dayNight_cycle = get_data["timezone"]


        local_time = datetime.utcnow() + timedelta(seconds=dayNight_cycle)
        local_hour = local_time.hour

        is_night = local_hour < 6 or local_hour >= 18#Night = before 6am or after 6pm



        self.temperature_label.setText(f"{convert_to_celsius:.0F}°C")
        self.weather_image.setPixmap(QPixmap(self.get_weather_image(weather_id, is_night)))
        self.weather_description.setText(description.capitalize())

    def get_weather_image(self, weather_id, is_night):

        if 200 <= weather_id <= 232:#thunderstorm
            pixmap = QPixmap("weather assets/storm.png")
            scaled_pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return scaled_pixmap

        elif 300 <= weather_id <= 321:#drizzle
            image_path = "weather assets/night-drizzle.png" if is_night else "weather assets/drizzle.png"
            pixmap = QPixmap(image_path)
            return pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif 500 <= weather_id <= 531:#rain
            image_path = "weather assets/night rain.png" if is_night else "weather assets/raining.png"
            pixmap = QPixmap(image_path)
            return pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        elif 600 <= weather_id <= 622:#snow
            pixmap = QPixmap("weather assets/snow.png")
            scaled_pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return scaled_pixmap

        elif weather_id == 800:#clear day or night
            image_path = "weather assets/night.png" if is_night else "weather assets/clear.png"
            pixmap = QPixmap(image_path)
            return pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)


        elif 801 <= weather_id <= 804:#cloudy
            pixmap = QPixmap("weather assets/clouds.png")
            scaled_pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return scaled_pixmap

        elif weather_id == 616:#rain and snow
            pixmap = QPixmap("weather assets/sleet.png")
            scaled_pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return scaled_pixmap

        elif weather_id == 721 and 721 and 701:#foggy
            pixmap = QPixmap("weather assets/haze.png")
            scaled_pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return scaled_pixmap
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = WeatherApp()
    main.show()
    sys.exit(app.exec_())