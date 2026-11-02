
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Создаёт главное интерактивное меню бота."""

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏆 Рейтинг игроков",
                    callback_data="top"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Статистика",
                    callback_data="stats"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎖 Достижения",
                    callback_data="achievements"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📁 Загрузить результаты",
                    callback_data="upload"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Помощь",
                    callback_data="help"
                )
            ]
        ]
    )

    return keyboard
