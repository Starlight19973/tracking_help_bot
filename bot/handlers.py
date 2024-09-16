import logging
from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, StateFilter, Command
from database.crud import add_patient, get_today_patients, get_patients_count_per_day
from validators import validate_name, validate_birth_date
from bot.states import PatientState
from database.database import create_connection, close_connection


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Привет! Введите ФИО пациента для добавления.")
    await state.set_state(PatientState.waiting_for_name)


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

    # Сохраняем дату рождения в FSM и переходим к вводу даты визита
    await state.update_data(birth_date=birth_date)
    await message.reply("Введите дату визита пациента в формате ДД.ММ.ГГГГ:")
    await state.set_state(PatientState.waiting_for_visit_date)


@router.message(StateFilter(PatientState.waiting_for_visit_date))
async def handle_visit_date(message: types.Message, state: FSMContext):
    visit_date = validate_birth_date(message.text)
    if not visit_date:
        await message.reply("Ошибка! Введите корректную дату визита.")
        return

    # Получаем данные из FSM
    user_data = await state.get_data()
    full_name = user_data.get("full_name")
    birth_date = user_data.get("birth_date")

    # Добавляем пациента в базу данных
    conn = None
    try:
        conn = create_connection()
        if conn:
            add_patient(full_name, birth_date, visit_date)  # Теперь добавляем пациента с датой визита
            await message.reply(f"Пациент {full_name} с датой визита {visit_date} добавлен.")
        else:
            await message.reply("Ошибка подключения к базе данных.")
    except Exception as e:
        await message.reply(f"Ошибка при добавлении пациента: {e}")
        logging.error(f"Ошибка при добавлении пациента: {e}")
    finally:
        if conn:
            close_connection(conn)

    # Сбрасываем состояние FSM после успешного добавления пациента
    await state.clear()


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


@router.message(Command("week_patients"))
async def week_patients_handler(message: types.Message):
    try:
        patients_per_day = get_patients_count_per_day()
        if not patients_per_day:
            await message.reply("На этой неделе пациентов не было.")
        else:
            response = "\n".join([f"{day.strip()}: {count}" for day, count in patients_per_day])
            await message.reply(f"Количество пациентов за каждый день недели:\n{response}")
    except Exception as e:
        await message.reply(f"Ошибка при получении количества пациентов: {e}")
        logging.error(f"Ошибка при получении количества пациентов: {e}")


@router.message(Command("reset"))
async def reset_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.reply("Добавьте нового пациента")
    await state.set_state(PatientState.waiting_for_name)
