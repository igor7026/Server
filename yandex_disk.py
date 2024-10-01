import os
import requests



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
        return

    def upload_file(self, url, headers, file, local_dir, overwrite=False):
        """Загрузка файла на Яндекс.Диск."""
        response = requests.get(f'{url}/upload?path={self.yandex_dir}/{file}&overwrite={overwrite}', headers=headers)
        if response.status_code == 200:
            link = response.json()['href']
            print(link)
            with open(os.path.join(local_dir,file), 'rb') as f:
                files = {'file': f}
                res = requests.put(link, files=files)
                if res.status_code == 201:
                    return f"Файл {file} успешно загружен на Яндекс.Диск"
                else:
                    return f'Ошибка загрузки файла на Яндекс.Диск {res.status_code}'

        else:
            return f'Ошибка загрузки файла на Яндекс.Диск {response.status_code}'

    def delete_file(self, url, headers,file):
        """Удаление файла с Яндекс.Диска."""
        response = requests.delete(f'{url}?path={self.yandex_dir}/{file}', headers=headers)
        if response.status_code == 204:
            return f"Файл {file} успешно удален с Яндекс.Диска"
        else:
            return f'Ошибка удаления файла с Яндекс.Диска {response.status_code}'