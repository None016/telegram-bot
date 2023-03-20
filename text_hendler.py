import global_variable
from global_variable import *
import function as fun
import Replay_keyboard
import DB


@bi.message_handler(content_types=["text", "photo"])
async def text(sms: ai.types.Message):
    if f"{sms.chat.id}" in user_keys.keys():
        data = user_keys[f"{sms.chat.id}"]
        print(data)
        if data[0][0] != 4 and data[0][0] != -1 and data[0][0] != 6 or data[0][0] == 5:
            # ^^^^^^^^^^ Исключение в виде отправления фото
            if data[0][0] == 1:     # Исключение для ввода перед полом
                user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.text   # Запись значений в словарь
                user_keys[f"{sms.chat.id}"][0][0] += 1      # прокрутка счетчика
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                          reply_markup=Replay_keyboard.sex_keyboard)
            elif data[0][0] == 5:
                user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.text  # Запись значений в словарь
                user_keys[f"{sms.chat.id}"][0][0] += 1  # прокрутка счетчика
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                          reply_markup=Replay_keyboard.search_by_gender)
            elif data[0][0] == 2:
                if sms.text in global_variable.converter_for_sex.keys():
                    # ^^^^^^^^^^ проверка на нажатие на кнопку для дальнейшего верного преобразования
                    user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.text  # Запись значений в словарь
                    user_keys[f"{sms.chat.id}"][0][0] += 1  # прокрутка счетчика
                    await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))
                else:
                    user_keys[f"{sms.chat.id}"][0][0] = 2  # прокрутка счетчика
                    await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                              reply_markup=Replay_keyboard.sex_keyboard)
            else:
                print(data)
                user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.text   # Запись значений в словарь
                user_keys[f"{sms.chat.id}"][0][0] += 1      # прокрутка счетчика
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))
        elif data[0][0] == 4:       # Исключение если пришло время для фото
            user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.photo[-1].file_id
            user_keys[f"{sms.chat.id}"][0][0] += 1
            await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id))
        elif data[0][0] == 6:
            print(data)
            if sms.text in global_variable.converter_for_sex_poisc.keys():
                # ^^^^^^^^^^ проверка на нажатие на кнопку для дальнейшего верного преобразования
                user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.text
                user_keys[f"{sms.chat.id}"][0][0] = -1
                await bi.bot.send_photo(sms.chat.id, photo=data[0][4],
                                        caption=f"{data[0][1]}, {data[0][2]}, {data[0][3]} \n{data[0][5]}")
                # Вывод введенных данных
                await bi.bot.send_message(sms.chat.id, "Все верно?", reply_markup=Replay_keyboard.binary_response)
            else:
                user_keys[f"{sms.chat.id}"][0][0] = 6  # прокрутка счетчика
                await bi.bot.send_message(sms.chat.id, fun.input_reg(sms.chat.id),
                                          reply_markup=Replay_keyboard.search_by_gender)
        elif data[0][0] == -1:
            if sms.text == "Да":
                DB.add_user(sms.chat.id, sms["from"]["first_name"], data[0][2],
                            data[0][1], data[0][4], data[0][5], data[0][6])
                del(user_keys[f"{sms.chat.id}"])
                await bi.bot.send_message(sms.chat.id, "temp mesage")
            elif sms.text == "Изменить анкету":
                await bi.bot.send_message(sms.chat.id, "temp mesage")
        print(data)

