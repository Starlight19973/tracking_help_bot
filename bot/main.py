import asyncio
from bot.bot_init import dp, bot
from bot.handlers import router


dp.include_router(router)


async def main():
    try:
        # Запуск поллинга бота
        await dp.start_polling(bot)
    finally:
        # Закрываем сессию бота после завершения
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())