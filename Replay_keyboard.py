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

