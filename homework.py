import logging 
import os 
import time 
 
import requests 
from dotenv import load_dotenv 
from telegram import Bot 
 
load_dotenv() 
 

PRAKTIKUM_TOKEN = 'OAuth ' + os.environ['PRAKTIKUM_TOKEN'] 
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN'] 
CHAT_ID = os.environ['TELEGRAM_CHAT_ID'] 
HEADERS = {"Authorization": PRAKTIKUM_TOKEN} 
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/' 
TIME_SLEEP = 20 * 60 
TIME_SLEEP_EXCEPTION = 60 
 
bot = Bot(token=TELEGRAM_TOKEN) 
 
logging.basicConfig( 
    level=logging.DEBUG, 
    filename='homework.log', 
    filemode='a', 
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',) 
logger = logging.getLogger(__name__) 
logger.setLevel(logging.INFO) 
 
 
def parse_homework_status(homework): 

    homework_name = homework.get("homework_name") 
    homework_status = homework.get("status") 
    if homework_status == 'rejected': 
        verdict = 'К сожалению, в работе нашлись ошибки.' 

    elif homework_status == 'reviewing': 
        verdict = 'Работа взята в ревью.' 
    else: 
        verdict = 'Ревьюеру всё понравилось, работа зачтена!' 
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}' 
 
 

def get_homeworks(current_timestamp):   
    params = {'from_date': current_timestamp} 
    homework_statuses = requests.get( 
        'https://praktikum.yandex.ru/api/user_api/homework_statuses/', 
        headers=HEADERS, params=params)     
    return homework_statuses.json() 
 
 
def send_message(message): 
    return bot.send_message(chat_id=CHAT_ID, text=message) 
 
 
def main(): 
    current_timestamp = int(time.time()) 

    #current_timestamp = 1622604970  # Начальное значение timestamp 
    while True: 
        try: 
            homeworks = get_homeworks(current_timestamp) 
            for homework in homeworks["homeworks"]: 
                if homework['status'] is not None: 
                    message = parse_homework_status(homework)
                    print(message) 
                    send_message(message) 

            time.sleep(TIME_SLEEP) 
        except IndexError: 
            send_message("Нет работ на проверке") 
            time.sleep(TIME_SLEEP) 
        except Exception as e: 
            message = (f'{e}')              
            send_message(message) 
            logging.error(e, exc_info=True) 

            print(f'Бот упал с ошибкой: {e}') 
            time.sleep(TIME_SLEEP_EXCEPTION) 
 
 
if __name__ == '__main__': 
    main() 
 