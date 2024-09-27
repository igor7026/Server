import configparser
import requests
import os
import datetime
import logging


config = configparser.ConfigParser()
config.read('config.ini')

# Получение данных из файла конфигурации
TOKEN= config.get('Settings', 'token')
local_dir = config.get('Settings', 'path_to_dir_local')
yandex_dir = config.get('Settings', 'name_dir_disk_yandex')
path_log = config.get('Settings', 'path_to_file_log')


logging.basicConfig(level='INFO', format='%(asctime)s - %(levelname)s - %(message)s', filename=path_log)
logger = logging.getLogger(__name__)



URL = 'https://cloud-api.yandex.net/v1/disk/resources'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {TOKEN}'}

class YandexDisk:
    def __init__(self, token, yandex_dir, headers):
        self.token = token
        self.yandex_dir = yandex_dir
        self.headers = headers

    def get_info_files(self):
        """Получение списка файлов в указанной папке."""
        response= requests.get(f"{URL}?path={self.yandex_dir}&fields=_embedded.items.name, _embedded.items.modified", headers=self.headers)
        if response.status_code == 200:
            res = response.json()
            logger.info(f'Получение списка файлов в облачном хранилище в папке {self.yandex_dir}')
            print(res)
            return res['_embedded']['items']
        return

    def upload_file(self, file, overwrite=False):
        """Загрузка файла на Яндекс.Диск."""
        response = requests.get(f'{URL}/upload?path={self.yandex_dir}/{file}&overwrite={overwrite}', headers=headers)
        if response.status_code == 200:
            link = response.json()['href']
            print(link)
            with open(os.path.join(local_dir,file), 'rb') as f:
                files = {'file': f}
                res = requests.put(link, files=files)
                if res.status_code == 201:
                    logger.info(f"Файл {file} успешно загружен на Яндекс.Диск")
                else:
                    return f'Ошибка загрузки файла на Яндекс.Диск {res.status_code}'

        else:
            return f'Ошибка загрузки файла на Яндекс.Диск {response.status_code}'

    def delete_file(self, file):
        """Удаление файла с Яндекс.Диска."""
        response = requests.delete(f'{URL}?path={self.yandex_dir}/{file}', headers=headers)
        if response.status_code == 204:
            logger.info(f"Файл {file} успешно удален с Яндекс.Диска")
        else:
            return f'Ошибка удаления файла с Яндекс.Диска {response.status_code}'



def file_date(path:str) -> datetime.datetime:
    """Функция для получения даты крайнего изменения файла."""
    ctime = os.stat(path).st_ctime
    time_change_file = datetime.datetime.fromtimestamp(ctime)
    return time_change_file


if __name__ == '__main__':

    a = YandexDisk(token=TOKEN, yandex_dir=yandex_dir, headers=headers)


 # Создание словаря с информацией о файлах на компьютере (имя: str; дата изменения: datetime)
    local_files = {}
    for file in os.listdir(local_dir):
        local_files[file] = file_date(os.path.join(local_dir, file))
    print('Local', local_files)


# Создание словаря с информацией о файлах на Яндекс.Диске (имя: str; дата изменения: datetime)
    disk_files = {}
    for file in a.get_info_files():
        disk_files[file['name']] = datetime.datetime.strptime(file['modified'][:-6], '%Y-%m-%dT%H:%M:%S')
    print('Disk', disk_files)

    for file in disk_files:
        if file not in local_files:
            print(f'Файл {file} отсутствует на компьютере')
            a.delete_file(file=file)
        elif local_files[file] > disk_files[file]:
                print(f'Файл {file} на компьютере был изменен после последнего загрузки на Яндекс.Диск')
                a.upload_file(file=file, overwrite=True)
                del local_files[file]


    if len(local_files) == 0:
        print('Все файлы на компьютере были загружены на Яндекс.Диск')
    else:
        for file in local_files:
            print(f'Файл {file} отсутствует на Яндекс.Диске')
            a.upload_file(file=file)





