import psycopg2
from psycopg2 import sql
from bot.config import settings


# Функция для создания подключения к базе данных
def create_connection():
    try:
        conn = psycopg2.connect(settings.db_url, client_encoding='UTF8')
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None


# Функция для закрытия подключения
def close_connection(conn):
    if conn:
        conn.close()
