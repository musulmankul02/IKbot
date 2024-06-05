from aiogram import types

def start_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Ыссык - кол', callback_data='region_issyk_kul'))
    keyboard.add(types.InlineKeyboardButton('Профиль клиента', callback_data='profile'))
    return keyboard

def city_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Чолпон-Ата', callback_data='city_cholponata'))
    keyboard.add(types.InlineKeyboardButton('Балыкчы', callback_data='city_balykchy'))
    keyboard.add(types.InlineKeyboardButton('Каракол', callback_data='city_karakol'))
    keyboard.add(types.InlineKeyboardButton('Туп', callback_data='city_tup'))
    keyboard.add(types.InlineKeyboardButton('Жети огуз', callback_data='city_jetiogyz'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    return keyboard


def profile_creation_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Создать профиль", callback_data="create_profile"))
    keyboard.add(types.InlineKeyboardButton("Изменить профиль", callback_data="edit_profile"))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    return keyboard
