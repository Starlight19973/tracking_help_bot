from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage  # Добавляем MemoryStorage
from bot.config import settings

# Инициализация бота
bot = Bot(token=settings.bot_token)

# Инициализация хранилища для FSM
storage = MemoryStorage()

# Инициализация диспетчера
dp = Dispatcher(storage=storage)
