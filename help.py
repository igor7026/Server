import configparser
import requests
import os
import datetime
import logging

from dateutil import tz

filename = input("Введите путь к файлу: ")
if os.path.exists(filename):
    print("Указанный файл существует")
else:
    print("Файл не существует")