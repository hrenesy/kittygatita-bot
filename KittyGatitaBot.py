import random
import time
import schedule
import requests
import asyncio
from datetime import datetime, timedelta

from telegram import Bot

TOKEN = "8668406663:AAG5tpUIGPKI1TYNlzN0q6WZFbLqZFZMnFM"
CHAT_ID = "186318437"

bot = Bot(token=TOKEN)

def get_cat_gif():
    response = requests.get(
        "https://api.thecatapi.com/v1/images/search?mime_types=gif"
    )

    data = response.json()
    return data[0]["url"]

async def send_cat():
    captions = [
        "кот прибыл",
        "срочная поставка кота",
        "кот инспектирует твою жизнь",
        "уровень стресса снижен на 3%",
        "кот одобряет это сообщение",
        "внимание: обнаружен кот",
        "кошачья поддержка активирована",
        "кот пришел проверить кукуху",
        "сервер котов отвечает нормально",
        "это обязательный кот по расписанию",
    ]

    gif = get_cat_gif()

    await bot.send_animation(
        chat_id=CHAT_ID,
        animation=gif,
        caption=random.choice(captions)
    )
def schedule_next_cat():
    now = datetime.now()

    start_hour = 9
    end_hour = 17

    current_hour = now.hour

    if current_hour >= end_hour:
        print("Кошки спят до завтра")
        return

    if current_hour < start_hour:
        next_time = now.replace(
            hour=start_hour,
            minute=random.randint(0, 59),
            second=0
        )
    else:
        minutes = random.randint(5, 60)
        next_time = now + timedelta(minutes=minutes)

        if next_time.hour >= end_hour:
            print("Рабочий день котов окончен")
            return

    delay = (next_time - now).total_seconds()

    print(f"Следующий кот в {next_time.strftime('%H:%M')}")

    schedule.clear()
    schedule.every(delay).seconds.do(send_and_reschedule)

print("Cat bot started")

while True:
    schedule.run_pending()
    time.sleep(1)