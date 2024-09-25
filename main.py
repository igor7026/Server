import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Получение данных из файла конфигурации
token= config.get('Settings', 'token')
password = config.get('Settings', 'period')

print(f'Token: {token}')
print(f'Period: {password}')