import telebot
import requests
from config import token


class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.handle_start(message)

        @self.bot.message_handler(content_types=['text'])
        def send_weather(message):
            self.handle_send_weather(message)

    def handle_start(self, message):
        text = ('''Приветствую вас! Если вы хотите узнать прогноз погоды, 
то вам достаточно написать название города, и я предоставлю вам информацию о текущей температуре, 
влажности, давлении, скорости ветра и состоянии погоды.''')
        self.bot.send_message(message.chat.id, text)

    def send_message_with_buttons(self, chat_id, response):
        self.bot.send_message(chat_id, response)

    def handle_send_weather(self, message):
        city = message.text
        url = ('https://api.openweathermap.org/data/2.5/weather?q=' + city +
               '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347')
        weather_data = requests.get(url).json()

        temperature = round(weather_data['main']['temp'])
        temperature_feels = round(weather_data['main']['feels_like'])
        humidity = weather_data['main']['humidity']
        pressure = round(weather_data['main']['pressure'] * 0.750063755419211)
        wind_speed = round(weather_data['wind']['speed'])

        w_now = f'📣 Сейчас в городе {city} {temperature} °C 📣\n'
        w_now += f'Ощущается как {temperature_feels} °C\n'
        w_now += f'Влажность: {humidity}%\n'
        w_now += f'Давление: {pressure} мм рт. столба\n'
        w_now += f'Скорость ветра: {wind_speed} м/с\n'
        self.send_message_with_buttons(message.chat.id, w_now)

    def run(self):
        self.bot.polling()


bot = TelegramBot(token)
bot.run()
