
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from config import BOT_TOKEN
from keyboards import get_main_keyboard


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("bot_flight.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "🛡️ Добро пожаловать в «Оборонный Штаб»!\n\n"
        "Я — аналитический бот игры «Тетрис-Защита».\n"
        "Здесь ты сможешь просматривать игровую статистику, "
        "узнавать достижения и сравнивать результаты игроков.\n\n"
        "Выбери нужный раздел в меню ниже:",
        reply_markup=get_main_keyboard()
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "📋 Список доступных команд:\n\n"
        "/start — запуск бота\n"
        "/help — справка\n"
        "/top — рейтинг игроков\n"
        "/stats — игровая статистика\n"
        "/achievements — достижения\n"
        "/upload — загрузка результатов",
        reply_markup=get_main_keyboard()
    )


@dp.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "📋 Список доступных команд:\n\n"
        "/start — запуск бота\n"
        "/help — справка\n"
        "/top — рейтинг игроков\n"
        "/stats — игровая статистика\n"
        "/achievements — достижения\n"
        "/upload — загрузка результатов",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


async def main():
    logging.info("Бот «Оборонный Штаб» запускается...")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
