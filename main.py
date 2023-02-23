from Token import TOKEN
import yadisk
import pyautogui
import os
from datetime import date, datetime
from time import sleep

now = datetime.now()
today = str(date.today())
disk = yadisk.YaDisk(token=TOKEN)
minutes_for_screen_shot = 1
minutes_for_upload_images = 3


def get_images():
    for object in list(disk.listdir(f"/{today}/")):
        yield object["name"]


def update_time():
    global now
    global today
    now = datetime.now()
    today = str(date.today())


def create_folder():
    update_time()
    if not os.path.exists(today):
        os.mkdir(today)


def create_screen():
    update_time()
    screen = pyautogui.screenshot()
    screen.save(f'{today}/{now.hour}-{now.minute}-{now.second}.png')


def test_screenshots():
    count = 0
    create_folder()
    while count < 5:
        create_folder()
        sleep(2)
        if now.second >= now.hour * now.minute + minutes_for_upload_images:
            upload_on_disk()
        create_screen()
        count += 1


def upload_on_disk():
    if not disk.exists(f"/{today}"):
        disk.mkdir(f"/{today}")
    for img in os.listdir(f'{today}/'):
        if img not in get_images():
            disk.upload(f"{today}/" + img, f"{today}/" + img)


if __name__ == "__main__":
    test_screenshots()
