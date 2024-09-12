import re
from datetime import datetime


# Валидация ФИО
def validate_name(name: str) -> bool:
    """
    Проверяет, что ФИО состоит только из букв и пробелов.
    """
    return bool(re.match(r'^[a-zA-Zа-яА-Я\s]+$', name))


# Валидация даты рождения
def validate_birth_date(birth_date: str) -> str:
    """
    Проверяет, что дата рождения в формате ДД.ММ.ГГГГ и возраст не превышает 100 лет.
    Возвращает дату в формате ГГГГ-ММ-ДД, если всё верно.
    """
    try:
        date = datetime.strptime(birth_date, '%d.%m.%Y')
        age = (datetime.now() - date).days // 365
        if age <= 100:
            return date.strftime('%Y-%m-%d')  # Возвращаем дату в формате для БД
        return False
    except ValueError:
        return False
