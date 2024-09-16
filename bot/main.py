import asyncio
import logging
from bot.bot_init import dp, bot
from bot.handlers import router
from database.crud import create_table

# Включаем обработчики из router
dp.include_router(router)


async def on_startup():
    """
    Функция, которая выполняется при старте бота.
    Здесь создаются таблицы в базе данных.
    """
    logging.info("Создание таблиц в базе данных...")
    create_table()  # Создаем таблицу "patients" перед запуском бота


async def main():
    try:
        # Выполняем стартовые действия перед поллингом
        await on_startup()

        # Запуск поллинга бота
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию бота после завершения
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())