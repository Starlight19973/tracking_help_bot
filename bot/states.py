from aiogram.fsm.state import StatesGroup, State


class PatientState(StatesGroup):
    waiting_for_name = State()          # Ожидание ввода ФИО пациента
    waiting_for_birth_date = State()    # Ожидание ввода даты рождения пациента
    patient_added = State()             # Пациент добавлен
