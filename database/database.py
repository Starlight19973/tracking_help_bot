import psycopg2
from bot.config import settings


def create_connection():
    try:
        connection = psycopg2.connect(
            dbname=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
            host=settings.postgres_host,
            port=settings.postgres_port
        )
        print("Успешное подключение к базе данных")
        return connection
    except Exception as _ex:
        print("Ошибка при подключении к базе данных:", _ex)
        return None


def close_connection(connection):
    if connection:
        connection.close()
        print("Соединение с базой данных закрыто")



