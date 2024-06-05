from aiogram import types

start_options_buttons = [
    types.InlineKeyboardButton('Прорекламировать отель', callback_data='advertise_hotel'),
    types.InlineKeyboardButton('Мои объявления', callback_data='my_ads')
]
start_options_markup = types.InlineKeyboardMarkup().add(*start_options_buttons)

start_region_buttons = [
    types.InlineKeyboardButton('Ыссык - кол', callback_data='region_issyk_kol')
]
start_region_markup = types.InlineKeyboardMarkup().add(*start_region_buttons)

start_raion_buttons = [
    types.InlineKeyboardButton('Чолпон-Ата', callback_data='raion_cholpon_ata'),
    types.InlineKeyboardButton('Балыкчы', callback_data='raion_balykchy'),
    types.InlineKeyboardButton('Каракол', callback_data='raion_karakol')
]
start_raion_markup = types.InlineKeyboardMarkup().add(*start_raion_buttons)

alloc_but = [
    types.InlineKeyboardButton('Квартира', callback_data='alloc_apartment'),
    types.InlineKeyboardButton('Койко место', callback_data='alloc_bed'),
    types.InlineKeyboardButton('Коттедж', callback_data='alloc_cottage'),
    types.InlineKeyboardButton('Номер', callback_data='alloc_room'),
    types.InlineKeyboardButton('Таунхаус', callback_data='alloc_townhouse'),
    types.InlineKeyboardButton('Юрта', callback_data='alloc_yurt')
]
start_hotels = types.InlineKeyboardMarkup().add(*alloc_but)

finish = [
    types.InlineKeyboardButton('разместить еще', callback_data='more'),
    types.InlineKeyboardButton('профиль отеля', callback_data='profile_hotel')
]
start_finish = types.InlineKeyboardMarkup().add(*finish)