from database.database import create_connection, close_connection
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO)


def create_table():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS patients (
                        patient_id SERIAL PRIMARY KEY,
                        full_name VARCHAR(255) NOT NULL,
                        birth_date DATE NOT NULL
                    )
                ''')
                connection.commit()
                logging.info("Таблица 'patients' успешно создана.")
        except Exception as e:
            logging.error(f"Ошибка при создании таблицы: {e}")
        finally:
            close_connection(connection)
    else:
        logging.error("Не удалось подключиться к базе данных для создания таблицы.")


def add_patient(full_name: str, birth_date: str, visit_date: str):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO patients (full_name, birth_date, visit_date) 
                    VALUES (%s, %s, %s)
                ''', (full_name, birth_date, visit_date))
                connection.commit()
                logging.info(f"Пациент {full_name} добавлен с датой визита {visit_date}.")
        except Exception as e:
            logging.error(f"Ошибка при добавлении пациента: {e}")
        finally:
            close_connection(connection)
    else:
        logging.error("Не удалось подключиться к базе данных для добавления пациента.")


def get_today_patients():
    connection = create_connection()
    if connection:
        try:
            today = datetime.now().date()  # Получаем текущую дату

            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT * FROM patients 
                    WHERE visit_date = %s
                ''', (today,))
                patients = cursor.fetchall()
                logging.info(f"Найдено {len(patients)} пациентов, пришедших сегодня.")
                return patients
        except Exception as e:
            logging.error(f"Ошибка при получении списка пациентов: {e}")
            return []
        finally:
            close_connection(connection)
    else:
        logging.error("Не удалось подключиться к базе данных для получения списка пациентов.")
        return []


def get_patients_count_per_day():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                # Группируем пациентов по дням недели и считаем их количество
                cursor.execute('''
                    SELECT TO_CHAR(visit_date, 'Day') AS day_of_week, COUNT(*) 
                    FROM patients
                    WHERE visit_date >= CURRENT_DATE - INTERVAL '7 days'
                    GROUP BY day_of_week
                    ORDER BY day_of_week;
                ''')
                patients_per_day = cursor.fetchall()
                logging.info(f"Количество пациентов за каждый день недели: {patients_per_day}")
                return patients_per_day
        except Exception as e:
            logging.error(f"Ошибка при получении количества пациентов за каждый день недели: {e}")
            return []
        finally:
            close_connection(connection)
    else:
        logging.error("Не удалось подключиться к базе данных для получения количества пациентов.")
        return []



