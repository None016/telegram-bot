from global_variable import *
import function as fun
import Replay_keyboard
import DB


@bi.message_handler(content_types=["text", "photo"])
async def text(sms: ai.types.Message):
    if f"{sms.chat.id}" in user_keys.keys():
        data = user_keys[f"{sms.chat.id}"]
        if data[0][0] != 4 and data[0][0] != -1:  # Исключение в виде отправления фото
            if data[0][0] == 1:     # Исключение для ввода перед полом
                user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.text   # Запись значений в словарь
                user_keys[f"{sms.chat.id}"][0][0] += 1      # прокрутка счетчика
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                          reply_markup=Replay_keyboard.sex_keyboard)
            else:
                user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.text   # Запись значений в словарь
                user_keys[f"{sms.chat.id}"][0][0] += 1      # прокрутка счетчика
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))
        elif data[0][0] == 4:       # Исключение если пришло время для фото
            user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.photo[-1].file_id
            user_keys[f"{sms.chat.id}"][0][0] = -1
            await bi.bot.send_photo(sms.chat.id, photo=sms.photo[-1].file_id,
                                    caption=f"{data[0][1]}, {data[0][2]}, {data[0][3]}")    # Вывод введенных данных
            await bi.bot.send_message(sms.chat.id, "Все правильно заполнено?",
                                      reply_markup=Replay_keyboard.binary_response)
        elif data[0][0] == -1:
            if sms.text == "Да":
                DB.add_user(sms.chat.id, sms["from"]["first_name"], data[0][2], data[0][1], data[0][4])
                del(user_keys[f"{sms.chat.id}"])
                await bi.bot.send_message(sms.chat.id, "temp mesage")


