from aiogram.fsm.state import StatesGroup, State


class PatientState(StatesGroup):
    waiting_for_name = State()
    waiting_for_birth_date = State()
    waiting_for_visit_date = State()
    patient_added = State()
