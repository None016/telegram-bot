import aiogram as ai

bot = ai.Bot(token="6158786303:AAGxXgKENOi-AwI7T8Df92aXUH9vLL9ypC0")
bi = ai.Dispatcher(bot)

user_keys = {}  # Используется для полной регистрации
user_keys2 = {}  # Используется для обновления данных [ключ, значение]
user_keys3 = {}  # Используется для поиска [[непоказанные пользователи],[[последний пользователь показанный в ленте]]
user_location = {}  # Используется для опознания есть ли данные по его местоположению [первая ось, вторая ось]

converter_for_sex = {"Мужской": 1, "Женский": 2}
converter_for_sex_poisc = {"Парни": 1, "Девушки": 2, "Без разницы": 3}
converter_for_re_registration = ["nic_for_poisc", "description", "location", ]


def app_user_keys(user_id):
    user_keys[f"{user_id}"] = [[None, None, None, None, None, None, None, None, None, None]]  # 0 - key_reg
    # ^^^^^^^^^^ | 1 - name_user | 2 - sex | 3 - old | 4 - photo | 5 - description | 6 - poisc_sex | 7 - location
    # | 8 - loc_lat | 9 - loc_long


def app_user_keys2(user_id):
    user_keys2[f"{user_id}"] = [None, None]


def conditions_select_1(my_data, sms, age_difference):  # Нужно оптимизировать
    print(1)
    return f'''sex == {my_data[6]} AND
                location_no == "{my_data[9]}" AND
                (sex_poisc == {my_data[2]} OR sex_poisc == 3) AND
                id != {sms.chat.id} AND                           
                (old == {my_data[8]} OR (old <= {my_data[8] + age_difference} AND
                old >= {my_data[8] - age_difference}))'''


def conditions_select_2(my_data, sms, age_difference):  # Нужно оптимизировать
    print(2)
    return f'''location_no == "{my_data[9]}" AND
                (sex_poisc == {my_data[2]} OR sex_poisc == 3) AND
                id != {sms.chat.id} AND                           
                (old == {my_data[8]} OR (old <= {my_data[8] + age_difference} AND
                old >= {my_data[8] - age_difference}))'''


def conditions_select_3(my_data, sms, age_difference):  # Нужно оптимизировать
    print(3)
    return f'''location_no == "000" AND
                (sex_poisc == {my_data[2]} OR sex_poisc == 3) AND
                id != {sms.chat.id} AND                           
                (old == {my_data[8]} OR (old <= {my_data[8] + age_difference} AND
                old >= {my_data[8] - age_difference})) AND
                (loc_lat <= {my_data[10] + 0.01} AND loc_lat >= {my_data[10] - 0.01} AND
                loc_long <= {my_data[11] + 0.01} AND loc_long >= {my_data[11] - 0.01})'''


def conditions_select_4(my_data, sms, age_difference):  # Нужно оптимизировать
    print(4)
    return f'''sex == {my_data[6]} AND location_no == "000" AND
                (sex_poisc == {my_data[2]} OR sex_poisc == 3) AND
                id != {sms.chat.id} AND                           
                (old == {my_data[8]} OR (old <= {my_data[8] + age_difference} AND
                old >= {my_data[8] - age_difference})) AND
                (loc_lat <= {my_data[10] + 0.01} AND loc_lat >= {my_data[10] - 0.01} AND
                loc_long <= {my_data[11] + 0.01} AND loc_long >= {my_data[11] - 0.01})'''
