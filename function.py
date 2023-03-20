import global_variable as gl


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
    gl.user_keys[f"{sms.chat.id}"][0][data[0][0]] = sms.text  # Запись значений в словарь
    gl.user_keys[f"{sms.chat.id}"][0][0] += 1  # прокрутка счетчика
