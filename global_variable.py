import aiogram as ai

bot = ai.Bot(token="6158786303:AAGxXgKENOi-AwI7T8Df92aXUH9vLL9ypC0")
bi = ai.Dispatcher(bot)

user_keys = {}  # Используется для полной регистрации
user_keys2 = {}  # Используется для обновления данных

converter_for_sex = {"Мужской": 1, "Женский": 2}
converter_for_sex_poisc = {"Парни": 1, "Девушки": 2, "Без разницы": 3}
converter_for_re_registration = ["nic_for_poisc", "description", "location", ]


def app_user_keys(user_id):
    user_keys[f"{user_id}"] = [[None, None, None, None, None, None, None, None]]  # 0 - key_reg | 1 - name_user | 2 - sex
    # ^^^^^^^^^^ | 3 - old | 4 - photo | 5 - description | 6 - poisc_sex | 7 - location


def app_user_keys2(user_id):
    user_keys2[f"{user_id}"] = [None, None]
