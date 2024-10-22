import configparser
import os
from dotenv import load_dotenv

load_dotenv() # load.env file
token = os.getenv('TOKEN')



def config_install():
    config = configparser.ConfigParser()
    config.add_section('Settings')
    config.set('Settings', 'token', token)
    config.set('Settings', 'path_to_dir_local', '/home/user/Документы') # путь к директории на локальном компьютере
    config.set('Settings', 'name_dir_disk_yandex', 'temp') # путь к директории в облачном хранилище
    config.set('Settings', 'period', '10') # интервал в секундах
    config.set('Settings', 'path_to_file_log', 'log.log') # путь к файлу лога

# Сохранение конфигурации в файл
    with open('config.ini', 'w') as config_file:
        config.write(config_file)