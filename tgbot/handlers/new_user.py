from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.types import ContentTypes

from tgbot.keyboards.inline import generate_confirm_markup, user_callback
from tgbot.misc.permissions import set_new_user_permissions, set_new_user_approved_permissions


async def checking_new_user(message: types.Message):
    # Выводим юзеру приветствие с кнопкой для подтверждения
    bot_user = await message.bot.me
    if message.from_user.id == bot_user.id:
        return False
    for user in message.new_chat_members:
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user.id,
            permissions=set_new_user_permissions(),
        )
    for user in message.new_chat_members:
        await message.answer(f'Привет, {user.get_mention()}.\n'
                             f'Подтверди, что ты не бот, нажатием на кнопку ниже.',
                             reply_markup=generate_confirm_markup(user.id))


async def user_is_not_robot(call: types.CallbackQuery, callback_data: dict):
    '''Ответ на нажатие кнопки юзером'''
    user_id = int(callback_data.get("user_id"))
    chat_id = int(call.message.chat.id)

    # Если кнопку нажал не новый юзер
    if call.from_user.id != user_id:
        return await call.answer()

    # with suppress(MessageToDeleteNotFound):
    #     await call.message.delete()
    #     text = str(
    #         f"Вопросов больше нет, {call.from_user.get_mention(as_html=True)}, проходите\n"
    #     )
    #     await call.bot.send_message(chat_id, text)

    new_permissions = set_new_user_approved_permissions()
    with suppress(Exception):
        await call.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=new_permissions,
        )
    await call.message.delete()


def register_new_user(dp: Dispatcher):
    dp.register_message_handler(checking_new_user, content_types=ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_callback_query_handler(user_is_not_robot, user_callback.filter())
