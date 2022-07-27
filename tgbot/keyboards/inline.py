from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

report_cb = CallbackData('report', 'user_id', 'chat_id', 'message_id', 'action')
user_callback = CallbackData("confirm", "user_id")


def report_reactions_markup(user_id, chat_id, message_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Забанить и удалить сообщение', callback_data=report_cb.new(
                    user_id=user_id, chat_id=chat_id, message_id=message_id, action='ban'
                )),
            ],
            [
                InlineKeyboardButton('Забанить и удалить всё', callback_data=report_cb.new(
                    user_id=user_id, chat_id=chat_id, message_id=message_id, action='ban_delete'
                ))
            ],
            [
                InlineKeyboardButton('Удалить сообщение', callback_data=report_cb.new(
                    user_id=user_id, chat_id=chat_id, message_id=message_id, action='delete'
                )),
            ]
        ]
    )


def generate_confirm_markup(user_id: int) -> InlineKeyboardMarkup:
    confirm_user_markup = InlineKeyboardMarkup()

    confirm_user_markup.add(
        InlineKeyboardButton(
            "Я не робот 🤖",
            callback_data=user_callback.new(
                user_id=user_id,
            ),
        ),
    )
    return confirm_user_markup
