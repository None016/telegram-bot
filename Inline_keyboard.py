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
re_registration = types.InlineKeyboardButton("Заполнить анкету заново", callback_data="registration")
re_name = types.InlineKeyboardButton("Имя", callback_data="re_name")
re_distraction = types.InlineKeyboardButton("Описание", callback_data="re_distraction")
re_location = types.InlineKeyboardButton("Местоположение", callback_data="re_location")
re_photo = types.InlineKeyboardButton("Фото", callback_data="re_photo")
registration_two.row(re_name, re_distraction, re_photo)
registration_two.row(re_location)
registration_two.row(re_registration)
