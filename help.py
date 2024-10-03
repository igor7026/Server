from loguru import logger
import sys

#logger.add(sys.stderr, format="{time} {level} {message}", filter="sub.module", level="INFO")
logger.debug("Красивое и простое ведение журнала!")



# Настройка логгера
logger_main = logging.getLogger(__name__)
logger_main.setLevel(logging.INFO)
# настройка обработчика и форматировщика
main_handler = logging.FileHandler(PATH_LOG, mode='w')
main_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# добавление форматировщика к обработчику
main_handler.setFormatter(main_formatter)
# добавление обработчика к логгеру
logger_main.addHandler(main_handler)



logger_server = logging.getLogger(__name__)
logger_server.setLevel(logging.WARNING)
# настройка обработчика и форматировщика
server_handler = logging.FileHandler('log.log', mode='w')
server_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
# добавление форматировщика к обработчику
server_handler.setFormatter(server_formatter)
# добавление обработчика к логгеру
logger_server.addHandler(server_handler)


TOKEN = 'y0_AgAAAAAAR7pHAADLWwAAAAESCLNkAACns3-yza9HC46dGL72sSdeeAgPUw'