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
        "https://api.thecatapi.com/v1/images/search?mime_types=gif",
        timeout=20
    )
    response.raise_for_status()
    return response.json()[0]["url"]


def send_cat():
    gif = get_cat_gif()
    url = f"https://api.telegram.org/bot{TOKEN}/sendAnimation"

    response = requests.post(
        url,
        data={"chat_id": CHAT_ID, "animation": gif},
        timeout=30
    )
    response.raise_for_status()
    print("Кот отправлен!", flush=True)


def schedule_next_cat():
    schedule.clear()

    now = datetime.now() + timedelta(hours=1)
    start_hour = 9
    end_hour = 22

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
        next_time = now + timedelta(minutes=random.randint(105, 135))

        if next_time.hour >= end_hour:
            next_time = (now + timedelta(days=1)).replace(
                hour=start_hour,
                minute=random.randint(0, 59),
                second=0,
                microsecond=0
            )

    delay = max(1, int((next_time - now).total_seconds()))

    print(
        f"Следующий кот в {next_time.strftime('%Y-%m-%d %H:%M')}",
        flush=True
    )

    schedule.every(delay).seconds.do(send_and_reschedule)


def send_and_reschedule():
    try:
        send_cat()
    except Exception as e:
        print(f"Ошибка отправки кота: {e}", flush=True)
    finally:
        schedule_next_cat()


print("Cat bot started", flush=True)
schedule_next_cat()

while True:
    schedule.run_pending()
    time.sleep(1)
