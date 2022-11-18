import psycopg2
import configparser
import os

# Использование configparser для чтения файла config.cfg
config = configparser.ConfigParser()
configFilePath = os.path.join(os.path.dirname(__file__), 'db.cfg')
config.read(configFilePath)

# Импорт данных БД из файла config.cfg
_dbname = config.get('info', 'dbname')
_user = config.get('info', 'user')
_password = config.get('info', 'password')
_host = config.get('info', 'host')

# Подключение к БД
conn = psycopg2.connect(dbname=_dbname, user=_user, password=_password, host=_host)

# Объявление курсора
cursor = conn.cursor()
