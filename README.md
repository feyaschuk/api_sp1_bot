### Описание:
Проект сервиса api_sp1_bot.

### Позволяет:
* регулярно делать запросы к базе данных, получать статус проверки работы ревьюером
* получать оповещение в Телеграмме об обновлениях статусов проверки работ
* получать оповещение в Телеграмме об ошибках в работе бота

### Используемые технологии:
* pytest==6.2.1
* python-dotenv==0.13.0
* python-telegram-bot==12.7
* requests==2.23.0
* telegram==0.0.1

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/feyaschuk/api_sp1_bot.git

```bash
cd api_sp1_bot
```bash
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv env
source env/bin/activate (Mac OS, Linux)  или source venv/Scripts/activate (Win10)
```bash
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```bash
pip install -r requirements.txt
```

В основной директории добавьте файл .env, в котором укажите свои ключи для Praktikuma и Telegramma.

PRAKTIKUM_TOKEN = 
TELEGRAM_TOKEN = 
TELEGRAM_CHAT_ID =

Запустить проект:
```bash
python3 manage.py runserver
```
