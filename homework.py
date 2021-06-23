import logging
import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

bot = Bot(token=TELEGRAM_TOKEN)
logging.basicConfig(
    level=logging.DEBUG,
    filename='homework.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',)


def parse_homework_status(homework):

    homework_name = homework["homework_name"]
    if homework["status"] == 'rejected':
        verdict = 'К сожалению, в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, работа зачтена!'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homeworks(current_timestamp):

    headers = {
        "Authorization": "OAuth AQAAAABNMV-PAAYckSNu9UA1D0RtpcM40Vl9NoA"}
    params = {'from_date': current_timestamp}
    homework_statuses = requests.get(
        'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
        headers=headers, params=params)
    return homework_statuses.json()


def send_message(message):
    logging.info
    logging.debug
    logging.error
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())
    # current_timestamp = 1622604970  # Начальное значение timestamp
    while True:
        try:
            homeworks = get_homeworks(current_timestamp)
            for homework in homeworks["homeworks"]:
                if homework['status'] is not None:
                    message = parse_homework_status(homework)
                    send_message(message)
            time.sleep(5 * 60)  # Опрашивать раз в пять минут

        except Exception as e:
            message = (f'{e}')
            send_message(message)
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
