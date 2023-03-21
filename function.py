import global_variable as gl
import DB
import random
import Replay_keyboard


def input_reg(user_id):
    data = gl.user_keys[f"{user_id}"][0]
    phrases = ["Как тебя зовут?", "Твой пол", "Сколько тебе лет?", "Отправь свое фото",
               "Напиши немного о себе", "Кто тебе интересен?", "Откуда ты?"]
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
        print(gl.user_keys3)
        db = DB.DB("Clop.db")
        my_data = db.SELECT("user", f"id == {sms.chat.id}")[0]
        if my_data[6] != 3:
            data = db.SELECT("user",
                             f"""(sex == {my_data[6]} AND
                              location_no == "{my_data[9]}" AND
                               (sex_poisc == {my_data[2]} OR sex_poisc == 3) AND
                               id != {sms.chat.id}) AND                           
                             (old == {my_data[8]} OR old == {my_data[8] + 1} OR old == {my_data[8] - 1})""")
        else:
            data = db.SELECT("user", f"""(location_no == "{my_data[9]}" AND
                               (sex_poisc == {my_data[2]} OR sex_poisc == 3) AND
                               id != {sms.chat.id}) AND                           
                             (old == {my_data[8]} OR old == {my_data[8] + 1} OR old == {my_data[8] - 1})""")

        if data != -1 and data:
            like_user = db.SELECT("like_user", f"id_user1 == {sms.chat.id}")
            if like_user != -1:  # Проверям есть ли тот кто нас лайкнул
                for i in like_user:
                    gl.user_keys3[f"{sms.chat.id}"][0].append(i[1])  # добавляем их в стек
            for i in range(6):  # заполняет стек новыми людьми
                us = random.randint(0, len(data) - 1)
                while data[us][0] == sms.chat.id or data[us][0] in gl.user_keys3[f"{sms.chat.id}"][0]:
                    # Есть баг поправить ^^^^^^^^^^^^
                    us = random.randint(0, len(data) - 1)
                gl.user_keys3[f"{sms.chat.id}"][0].append(data[us][0])
            await print_rec(sms)

        else:
            await gl.bi.bot.send_message(sms.chat.id,
                                         "К сожалению на данных момент нет пользователей удовлетворяющие вашим характеристикам")
    else:
        await print_rec(sms)


async def like(sms):  # функция вызывается при нажатии на лайк пользователем
    db = DB.DB("Clop.db")
    data = db.SELECT("like_user", f"id_user2 == {sms.chat.id}")
    l_us = []
    for i in data:
        l_us.append(i)
    if data and l_us in gl.user_keys3[f"{sms.chat.id}"][1][0]:
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
