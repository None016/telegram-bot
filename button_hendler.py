import global_variable as gl
import aiogram as ai
import DB
import Inline_keyboard
import function as fun


@gl.bi.callback_query_handler(text="registration")
async def registration_button(sms: ai.types.message):
    if DB.check_for_availability_user(sms.from_user.id):
        db = DB.DB("Clop.db")
        db.DELETE("user", f"id == '{sms.from_user.id}'")
    gl.app_user_keys(sms.from_user.id)
    gl.user_keys[f"{sms.from_user.id}"][0][0] = 1
    await gl.bot.send_message(sms.from_user.id, fun.input_reg(sms.from_user.id))


@gl.bi.callback_query_handler(text="forward")
async def forward(sms: ai.types.message):
    print(gl.user_keys[f"{sms.from_user.id}"])

    gl.user_keys[f"{sms.from_user.id}"][0][0] += 1
    if gl.user_keys[f"{sms.from_user.id}"][0][0] < 4:
        await gl.bot.send_message(sms.from_user.id, fun.input_reg(sms.from_user.id),
                                  reply_markup=Inline_keyboard.registration)
    else:
        await gl.bot.send_message(sms.from_user.id, fun.input_reg(sms.from_user.id),
                                  reply_markup=Inline_keyboard.reg_left)


@gl.bi.callback_query_handler(text="back")
async def back(sms: ai.types.message):
    print(gl.user_keys[f"{sms.from_user.id}"])

    gl.user_keys[f"{sms.from_user.id}"][0][0] -= 1
    if gl.user_keys[f"{sms.from_user.id}"][0][0] > 1:
        await gl.bot.send_message(sms.from_user.id, fun.input_reg(sms.from_user.id),
                                  reply_markup=Inline_keyboard.registration)
    else:
        await gl.bot.send_message(sms.from_user.id, fun.input_reg(sms.from_user.id),
                                  reply_markup=Inline_keyboard.reg_right)


@gl.bi.callback_query_handler(text="re_name")
async def back(sms: ai.types.message):
    gl.app_user_keys2(sms.from_user.id)
    gl.user_keys2[f"{sms.from_user.id}"][0] = 0
    await gl.bot.send_message(sms.from_user.id, "Введите имя")


@gl.bi.callback_query_handler(text="re_distraction")
async def back(sms: ai.types.message):
    gl.app_user_keys2(sms.from_user.id)
    gl.user_keys2[f"{sms.from_user.id}"][0] = 1
    await gl.bot.send_message(sms.from_user.id, "Введите описание")


@gl.bi.callback_query_handler(text="re_location")
async def back(sms: ai.types.message):
    gl.app_user_keys2(sms.from_user.id)
    gl.user_keys2[f"{sms.from_user.id}"][0] = 2
    await gl.bot.send_message(sms.from_user.id, "Введите местоположения")


@gl.bi.callback_query_handler(text="re_photo")
async def back(sms: ai.types.message):
    gl.app_user_keys2(sms.from_user.id)
    gl.user_keys2[f"{sms.from_user.id}"][0] = 3
    await gl.bot.send_message(sms.from_user.id, "Отправте свое фото")
