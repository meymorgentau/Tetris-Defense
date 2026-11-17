
import asyncio
import logging
import os
import tempfile

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN
from keyboards import get_main_keyboard

from analytics import (
    get_top_players,
    get_player_statistics,
    get_achievements,
    import_csv
)


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


# Состояния загрузки файлов
class UploadStates(StatesGroup):
    waiting_for_file = State()


def format_top_players():
    """Формирует текст рейтинга игроков."""

    players = get_top_players()

    if not players:
        return (
            "🏆 Рейтинг игроков\n\n"
            "Пока здесь нет результатов.\n"
            "Загрузите CSV-файл с игровыми результатами!"
        )

    text = "🏆 Рейтинг игроков\n\n"

    for index, player in enumerate(players, start=1):
        text += (
            f"{index}. {player['player_name']}\n"
            f"   Линий уничтожено: {player['lines_cleared']}\n"
            f"   Очки: {player['score']}\n"
            f"   Игр сыграно: {player['games_played']}\n\n"
        )

    return text


def format_statistics():
    """Формирует текст общей статистики."""

    stats = get_player_statistics()

    total_score = stats.get(
        "total_score",
        stats.get("total_ score", 0)
    )

    return (
        "📊 Общая статистика\n\n"
        f"👥 Игроков: {stats['players_count']}\n"
        f"🎮 Всего игр: {stats['total_games']}\n"
        f"💥 Уничтожено линий: {stats['total_lines']}\n"
        f"⭐ Всего очков: {total_score}"
    )


def format_achievements():
    """Формирует достижения на основе лучшего результата."""

    players = get_top_players()

    if not players:
        return (
            "🎖 Достижения\n\n"
            "Пока нет игровых результатов.\n"
            "Загрузите CSV-файл, чтобы открыть достижения!"
        )

    best_player = players[0]
    lines_cleared = best_player["lines_cleared"]

    achievements = get_achievements()

    text = (
        "🎖 Достижения\n\n"
        f"🏆 Лучший игрок: {best_player['player_name']}\n"
        f"💥 Уничтожено линий: {lines_cleared}\n\n"
    )

    if not achievements:
        text += "Пока нет открытых достижений."
    else:
        for achievement in achievements:
            text += f"{achievement}\n"

    return text


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


@dp.message(Command("top"))
async def top_command(message: Message):
    await message.answer(
        format_top_players(),
        reply_markup=get_main_keyboard()
    )


@dp.message(Command("stats"))
async def stats_command(message: Message):
    await message.answer(
        format_statistics(),
        reply_markup=get_main_keyboard()
    )


@dp.message(Command("achievements"))
async def achievements_command(message: Message):
    await message.answer(
        format_achievements(),
        reply_markup=get_main_keyboard()
    )


# Начало загрузки CSV
@dp.message(Command("upload"))
async def upload_command(message: Message, state: FSMContext):
    await state.set_state(UploadStates.waiting_for_file)

    await message.answer(
        "📁 Загрузка игровых результатов\n\n"
        "Отправь мне CSV-файл с результатами игроков.\n\n"
        "Файл должен содержать столбцы:\n"
        "player_name, lines_cleared, score, games_played\n\n"
        "Для отмены отправь /cancel."
    )


@dp.callback_query(F.data == "upload")
async def upload_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UploadStates.waiting_for_file)

    await callback.message.answer(
        "📁 Загрузка игровых результатов\n\n"
        "Отправь мне CSV-файл с результатами игроков.\n\n"
        "Файл должен содержать столбцы:\n"
        "player_name, lines_cleared, score, games_played\n\n"
        "Для отмены отправь /cancel."
    )

    await callback.answer()


# Отмена загрузки
@dp.message(Command("cancel"), UploadStates.waiting_for_file)
async def cancel_upload(message: Message, state: FSMContext):
    await state.clear()

    await message.answer(
        "❌ Загрузка отменена.",
        reply_markup=get_main_keyboard()
    )


# Приём CSV-файла
@dp.message(UploadStates.waiting_for_file, F.document)
async def receive_csv(message: Message, state: FSMContext):

    document = message.document

    if not document.file_name.lower().endswith(".csv"):
        await message.answer(
            "⚠️ Неверный формат файла.\n"
            "Пожалуйста, отправь файл с расширением .csv."
        )
        return

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".csv",
            delete=False
        ) as temp_file:
            temp_path = temp_file.name

        await bot.download(document, destination=temp_path)

        imported_count = import_csv(temp_path)

        await state.clear()

        logging.info(
            "Пользователь %s загрузил %s записей.",
            message.from_user.id,
            imported_count
        )

        await message.answer(
            "✅ Импорт завершён успешно!\n\n"
            f"Добавлено записей: {imported_count}\n\n"
            "Теперь можно посмотреть обновлённый рейтинг "
            "и статистику.",
            reply_markup=get_main_keyboard()
        )

    except (ValueError, OSError, UnicodeError) as error:
        logging.warning("Ошибка импорта CSV: %s", error)

        await message.answer(
            "❌ Не удалось загрузить файл.\n\n"
            "Проверь его содержимое и наличие обязательных столбцов:\n"
            "player_name, lines_cleared, score, games_played\n\n"
            "Попробуй отправить другой файл."
        )

    except Exception:
        logging.exception("Непредвиденная ошибка при загрузке CSV.")

        await message.answer(
            "❌ Произошла ошибка при обработке файла. "
            "Попробуй ещё раз."
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# Если пользователь отправил не документ
@dp.message(UploadStates.waiting_for_file)
async def invalid_upload(message: Message):
    await message.answer(
        "⚠️ Я ожидаю CSV-файл.\n"
        "Отправь документ с расширением .csv "
        "или используй /cancel для отмены."
    )


# Кнопки главного меню
@dp.callback_query(F.data == "top")
async def top_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        format_top_players(),
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "stats")
async def stats_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        format_statistics(),
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@dp.callback_query(F.data == "achievements")
async def achievements_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        format_achievements(),
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


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
