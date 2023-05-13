import yadisk
import json
import time
import os

from time import strftime as now
from os.path import exists as file_exists
from pyautogui import screenshot as screenshot_


def create_config() -> None:
    print('https://oauth.yandex.ru/authorize?response_type=token&client_id=be491110744243898092f14d82543271')
    token = input('Token: ')
    min_for_screen_shot = int(input('minutes for screen shot: '))
    min_for_upload = int(input('minutes for upload: '))
    print('save screens on your pc?(y/n)')
    if input() == 'y':
        save_files = True
    else:
        save_files = False
    config_ = {'Token': token, 'Min_for_screen_shot': min_for_screen_shot,
               'Min_for_upload': min_for_upload, 'Save_files': save_files}
    json_config = json.dumps(config_)
    with open('config.json', 'w') as outfile:
        outfile.write(json_config)
    print('config created')


def load_config() -> dict:
    if file_exists('config.json'):
        with open('config.json') as json_file:
            config = json.load(json_file)
        print('config loaded')
    else:
        print('config not exist, creating...')
        create_config()
        return load_config()
    return config


def screenshot(save_files: bool) -> None:
    screen = screenshot_()
    screen.save(f'{now("%d.%m.%Y")}/{now("%H.%M")}.png')
    if save_files:
        screen.save(f'{now("%d.%m.%Y")}_archive/{now("%H.%M")}.png')
    print(f'Screenshot! - {now("%H.%M")}.png')


def create_folder_if_not_exist(save_files: bool) -> None:
    if not file_exists(f'{now("%d.%m.%Y")}'):
        os.mkdir(now('%d.%m.%Y'))
        print('Create folder')
    if save_files:
        if not file_exists(f'{now("%d.%m.%Y")}_archive'):
            os.mkdir(f'{now("%d.%m.%Y")}_archive')
            print('Create archive folder')


def upload_on_disk(disk: yadisk.YaDisk) -> None:
    if not disk.exists(f'{now("%d.%m.%Y")}'):
        disk.mkdir(f'{now("%d.%m.%Y")}')
        print(f'yandex folder {now("%d.%m.%Y")} created')
    for img in os.listdir(f'{now("%d.%m.%Y")}'):
        disk.upload(f'{now("%d.%m.%Y")}/{img}', f'{now("%d.%m.%Y")}/{img}')
        os.remove(f'{now("%d.%m.%Y")}/{img}')
    print('upload on disk successful')


def main() -> None:
    config = load_config()
    disk = yadisk.YaDisk(token=config['Token'])
    if not disk.check_token():
        exit("Problem token")
    create_folder_if_not_exist(config['Save_files'])
    while True:
        for minute_upload in range(config['Min_for_upload']):
            create_folder_if_not_exist(config['Save_files'])
            print("Waiting minutes for screen shot")
            time.sleep(config['Min_for_screen_shot'] * 60)
            screenshot(config['Save_files'])
        upload_on_disk(disk)


if __name__ == '__main__':
    print('ScreenShooter on python v2 by pasha coder')
    main()
