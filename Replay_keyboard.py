from aiogram import types

sex_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
boy_button = types.KeyboardButton("Мужской")
girl_button = types.KeyboardButton("Женский")

sex_keyboard.row(boy_button, girl_button)

# _____________________________________________________________________________________________________________________

binary_response = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
true_button = types.KeyboardButton("Да")
false_button = types.KeyboardButton("Изменить анкету")
binary_response.row(true_button, false_button)

# _____________________________________________________________________________________________________________________

search_by_gender = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
boy_poisc = types.KeyboardButton("Парни")
girl_poisc = types.KeyboardButton("Девушки")
doesnt_matter = types.KeyboardButton("Без разницы")
search_by_gender.row(boy_poisc, girl_poisc, doesnt_matter)

# _____________________________________________________________________________________________________________________

menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
Change_profile = types.KeyboardButton("Изменить анкету")
View_profile = types.KeyboardButton("🚀Лента🚀")
My_profile = types.KeyboardButton("Моя анкета")
menu.row(Change_profile, View_profile)
menu.row(My_profile)

# _____________________________________________________________________________________________________________________

assessment = types.ReplyKeyboardMarkup(resize_keyboard=True)
lick_p = types.KeyboardButton("❤️")
diz_lick_p = types.KeyboardButton("👎")
assessment.row(lick_p, diz_lick_p)
