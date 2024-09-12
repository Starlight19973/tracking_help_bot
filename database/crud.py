from database.database import create_connection, close_connection


# Создание таблицы "patients"
def create_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id SERIAL PRIMARY KEY,
                full_name VARCHAR(255) NOT NULL,
                birth_date DATE NOT NULL
            );
        ''')
        conn.commit()
        cursor.close()
        close_connection(conn)
    else:
        print("Ошибка при подключении к базе данных.")


# Добавление пациента
def add_patient(full_name: str, birth_date: str):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (full_name, birth_date) 
            VALUES (%s, %s)
        ''', (full_name, birth_date))
        conn.commit()
        cursor.close()
        close_connection(conn)
    else:
        print("Ошибка при подключении к базе данных.")


# Получение списка пациентов, пришедших сегодня
def get_today_patients():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM patients 
            WHERE birth_date = CURRENT_DATE
        ''')
        patients = cursor.fetchall()
        cursor.close()
        close_connection(conn)
        return patients
    else:
        print("Ошибка при подключении к базе данных.")
        return []

# Пример использования get_today_patients()
# patients = get_today_patients()
# for patient in patients:
#     print(patient)
