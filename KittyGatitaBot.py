import os
import random
import time
import schedule
import requests
from datetime import datetime, timedelta


TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def get_cat_gif():
    response = requests.get(
        "https://api.thecatapi.com/v1/images/search?mime_types=gif"
    )

    data = response.json()
    return data[0]["url"]

def send_cat():
    captions = [
        "кот прибыл",
        "срочная поставка кота",
        "кот инспектирует твою жизнь",
        "уровень стресса снижен на 3%",
        "кот одобряет это сообщение",
        "внимание: обнаружен кот",
    ]

    gif = get_cat_gif()

    url = f"https://api.telegram.org/bot{TOKEN}/sendAnimation"

    data = {
        "chat_id": CHAT_ID,
        "animation": gif,
        "caption": random.choice(captions)
    }

    response = requests.post(url, data=data)

    print(response.text)
def schedule_next_cat():
    schedule.clear()

    now = datetime.now() + timedelta(hours=1)

    start_hour = 9
    end_hour = 20

    if now.hour >= end_hour:
        next_time = (now + timedelta(days=1)).replace(
            hour=start_hour,
            minute=random.randint(0, 59),
            second=0,
            microsecond=0
        )

    elif now.hour < start_hour:
        next_time = now.replace(
            hour=start_hour,
            minute=random.randint(0, 59),
            second=0,
            microsecond=0
        )

    else:
        next_time = now + timedelta(
            minutes=random.randint(20, 50)
        )

        if next_time.hour >= end_hour:
            next_time = (now + timedelta(days=1)).replace(
                hour=start_hour,
                minute=random.randint(0, 59),
                second=0,
                microsecond=0
            )

    delay = int((next_time - now).total_seconds())

    print(f"Следующий кот в {next_time.strftime('%Y-%m-%d %H:%M')}")

    schedule.every(delay).seconds.do(send_and_reschedule)

def send_and_reschedule():
    try:
        send_cat()
    except Exception as e:
        print(e)

    schedule_next_cat()

print("Cat bot started")

schedule_next_cat()

while True:
    schedule.run_pending()
    time.sleep(1)
