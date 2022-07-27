from aiogram import Dispatcher, types
from aiogram.types import Message, ContentTypes

from tgbot.keyboards.inline import report_cb
from tgbot.misc.spam import spam_checking


async def checking_message(message: Message):
    # Проверяем сообщение на СПАМ, есть ли там ссылка либо слишком длинное сообщение
    await spam_checking(message)


async def report_user_callback(call: types.CallbackQuery, callback_data: dict):
    ''' Ловим решение админа на СПАМ сообщение '''
    action = callback_data.get('action')
    message_id = callback_data.get('message_id')
    user_id = callback_data.get('user_id')
    chat_id = callback_data.get('chat_id')

    try:
        if action == 'ban':
            # Удаляем сообщение и баним юзера
            await call.bot.kick_chat_member(
                chat_id, user_id, revoke_messages=False)
            await call.bot.delete_message(chat_id, message_id)

        elif action == 'ban_delete':
            # Удаляем все сообщения и баним юзера
            await call.bot.kick_chat_member(
                chat_id, user_id, revoke_messages=True)

        elif action == 'delete':
            # Удаляем сообщение
            await call.bot.delete_message(chat_id, message_id)
    except Exception as e:
        pass
    finally:
        await call.message.delete_reply_markup()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(checking_message, state="*", content_types=ContentTypes.PHOTO | ContentTypes.TEXT)
    dp.register_callback_query_handler(report_user_callback, report_cb.filter())
