from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import settings


bot = Bot(token=settings.bot_token)


storage = MemoryStorage()


dp = Dispatcher(storage=storage)
