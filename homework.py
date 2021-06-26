import logging
import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='homework.log',
    filemode='a',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    PRAKTIKUM_TOKEN = 'OAuth ' + os.environ['PRAKTIKUM_TOKEN']
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
    CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
    HEADERS = {"Authorization": PRAKTIKUM_TOKEN}
    URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
    TIME_SLEEP = 20 * 60
    TIME_SLEEP_EXCEPTION = 5
except Exception as e:
    logging.error(e, exc_info=True)


try:
    bot = Bot(token=TELEGRAM_TOKEN)
except Exception as e:
    logging.error(e, exc_info=True)

def parse_homework_status(homework):
    try:
        homework_name = homework.get("homework_name")
        homework_status = homework.get("status")
        if homework_name or homework_status is None:
            raise Exception('Нет названия работы или статуса проверки')
    except Exception as e:
        logging.error(e, exc_info=True)
    statuses = {
        'rejected': 'К сожалению, в работе нашлись ошибки.',
        'reviewing': 'Работа взята в ревью.',
        'approved': 'Ревьюеру всё понравилось, работа зачтена!'}
    for status, resume in statuses.items():
        if status == homework_status:
            verdict = resume
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homeworks(current_timestamp):
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(URL, headers=HEADERS, params=params)
        if homework_statuses.status_code != 200:
            homework_statuses.raise_for_status()
        else:
            raise requests.exceptions.RequestException
    except requests.exceptions.RequestException as e:
        logging.error(e, exc_info=True)
    return homework_statuses.json()


def send_message(message):
    try:
        return bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        logging.error(e, exc_info=True)


def main():
    try:
        #current_timestamp = int(time.time())
        current_timestamp = 1621604970
    except ValueError:
        logging.error("Дата должна быть в формате Unix")
        time.sleep(TIME_SLEEP)
    while True:
        try:
            homeworks = get_homeworks((current_timestamp))
            homework = homeworks.get("homeworks")[0]
            message = parse_homework_status(homework)
            send_message(message)
            time.sleep(TIME_SLEEP)

        except IndexError:
            logging.error("Нет работ на проверке")
            time.sleep(TIME_SLEEP)
        except Exception as e:
            logging.error(f'Бот упал с ошибкой: {e}', exc_info=True)
            message = (f'Бот упал с ошибкой:{e}')
            send_message(message)
            time.sleep(TIME_SLEEP_EXCEPTION)


if __name__ == '__main__':
    main()
