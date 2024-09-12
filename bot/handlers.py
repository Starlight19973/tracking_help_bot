import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command
from database.crud import add_patient, get_today_patients
from validators import validate_name, validate_birth_date
from bot.states import PatientState
from database.database import create_connection, close_connection


router = Router()


# Команда /start для начала работы
@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Привет! Введите ФИО пациента для добавления.")
    await state.set_state(PatientState.waiting_for_name)


# Обработчик для ввода ФИО пациента
@router.message(StateFilter(PatientState.waiting_for_name))
async def handle_name(message: types.Message, state: FSMContext):
    full_name = message.text
    if not validate_name(full_name):
        await message.reply("Ошибка! ФИО должно содержать только буквы.")
        return

    # Сохраняем ФИО в FSM и переходим к вводу даты рождения
    await state.update_data(full_name=full_name)
    await message.reply("Введите дату рождения пациента в формате ДД.ММ.ГГГГ:")
    await state.set_state(PatientState.waiting_for_birth_date)


@router.message(StateFilter(PatientState.waiting_for_birth_date))
async def handle_birth_date(message: types.Message, state: FSMContext):
    birth_date = validate_birth_date(message.text)
    if not birth_date:
        await message.reply("Ошибка! Введите корректную дату рождения (максимальный возраст - 100 лет).")
        return

    user_data = await state.get_data()
    full_name = user_data.get("full_name")

    # Инициализируем переменную conn заранее
    conn = None

    try:
        conn = create_connection()  # Подключаемся к базе данных
        if conn:
            add_patient(conn, full_name, birth_date)  # Функция добавления пациента в БД
            await message.reply(f"Пациент {full_name} добавлен.")
        else:
            await message.reply("Ошибка подключения к базе данных.")
    except Exception as e:
        await message.reply(f"Ошибка при добавлении пациента: {e}")
        logging.error(f"Ошибка при добавлении пациента: {e}")
    finally:
        if conn:
            close_connection(conn)  # Закрываем соединение с базой данных


# Обработчик для команды /today_patients
@router.message(Command("today_patients"))
async def today_patients_handler(message: types.Message):
    try:
        patients = get_today_patients()
        if not patients:
            await message.reply("Сегодня пациентов нет.")
        else:
            response = "\n".join([f"{p[1]} - {p[2]}" for p in patients])
            await message.reply(f"Пациенты на сегодня:\n{response}")
    except Exception as e:
        await message.reply(f"Ошибка при получении списка пациентов: {e}")
        logging.error(f"Ошибка при получении списка пациентов: {e}")


# Обработчик для команды /reset для сброса состояния
@router.message(Command("reset"))
async def reset_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Состояние сброшено. Вы можете начать с добавления нового пациента.")
    await state.set_state(PatientState.waiting_for_name)
