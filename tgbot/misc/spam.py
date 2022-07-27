import asyncio
import re

from aiogram import types
from aiogram.utils.markdown import hlink

from tgbot.keyboards.inline import report_reactions_markup


async def spam_checking(message: types.Message):
    url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)'

    if message.content_type == 'photo':
        #Проверка на тот случай, если отправлено сообщение с изображением
        message_text = message.caption
    else:
        message_text = message.text

    if re.match(url_regex, message_text) or \
            len(message_text) >= 1 and message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP):

        await message.reply('Ваше сообщение похоже на спам или рекламу.\n'
                            'Администратор группы уведомлен')
        chat_admins = await message.bot.get_chat_administrators(message.chat.id)
        for admin in chat_admins:
            admin_id = admin.user.id
            text = f"Подозрительное сообщение от {message.from_user.get_mention()}\n{hlink('сообщение', message.url)}"
            if not admin.user.is_bot:
                await message.bot.send_message(
                    chat_id=admin_id,
                    text=text,
                    reply_markup=report_reactions_markup(
                        message.from_user.id,
                        message.chat.id,
                        message.message_id)
                )
                await asyncio.sleep(0.05)
                return True
