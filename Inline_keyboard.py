from aiogram import types

# ______________________________________________________________________________________________________________________

start = types.InlineKeyboardMarkup()
reg = types.InlineKeyboardButton("Регистрация", callback_data='registration')
start.row(reg)

# ______________________________________________________________________________________________________________________

registration = types.InlineKeyboardMarkup()
forward = types.InlineKeyboardButton("➡️", callback_data="forward")    # Набор кнопок
back = types.InlineKeyboardButton("⬅️", callback_data="back")
registration.row(back, forward)

reg_right = types.InlineKeyboardMarkup()    # Клавиатура, которая имеет только кнопку на право
reg_right.row(forward)

reg_left = types.InlineKeyboardMarkup()     # Клавиатура, которая имеет только кнопку на лево
reg_left.row(back)

# _____________________________________________________________________________________________________________________

registration_two = types.InlineKeyboardMarkup()
re_registration = types.InlineKeyboardButton("Заполнить анкету заново", callback_data="re_registration")
re_name = types.InlineKeyboardButton("Изменить имя", callback_data="re_name")


