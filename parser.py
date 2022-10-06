import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from bs4 import BeautifulSoup
from time import sleep
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token="AAFzD8fLOe38DTRRj7ZglpOMkLQK0z4_SKI")
dp = Dispatcher(bot)


async def parser():
    headers = {"User-Agent":
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
               "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"}  # нужен для антибана ( из за запросов сайта )

    arr = []

    url = f"https://avi.kz/noutbuki/?lt=1&page=1=1"
    response = requests.get(url,
                                headers=headers)  # получаем запрос со страницы сайта, headers - это заголовок вашего браузера
    soup = BeautifulSoup(response.text, "lxml")  # переводит текст сайта в более удобный язык для python

    data = soup.find_all("div",
                             class_="sr-2-list-item-n")  # получаем информацию о фильме, без захода по его ссылке
    count = 0
    for notebook in data:  # новый цикл захода в каждую ссылку с ноутбуком
        count += 1
        link = notebook.find("div", class_="sr-2-list-item-n-title").find("a", href=True)['href']
        name = notebook.find("div", class_="sr-2-list-item-n-title").find("a").text  # получаем название ноутбука
        price = notebook.find("div", class_="sr-2-list-item-n-price").find("strong").text  # получаем цену товара
        finish = (f"{count}) {name} |  {price} |  {link} \n\n")
        arr.append(finish)
    return arr


@dp.message_handler()
async def echo(message: types.Message):
    x = await parser()
    arrr = ''.join(x[0:10])
    await message.answer(arrr)