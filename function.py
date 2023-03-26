import global_variable as gl
import DB
import random
import Replay_keyboard


def input_reg(user_id):
    data = gl.user_keys[f"{user_id}"][0]
    phrases = ["Как тебя зовут?", "Твой пол", "Сколько тебе лет?", "Отправь свое фото",
               "Напиши немного о себе", "Кто тебе интересен?",
               "Откуда ты?(Напиши свой город или отправь свое местоположение)"]
    if data[0] >= 7:
        return phrases[6]
    if data[0] <= 1:
        return phrases[0]
    else:
        return phrases[data[0] - 1]


def add_user_key(sms, data):
    gl.user_keys[f"{sms.chat.id}"][0][data[0]] = sms.text  # Запись значений в словарь
    gl.user_keys[f"{sms.chat.id}"][0][0] += 1  # прокрутка счетчика


def update_reg(sms, db, column):
    db.UPDATE("user", f"{column} = '{sms.text}'", f"id == {sms.chat.id}")
    del(gl.user_keys2[f"{sms.chat.id}"])


async def print_inf_user(id, sms):
    db = DB.DB("Clop.db")
    data = db.SELECT("user", f"id == {id}")[0]
    await gl.bi.bot.send_photo(sms.chat.id, photo=data[4], caption=f"{data[3]}, {data[7]}, {data[8]}\n{data[5]}")


async def print_rec(sms):
    await print_inf_user(gl.user_keys3[f"{sms.chat.id}"][0][0], sms)
    gl.user_keys3[f"{sms.chat.id}"][1].append(gl.user_keys3[f"{sms.chat.id}"][0][0])
    del (gl.user_keys3[f"{sms.chat.id}"][0][0])
    if len(gl.user_keys3[f"{sms.chat.id}"][1]) >= 2:
        del (gl.user_keys3[f"{sms.chat.id}"][1][0])


async def recommendations(sms):
    if len(gl.user_keys3[f"{sms.chat.id}"][0]) == 0:
        db = DB.DB("Clop.db")

        my_data = db.SELECT("user", f"id == {sms.chat.id}")[0]

        age_difference = 1
        data = []
        if my_data[6] != 3 and my_data[9] != "000":  # Если важен пол и неизвестны координаты

            while len(data) <= 6:  # Цикл набирает нужное число пользователей изменяя возраст
                data = db.SELECT("user", gl.conditions_select_1(my_data, sms, age_difference))
                age_difference += 1  # Защита от вечного цикла

                if age_difference >= 15:  # Если цикл повторился 15 раз
                    data = []  # то цикл прерывается и возвращает пустое значение
                    break

        elif my_data[6] == 3 and my_data[9] != "000":  # Если пол не важен и неизвестны координаты

            while len(data) <= 6:
                data = db.SELECT("user", gl.conditions_select_2(my_data, sms, age_difference))
                age_difference += 1

                if age_difference >= 15:
                    data = []
                    break

        elif my_data[6] == 3 and my_data[9] == "000":  # Если пол не важен и известны координаты
            gl.user_location[f"{sms.chat.id}"] = [my_data[10], my_data[11]]  # Добавляем в словарь свои координаты

            while len(data) <= 6:
                data = db.SELECT("user", gl.conditions_select_3(my_data, sms, age_difference))
                age_difference += 1

                if age_difference >= 15:
                    data = []
                    break

        elif my_data[6] != 3 and my_data[9] == "000":  # Если пол важен и известны координаты
            gl.user_location[f"{sms.chat.id}"] = [my_data[10], my_data[11]]    # Добавляем в словарь свои координаты

            while len(data) <= 6:
                data = db.SELECT("user", gl.conditions_select_4(my_data, sms, age_difference))
                age_difference += 1

                if age_difference >= 15:
                    data = []
                    break

        if data != -1 and data:
            like_user = db.SELECT("like_user", f"id_user2 == {sms.chat.id}")
            if like_user != -1:  # Проверям есть ли тот кто нас лайкнул
                for i in like_user:
                    gl.user_keys3[f"{sms.chat.id}"][0].append(i[0])  # добавляем их в стек

            for i in range(6):  # заполняет стек новыми людьми
                us = random.randint(0, len(data) - 1)
                counter = 0
                while data[us][0] == sms.chat.id or data[us][0] in gl.user_keys3[f"{sms.chat.id}"][0]:
                    counter += 1
                    # Есть баг поправить ^^^^^^^^^^^^
                    us = random.randint(0, len(data) - 1)
                    if counter >= 15:
                        break
                gl.user_keys3[f"{sms.chat.id}"][0].append(data[us][0])
            if my_data[9] == "000":  # если известного его место положение
                db = DB.DB("Clop.db")
                data = db.SELECT("user", f"id == {gl.user_keys3[f'{sms.chat.id}'][0][0]}")[0]
                temp = gl.user_location[f"{sms.chat.id}"]
                await gl.bi.bot.send_photo(sms.chat.id, photo=data[4],
                                           caption=f"{data[3]}, {location(temp[0], temp[1], data[10], data[11])}м, {data[8]}\n{data[5]}")
                gl.user_keys3[f"{sms.chat.id}"][1].append(gl.user_keys3[f"{sms.chat.id}"][0][0])
                del (gl.user_keys3[f"{sms.chat.id}"][0][0])

                if len(gl.user_keys3[f"{sms.chat.id}"][1]) >= 2:
                    del (gl.user_keys3[f"{sms.chat.id}"][1][0])
            else:
                await print_rec(sms)

        else:
            await gl.bi.bot.send_message(sms.chat.id,
                                         "К сожалению на данных момент нет пользователей удовлетворяющие вашим характеристикам",
                                         reply_markup=Replay_keyboard.menu)
    else:
        if f"{sms.chat.id}" in gl.user_location.keys():
            db = DB.DB("Clop.db")
            data = db.SELECT("user", f"id == {gl.user_keys3[f'{sms.chat.id}'][0][0]}")[0]
            temp = gl.user_location[f"{sms.chat.id}"]
            await gl.bi.bot.send_photo(sms.chat.id, photo=data[4],
                                       caption=f"{data[3]}, {location(temp[0], temp[1], data[10], data[11])}м, {data[8]}\n{data[5]}")
            gl.user_keys3[f"{sms.chat.id}"][1].append(gl.user_keys3[f"{sms.chat.id}"][0][0])
            del (gl.user_keys3[f"{sms.chat.id}"][0][0])

            if len(gl.user_keys3[f"{sms.chat.id}"][1]) >= 2:
                del (gl.user_keys3[f"{sms.chat.id}"][1][0])
        else:
            await print_rec(sms)


async def like(sms):  # функция вызывается при нажатии на лайк пользователем
    db = DB.DB("Clop.db")
    data = db.SELECT("like_user", f"id_user2 == {sms.chat.id}")
    l_us = []
    if data:
        for i in data:
            l_us.append(i[0])
    if data and gl.user_keys3[f"{sms.chat.id}"][1][0] in l_us:
        await gl.bi.bot.send_message(sms.chat.id, "Вы обоюдно понравились друг другу",
                                     # отправка последнему лакавшему ^^^^^^^^^^
                                     reply_markup=Replay_keyboard.menu)
        await print_inf_user(data[0][0], sms)
        await gl.bi.bot.send_message(data[0][0], "Вы обоюдно понравились друг другу",
                                     # отправка кого лайкнули ^^^^^^^^^^^
                                     reply_markup=Replay_keyboard.menu)
        data2 = db.SELECT("user", f"id == {sms.chat.id}")[0]
        await gl.bi.bot.send_photo(data[0][0], photo=data2[4],
                                   caption=f"{data2[3]}, {data2[7]}, {data2[8]}\n{data2[5]}")
        db.DELETE("like_user", f"id_user2 == {sms.chat.id}")
        del(gl.user_keys3[f"{sms.chat.id}"])  # выводим его из поиска
        if f"{data[0][0]}" in gl.user_keys3.keys():  # выводим его из поиска если от там есть
            del (gl.user_keys3[f"{data[0][0]}"])
    else:
        db.INSERT("like_user", "(?, ?)", [(sms.chat.id, gl.user_keys3[f"{sms.chat.id}"][1][0])])
        # Записываем в базу кого лайкнули ^^^^^^^^^^^^


def location(loc_lat1, loc_long1, loc_lat2, loc_long2):
    return int(((abs((loc_lat1 - loc_lat2) ** 2) + abs((loc_long1 - loc_long2) ** 2)) ** 0.5) * 111_000)


async def wrong_data_type(namber, sms):
    gl.user_keys[f"{sms.chat.id}"][0][0] = namber
    await gl.bi.bot.send_message(sms.chat.id, input_reg(sms.chat.id))
