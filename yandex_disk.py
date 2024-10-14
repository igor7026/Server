import os
import requests

from loguru import logger


class YandexDisk:
    def __init__(self, token, yandex_dir):
        self.token = token
        self.yandex_dir = yandex_dir

    def get_info_files(self, url, headers):
        """Получение списка файлов в указанной папке."""
        response= requests.get(f"{url}?path={self.yandex_dir}&fields=_embedded.items.name, _embedded.items.modified", headers=headers)
        if response.status_code == 200:
            res = response.json()
            return res['_embedded']['items']
        logger.warning(f'Список файлов с хранилища сервера недоступен. Ошибка  сервера: {response.status_code}')
        return None

    def upload_file(self, url, headers, file, local_dir, overwrite=False):
        """Загрузка файла на Яндекс.Диск."""
        print('upload_file1')
        response = requests.get(f'{url}/upload?path={self.yandex_dir}/{file}&overwrite={overwrite}', headers=headers)
        link = response.json()['href']

        with open(os.path.join(local_dir,file), 'rb') as f:
            files = {'file': f}
            res = requests.put(link, files=files)
            print('upload_file2')




    def delete_file(self, url, headers,file):
        """Удаление файла с Яндекс.Диска."""
        response = requests.delete(f'{url}?path={self.yandex_dir}/{file}', headers=headers)


