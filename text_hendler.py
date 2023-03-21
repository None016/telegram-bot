import Inline_keyboard
import global_variable
from global_variable import *
import function as fun
import Replay_keyboard
import DB


@bi.message_handler(content_types=["text", "photo"])
async def text(sms: ai.types.Message):
    if f"{sms.chat.id}" in user_keys.keys():
        data = user_keys[f"{sms.chat.id}"][0]

        if data[0] == 1:  # Исключение для ввода перед полом
            fun.add_user_key(sms, data)
            await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                      reply_markup=Replay_keyboard.sex_keyboard)

        elif data[0] == 2:
            if sms.text in global_variable.converter_for_sex.keys():
                # ^^^^^^^^^^ проверка на нажатие на кнопку для дальнейшего верного преобразования
                fun.add_user_key(sms, data)
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))
            else:
                user_keys[f"{sms.chat.id}"][0] = 2  # прокрутка счетчика
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                          reply_markup=Replay_keyboard.sex_keyboard)

        elif data[0] == 3:
            fun.add_user_key(sms, data)
            await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))

        elif data[0] == 4:       # Исключение если пришло время для фото
            if sms.photo:
                user_keys[f"{sms.chat.id}"][0][data[0]] = sms.photo[-1].file_id
                user_keys[f"{sms.chat.id}"][0][0] += 1
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))
            else:
                user_keys[f"{sms.chat.id}"][0][0] = 4
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))

        elif data[0] == 5:
            fun.add_user_key(sms, data)
            await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                      reply_markup=Replay_keyboard.search_by_gender)

        elif data[0] == 6:
            if sms.text in global_variable.converter_for_sex_poisc.keys():
                # ^^^^^^^^^^ проверка на нажатие на кнопку для дальнейшего верного преобразования
                fun.add_user_key(sms, data)
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))
            else:
                user_keys[f"{sms.chat.id}"][0][0] = 6
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                          reply_markup=Replay_keyboard.search_by_gender)

        elif data[0] == 7:
            user_keys[f"{sms.chat.id}"][0][data[0]] = sms.text  # Запись значений в словарь
            user_keys[f"{sms.chat.id}"][0][0] = -1
            await bi.bot.send_photo(sms.chat.id, photo=data[4],
                                    caption=f"{data[1]}, {data[2]}, {data[3]} \n{data[5]}")
            await bi.bot.send_message(sms.chat.id, "Все верно?",
                                      reply_markup=Replay_keyboard.binary_response)

        elif data[0] == -1:
            DB.add_user(sms.chat.id, sms["from"]["first_name"], data[2],
                        data[1], data[4], data[5], data[6], data[7], data[3])
            del (user_keys[f"{sms.chat.id}"])
            if sms.text == "Да":
                await bi.bot.send_message(sms.chat.id, "temp mesage")

    elif sms.text == "Изменить анкету" and DB.check_for_availability_user(sms.chat.id):
        await bi.bot.send_message(sms.chat.id, "Выберите изменения", reply_markup=Inline_keyboard.registration_two)

    elif f"{sms.chat.id}" in user_keys2.keys():     # Отлов для изменения анкеты
        data = user_keys2[f"{sms.chat.id}"]
        db = DB.DB("Clop.db")
        if data[0] != 3:
            fun.update_reg(sms, db, converter_for_re_registration[data[0]])
            await fun.print_inf_user(sms.chat.id)
        else:
            if sms.photo:
                db.UPDATE("user", f"photo = '{sms.photo[-1].file_id}'", f"id == {sms.chat.id}")
                await fun.print_inf_user(sms.chat.id)
            else:
                await bi.bot.send_message(sms.chat.id, "Отправте свое фото")

