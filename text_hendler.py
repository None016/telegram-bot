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
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                          reply_markup=Replay_keyboard.skip_description)
            else:
                user_keys[f"{sms.chat.id}"][0][0] = 4
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))

        elif data[0] == 5:
            if sms.text == "Оставить описание пустым":
                user_keys[f"{sms.chat.id}"][0][data[0]] = " "  # Запись значений в словарь
                user_keys[f"{sms.chat.id}"][0][0] += 1  # прокрутка счетчика
            else:
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
                await bot.send_message(sms.chat.id, "Выбери действие", reply_markup=Replay_keyboard.menu)

    elif sms.text == "Изменить анкету" and DB.check_for_availability_user(sms.chat.id):
        await bi.bot.send_message(sms.chat.id, "Выберите изменения", reply_markup=Inline_keyboard.registration_two)
    elif sms.text == "Моя анкета" and DB.check_for_availability_user(sms.chat.id):
        await fun.print_inf_user(sms.chat.id, sms)   # Выводит информацию о пользователе
        await bot.send_message(sms.chat.id, "Выбери действие", reply_markup=Replay_keyboard.menu)
    elif (sms.text == "🚀Лента🚀") and DB.check_for_availability_user(sms.chat.id):
        user_keys3[f"{sms.chat.id}"] = [[], []]  # 1 для показа 2 для прошедших показ
        await bi.bot.send_message(sms.chat.id, "Хорошего просмотра", reply_markup=Replay_keyboard.assessment)
        await fun.recommendations(sms)
    elif (sms.text == "💤") and DB.check_for_availability_user(sms.chat.id) and f"{sms.chat.id}" in user_keys3.keys():  # уход в спящий режим
        del(user_keys3[f"{sms.chat.id}"])
        await bi.bot.send_message(sms.chat.id, "Подождем пока тебя кто то лайкнит", reply_markup=Replay_keyboard.menu)
    elif (sms.text == "❤️") and f"{sms.chat.id}" in user_keys3.keys():
        await fun.like(sms)
        if f"{sms.chat.id}" in user_keys3.keys():
            await fun.recommendations(sms)
    if sms.text == "👎" and f"{sms.chat.id}" in user_keys3.keys():
        db = DB.DB("Clop.db")
        data4 = db.SELECT("like_user", f"id_user2 == {sms.chat.id}")
        if data4:
            for i in data4:
                if i[0] == user_keys3[f"{sms.chat.id}"][1][0]:
                    db.DELETE("like_user",
                              f"id_user2 == {sms.chat.id} and id_user1 == {user_keys3[f'{sms.chat.id}'][1][0]}")
        await fun.recommendations(sms)
    elif f"{sms.chat.id}" in user_keys2.keys():     # Отлов для изменения анкеты
        data = user_keys2[f"{sms.chat.id}"]
        db = DB.DB("Clop.db")
        if data[0] != 3 and data[0] != 2:
            fun.update_reg(sms, db, converter_for_re_registration[data[0]])
            await fun.print_inf_user(sms.chat.id, sms)  # Выводит информацию о пользователе
        elif data[0] == 2:
            db.UPDATE("user", f"location = '{sms.text}'", f"id == {sms.chat.id}")
            db.UPDATE("user", f"location_no = '{sms.text.lower()}'", f"id == {sms.chat.id}")
            del (user_keys2[f"{sms.chat.id}"])
            await fun.print_inf_user(sms.chat.id, sms)  # Выводит информацию о пользователе
            await bot.send_message(sms.chat.id, "Выбери действие", reply_markup=Replay_keyboard.menu)
        else:
            if sms.content_type == "photo":
                db.UPDATE("user", f"photo = '{sms.photo[-1].file_id}'", f"id == {sms.chat.id}")
                del(user_keys2[f"{sms.chat.id}"])
                await fun.print_inf_user(sms.chat.id, sms)   # Выводит информацию о пользователе
                await bot.send_message(sms.chat.id, "Выбери действие", reply_markup=Replay_keyboard.menu)
            else:
                await bi.bot.send_message(sms.chat.id, "Отправте свое фото")

