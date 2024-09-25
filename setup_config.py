import configparser

config = configparser.ConfigParser()
config.add_section('Settings')
config.set('Settings', 'token', 'y0_AgAAAAAAR7pHAADLWwAAAAESCLNkAACns3-yza9HC46dGL72sSdeeAgPUw')
config.set('Settings', 'path_to_dir_local', '/home/igor/Документы')
config.set('Settings', 'name_dir_disk_yandex', 'Документы_Игорь')
config.set('Settings', 'period', '10')
config.set('Settings', 'path_to_file_log', '/home/igor/log.log')

# Сохранение конфигурации в файл
with open('config.ini', 'w') as config_file:
    config.write(config_file)