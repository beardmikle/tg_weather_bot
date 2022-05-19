import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

# class color:
#    PURPLE = '\033[95m'
#    CYAN = '\033[96m'
#    DARKCYAN = '\033[36m'
#    BLUE = '\033[94m'
#    GREEN = '\033[92m'
#    YELLOW = '\033[93m'
#    RED = '\033[91m'
#    BOLD = '\033[1m'
#    UNDERLINE = '\033[4m'
#    END = '\033[0m'

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(f"Привет! Напиши название города\n"
                        f"на английском \n"
                        f"и я покажу тебе погоду!")

@dp.message_handler()
async def get_weather(message: types.Message):

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
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
                )
        data = r.json()

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

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***"f"\n"
                            f"Погода в городе: {city}"
              f"\nТемпература: {cur_weather}°C,{wd}"
              f"\nОщущается как: {feels}°C"
              f"\nВлажность: {humidity} %"
              f"\nДавление: {pressure} Па"
              f"\nВетер: {wind} м/с"
              f"\nВосход: {sunrise_time}"
              f"\nЗакат: {sunset_time}"
              f"\nПродолжительность дня: {length_of_the_day}"
              f"\n***Приятного дня!***")

    except:
        await message.reply("Проверьте название города")

if __name__ == '__main__':
    executor.start_polling(dp)
