from Token import TOKEN
import yadisk
import pyautogui
import os
from datetime import date, datetime
from time import sleep

now = datetime.now()
today = str(date.today())
minutes = 1


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
    while count < 3:
        create_folder()
        sleep(10)
        create_screen()
        count += 1


def test_yadisk():
    y = yadisk.YaDisk(token=TOKEN)
    print(y.check_token())

    y.mkdir(f"/{today}")


def test_write_files_for_upload():
    content = os.listdir(f'{today}/')
    print(content)


if __name__ == "__main__":
    test_screenshots()
