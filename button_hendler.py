import global_variable as gl
import aiogram as ai
import DB
import Inline_keyboard


@gl.bi.callback_query_handler(text="registration")
async def registration_button(sms: ai.types.message):
    gl.app_user_keys(sms.from_user.id)
    gl.user_keys[f"{sms.from_user.id}"][0][0] = 1
    await gl.bot.send_message(sms.from_user.id, "имя", reply_markup=Inline_keyboard.reg_right)


@gl.bi.callback_query_handler(text="forward")
async def forward(sms: ai.types.message):
    print(gl.user_keys[f"{sms.from_user.id}"])
    gl.user_keys[f"{sms.from_user.id}"][0][0] += 1
    await gl.bot.send_message(sms.from_user.id, "Temp mesage", reply_markup=Inline_keyboard.registration)
    # ^^^^^^^^^^ Временно добавлено клавиатура и сообщение в дальнейшем исправить


@gl.bi.callback_query_handler(text="back")
async def back(sms: ai.types.message):
    print(gl.user_keys[f"{sms.from_user.id}"])
    gl.user_keys[f"{sms.from_user.id}"][0][0] -= 1
    await gl.bot.send_message(sms.from_user.id, "Temp mesage", reply_markup=Inline_keyboard.registration)
    # ^^^^^^^^^^ Временно добавлено клавиатура и сообщение в дальнейшем исправить


@gl.bi.callback_query_handler(text="input")
async def back(sms: ai.types.message):
    print(gl.user_keys[f"{sms.from_user.id}"])
    gl.user_keys[f"{sms.from_user.id}"][0][5] = True
    await gl.bot.send_message(sms.from_user.id, "Temp mesage")
    # ^^^^^^^^^^ Временно добавлено клавиатура и сообщение в дальнейшем исправить



