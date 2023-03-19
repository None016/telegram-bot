import aiogram
import global_variable as gl


def input_reg(user_id):
    data = gl.user_keys[f"{user_id}"][0]
    phrases = ["Как тебя зовут?", "Твой пол", "Сколько тебе лет?", "Отправь свое фото"]
    if data[0] >= 4:
        return phrases[3]
    if data[0] <= 1:
        return phrases[0]
    else:
        return phrases[data[0] - 1]



