import yadisk
import pyautogui
import os
from Token import TOKEN
from datetime import date, datetime
from time import sleep


now = datetime.now()
today = str(date.today())
disk = yadisk.YaDisk(token=TOKEN)
minutes_for_screen_shot = 1
minutes_for_upload_images = 3
images_for_upload = list()


def update_time():
    global now
    global today
    now = datetime.now()
    today = str(date.today())
    print("Update time")


def create_folder():
    update_time()
    if not os.path.exists(today):
        os.mkdir(today)
        print("Create folder")


def create_screen():
    update_time()
    screen = pyautogui.screenshot()
    screen.save(f'{today}/{now.hour}-{now.minute}.png')
    print("Create screen")
    images_for_upload.append(f'{today}/{now.hour}-{now.minute}.png')


def upload_on_disk():
    if not disk.exists(f"/{today}"):
        disk.mkdir(f"/{today}")
        print("Created folder in yadisk")
    for img in os.listdir(f'{today}/'):
        if img in images_for_upload:
            disk.upload(f"{today}/" + img, f"{today}/" + img)
            images_for_upload.remove(img)
            print(f"upload {img}")


def main():
    count = 0
    create_folder()     
    while True:
        create_folder()
        print("waiting minutes_for_screen_shot")
        sleep(minutes_for_screen_shot * 60)
        create_screen()
        if count == minutes_for_upload_images:
            upload_on_disk()
            count = 0
        count += 1


if __name__ == "__main__":
    main()
