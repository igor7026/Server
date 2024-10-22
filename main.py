import configparser
import time
import pytz
import os
import datetime

from loguru import logger

from yandex_disk import YandexDisk
from setup_config import config_install


# Создание конфигурационного файла
config_install()

# Получение данных из файла конфигурации
config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get('Settings', 'token')
LOCAL_DIR = config.get('Settings', 'path_to_dir_local')
SERVER_DIR = config.get('Settings', 'name_dir_disk_yandex')
PATH_LOG = config.get('Settings', 'path_to_file_log')
PERIOD = int(config.get('Settings', 'period'))

#Настройка логгера
logger.remove()
logger.add(PATH_LOG)

# Сервер
URL = 'https://cloud-api.yandex.net/v1/disk/resources'
HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}


def file_date(path:str) -> datetime.datetime:
    """Функция для получения даты крайнего изменения файла и перевод в UTC."""
    ctime = os.stat(path).st_ctime
    time_change = datetime.datetime.fromtimestamp(ctime).astimezone(pytz.UTC)
    return time_change


def local_dir_dict(local_dir:str) -> dict[str, datetime.datetime]:
    """Функция для создания словаря с информацией о файлах на компьютере (имя: str; дата изменения: datetime)"""
    local_files = {}
    if os.path.isdir(local_dir):
        for file in os.listdir(local_dir):
            local_files[file] = file_date(os.path.join(local_dir, file))
        return local_files
    else:
        print(f'Папка {local_dir} не найдена')
        return None


def server_dir_dict(url: str, headers: str) -> dict[str, datetime.datetime]:
    """Функция для создания словаря с информацией о файлах на Яндекс.Диске (имя: str; дата изменения: datetime)"""
    disk_files = {}
    if a.get_info_files(url=url, headers=headers) is not None:
        for file in a.get_info_files(url=url, headers=headers):
            disk_files[file['name']] = datetime.datetime.strptime(file['modified'], '%Y-%m-%dT%H:%M:%S%z')
        return disk_files
    else:
        print(f'Ошибка получения списка файлов в облачном хранилище.')
        return None

def synchronized(local_files: dict[str,datetime.datetime], server_files: dict[str, datetime.datetime]) -> None:
    """
    Функция для синхронизации файлов на компьютере и на Яндекс.Диске
    :param local_files:
    :param server_files:
    """
    for file in server_files:
        if file not in local_files:
            a.delete_file(url=URL, headers=HEADERS, file=file)
            logger.info(f'Файл {file} удален на Яндекс.Диске')
        elif local_files[file] > server_files[file]:
            print(f'Файл {file} на компьютере был изменен после последней загрузки на Яндекс.Диск')
            a.upload_file(url=URL, headers=HEADERS, local_dir=LOCAL_DIR, file=file, overwrite=True)
            del local_files[file]
            logger.info(f'Файл {file} перезаписан на Яндекс.Диск')
        elif local_files[file] < server_files[file]:
            del local_files[file]

    if len(local_files) == 0:
        logger.info('Синхронизация завершена')
    else:
        for file in local_files:
            a.upload_file(url=URL, headers=HEADERS, local_dir=LOCAL_DIR, file=file)
            logger.info(f'Файл {file} записан на Яндекс.Диск')

        logger.info('Синхронизация завершена')


if __name__ == '__main__':


# Создание объекта для работы с Яндекс.Диском
    a = YandexDisk(token=TOKEN, yandex_dir=SERVER_DIR)

# Проверка создания словарей с информацией о файлах на компьютере и на Яндекс.Диске (имя: str; дата изменения: datetime)

    try:
        local_files = local_dir_dict(LOCAL_DIR)
        server_files = server_dir_dict(url=URL, headers=HEADERS)
    except FileNotFoundError:
        print(f'Не существует папка синхронизации {LOCAL_DIR}.\n\
Проверьте правильность ввода пути к папке синхронизации для инициализации конфигурационного файла')
        exit(1)
    except TypeError:
        print(f'Ошибка получения списка файлов в облачном хранилище   из-за неправильного токена {TOKEN}.\n\
Проверьте правильность ввода токена для инициализации конфигурационного файла')
        exit(1)
    except Exception as e:
        print(f'Ошибка получения списка файлов в облачном хранилище из-за {e}.')
        exit(1)

    logger.info(f'Начинаем работу с Яндекс.Диском. Папка синхронизации - {LOCAL_DIR}')
    synchronized(local_files=local_files, server_files=server_files)

    while True:
# Проверка наличия и соответствия файлов на Яндекс.Диске и на компьютере
        time.sleep(PERIOD)

        if local_dir_dict(LOCAL_DIR) is not None:
            local_files = local_dir_dict(LOCAL_DIR)
        else:
            continue

        if server_dir_dict(url=URL, headers=HEADERS) is not None:
            server_files = server_dir_dict(url=URL, headers=HEADERS)
        else:
            continue
        try:
            synchronized(local_files=local_files, server_files=server_files)
        except Exception as e:
            logger.error(f'Ошибка синхронизации: {e}')
            continue


        # break
    logger.info('Завершение работы с Яндекс.Диском')

# Удаление файла конфигурации
    os. remove('config.ini')
