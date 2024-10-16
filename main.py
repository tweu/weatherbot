import os
import datetime
import requests
import asyncio
import logging
import math
from aiogram import Bot, types,Dispatcher
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)
bot = Bot(token="1935133534:AAHkLp8ctu2dZu33bikWv_p4osN3bNx610Q")
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет,напиши название города и я пришлю сводку о погоде.")

async def main():
    await dp.start_polling(bot)

@dp.message()
async def get_weather(message: types.Message):
    city = message.text
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&lang=ru&appid=46bc8e903b2067bf5cf43e820a6d6438")
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])


        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}""\n"
        f"Погода в городе: {city}\nТемпература: {cur_temp}°C {city}\n"
        f"Влажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
        f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
        f"Хорошего дня!"
        )
    except:
        await message.reply("Проверьте название города!")


if __name__ == "__main__":
    asyncio.run(main())
