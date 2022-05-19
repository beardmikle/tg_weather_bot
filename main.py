import requests
import datetime
from pprint import pprint
from config import open_weather_token

def get_weather(city, open_wearher_toke):

    code_to_emoji = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Ясно \U00002601",
        "Rain": "Дождь \U00002614",
        "Clouds": "Облачно \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B",
        "Fog": "Туман \U0001F32B",
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_wearher_toke}&units=metric"
                )
        data = r.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_discription = data["weather"][0]["main"]
        if weather_discription in code_to_emoji:
            wd = code_to_emoji[weather_discription]
        else:
            wd = "(За окном непонятная погода..)"

        feels = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***"
              f"\nПогода в городе: {city}"
              f"\nТемпература: {cur_weather}°C,{wd}"
              f"\nОщущается как: {feels}°C"
              f"\nВлажность: {humidity} %"
              f"\nДавление: {pressure} Па"
              f"\nВетер: {wind} м/с"
              f"\nВосход: {sunrise_time}"
              f"\nЗакат: {sunset_time}"
              f"\nПродолжительность дня: {length_of_the_day}"
              f"\nПриятного дня!")

    except Exception as ex:
        print(ex)
        print("Проверьте названия города:")

def main():
    city = input("Введите город:")
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()

