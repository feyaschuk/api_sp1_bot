import logging
import os
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='rakitin_bot.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
    URL = 'http://murders.ru/'
    TIME_SLEEP = 72 * 60 * 60

except Exception as e:
    logging.error(e, exc_info=True)

try:
    bot = Bot(token=TELEGRAM_TOKEN)
except Exception as e:
    logging.error(e, exc_info=True)
old_article = []


def get_new_article(some_list):
    d = []
    for i in some_list:
        q = ''.join(filter(str.isdigit, str(i)))
        if q != '2014' and q != '':
            d.append(q)
            return max(d)


def get_new_page(current_timestamp):
    params = {'from_date': current_timestamp}
    response = requests.get(URL, params=params)
    data = BeautifulSoup(response.text)
    a = data.find(class_="index")
    some_list = a.find_all('a')
    return some_list


def send_message(message):
    try:
        return bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        logging.error(e, exc_info=True)


def main():
    try:
        current_timestamp = int(time.time())
    except ValueError:
        logging.error("Дата должна быть в формате Unix")
        time.sleep(TIME_SLEEP)
    while True:
        try:
            page = get_new_page(current_timestamp)
            article = get_new_article(page)
            if article not in old_article:
                old_article.append(article)
                send_message('На сайте murders.ru новая статья')
            time.sleep(TIME_SLEEP)

        except Exception as e:
            logging.error(f'Бот упал с ошибкой: {e}', exc_info=True)
            message = (f'Бот упал с ошибкой:{e}')
            send_message(message)


if __name__ == '__main__':
    main()
