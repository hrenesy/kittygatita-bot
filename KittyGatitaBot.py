import random
import time
import schedule
import requests
import asyncio
from datetime import datetime, timedelta

from telegram import Bot

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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
    schedule.clear()

    now = datetime.now()

    start_hour = 9
    end_hour = 17

    if now.hour >= end_hour:
        print("Кошки спят до завтра")
        return

    if now.hour < start_hour:
        next_time = now.replace(
            hour=start_hour,
            minute=random.randint(0, 59),
            second=0,
            microsecond=0
        )
    else:
        next_time = now + timedelta(
            minutes=random.randint(5, 60)
        )

        if next_time.hour >= end_hour:
            print("Рабочий день котов окончен")
            return

    delay = int((next_time - now).total_seconds())

    print(f"Следующий кот в {next_time.strftime('%H:%M')}")

    schedule.every(int(delay)).seconds.do(send_and_reschedule)

def send_and_reschedule():
    asyncio.run(send_cat())
    schedule_next_cat()

schedule_next_cat()

print("Cat bot started")

while True:
    schedule.run_pending()
    time.sleep(1)