import aiogram as ai
import Inline_keyboard
import Replay_keyboard
import DB
from global_variable import *
import button_hendler


@bi.message_handler(commands="start")
async def com_start(sms: ai.types.message):
    if not DB.check_for_availability_user(sms.chat.id):
        await bot.send_message(sms.chat.id, "Привет для использования бота необходимо пройти регистрацию",
                               reply_markup=Inline_keyboard.start)
    else: await bot.send_message(sms.chat.id, "Выбери действие", reply_markup=Replay_keyboard.menu)

import text_hendler


if __name__ == "__main__":
    ai.executor.start_polling(bi, fast=True, skip_updates=True)