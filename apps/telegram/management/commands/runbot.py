import logging
import os
import re
import django
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from asgiref.sync import sync_to_async
from dotenv import load_dotenv

from apps.telegram.button.button_cklient import city_keyboard, start_keyboard
from apps.telegram.models import Booking, AccommodationType, Pension, UserBusness, Invitation, District, User

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Загрузка переменных окружения
load_dotenv('.env')

# Настройка бота
bot = Bot(token='6962324611:AAFrx-xzFHHyvBvRuy5lvEiiqpS9occpiyk')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# Жестко закодированные данные
districts = {
    'Балыкчи': ['Аврора', 'Алтын'],
    'Чолпон-Ата': ['Голубой', 'Радуга'],
    'Каракол': ['АлтынАрашан', 'Каракол'],
    'Тюп': ['Тюпский', 'ТюпТауэр'],
    'Джетигез': ['Аврора', 'Алтын']
}
amenities = ['Еда', 'Кондиционер', 'Стиральная машина', 'Утюг', 'Балкон', 'Wi-Fi', 'Бассейн', 'Парковка', 'Фитнес-зал']
accommodation_types = ['Квартира', 'Тансаус', 'Пентхаус', 'Юрта', 'Вилла']

def start_keyboard2():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Продолжить', callback_data='сontinue'))
    keyboard.add(types.InlineKeyboardButton('Профиль клиента', callback_data='profile_busness'))
    return keyboard

class BookingState(StatesGroup):
    waiting_for_number_of_people = State()
    waiting_for_distance_to_beach = State()
    waiting_for_phone_number = State()
    waiting_for_price = State()
    waiting_for_photos = State()
    waiting_for_city = State()
    waiting_for_date = State()
    waiting_for_comment = State()
    waiting_for_amenities = State()
    waiting_for_invitation = State()

def create_amenities_keyboard(selected_amenities):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for amenity in amenities:
        text = f"✅ {amenity}" if amenity in selected_amenities else amenity
        keyboard.insert(types.InlineKeyboardButton(text, callback_data=f'amenity_{amenity}'))
    keyboard.add(types.InlineKeyboardButton('Готово', callback_data='done_selecting_amenities'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    return keyboard

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    logging.info("Команда /start получена")
    user_id = message.from_user.id
    username = message.from_user.username

    if not await sync_to_async(UserBusness.objects.filter(user_id=user_id).exists)():
        start_command = message.text
        referrer_id = str(start_command[7:])
        if referrer_id:
            if referrer_id != str(user_id):
                await sync_to_async(UserBusness.objects.create)(user_id=user_id, referrer_id=referrer_id)
                await bot.send_message(referrer_id, 'По вашей ссылке зарегистрировался новый пользователь')
                await message.answer('Вы зарегистрировались по реферальной ссылке.')
            else:
                await sync_to_async(UserBusness.objects.create)(user_id=user_id)
                await message.answer("Нельзя регистрировать по собственной реферальной ссылке.")
        else:
            await sync_to_async(UserBusness.objects.create)(user_id=user_id)

    await message.answer(
        "Здравствуйте! Выберите тип пользователя:",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Клиент', callback_data='client_start'),
            types.InlineKeyboardButton('Бизнес', callback_data='business_start')
        )
    )

@dp.callback_query_handler(lambda c: c.data == 'client_start')
async def client_start(callback_query: types.CallbackQuery):
    logging.info("Callback client_start получен")
    keyboard = start_keyboard()
    await callback_query.message.edit_text(
        "Здравствуйте! 🏨 Я ваш личный помощник по поиску отелей и пансионатов. Укажите ваши предпочтения, и я найду идеальное место для вашего отдыха. Давайте начнем путешествие вместе! 🌍✨\n\n",
        reply_markup=keyboard,
        parse_mode=types.ParseMode.MARKDOWN
    )
    logging.info("Сообщение client_start успешно отправлено")

@dp.callback_query_handler(lambda c: c.data == 'business_start')
async def business_start(callback_query: types.CallbackQuery):
    logging.info("Callback business_start получен")
    keyboard = start_keyboard2()
    await callback_query.message.edit_text(
       """ Вы выбрали тип пользователя 'Бизнес'.
        Примерный заполнение:
        1) Город :
        2) Район :
        3) Пансионаты :
        4) Тип размещение :
        5) Количество мест :
        6) Удобства :
        7) Расстояние до пляжа от отеля :
        8) Номер телефона (номер телефона должно начинаться +996):
        9) Цена :
        10) Фото отеля :""",
        reply_markup=keyboard,
        parse_mode=types.ParseMode.MARKDOWN
    )
    logging.info("Сообщение business_start успешно отправлено")

@dp.callback_query_handler(lambda c: c.data == 'сontinue')
async def сontinue(callback_query: types.CallbackQuery):
    logging.info("Callback сontinue получен")
    business_text = """
    Для размещения объявления, пожалуйста, выберите район.
    """
    keyboard = types.InlineKeyboardMarkup()
    for district in districts.keys():
        keyboard.add(types.InlineKeyboardButton(district, callback_data=f'district_{district}'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    await callback_query.message.edit_text(business_text, reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data == 'profile_busness')
async def profile_busness(query: types.CallbackQuery):
    user_id = query.from_user.id
    username = query.from_user.username

    profile_text = f"""
    Ваш профиль:
    ID: {user_id}
    Username: {username}
    """

    keyboard = types.InlineKeyboardMarkup()
    if username.startswith('busness_'):
        keyboard.add(types.InlineKeyboardButton('Поиск отеля', callback_data='search'))
        profile_text += "\n\nВы клиент и не можете размещать объявления отелей."
    else:
        keyboard.add(types.InlineKeyboardButton('Мои объявления', callback_data='my_ads_busness'))

    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='back'))

    await query.message.edit_text(profile_text, reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith('district_'))
async def district_pensions(query: types.CallbackQuery, state: FSMContext):
    district = query.data.split('_')[1]
    await state.update_data(district=district)
    keyboard = types.InlineKeyboardMarkup()
    for pension in districts[district]:
        keyboard.add(types.InlineKeyboardButton(pension, callback_data=f'pension_{pension[:30]}'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='business_start'))
    await query.message.edit_text("Пансионаты в районе:", reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith('pension_'))
async def select_accommodation_type(query: types.CallbackQuery, state: FSMContext):
    pension = query.data.split('_')[1]
    await state.update_data(pension=pension)
    keyboard = types.InlineKeyboardMarkup()
    for acc_type in accommodation_types:
        keyboard.add(types.InlineKeyboardButton(acc_type, callback_data=f'acc_{acc_type[:30]}'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data=f'district_{(await state.get_data()).get("district")}'))
    await query.message.edit_text("Выберите тип размещения:", reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith('acc_'))
async def ask_number_of_people(query: types.CallbackQuery, state: FSMContext):
    accommodation = query.data.split('_')[1]
    await state.update_data(accommodation=accommodation)
    await query.message.edit_text("Количество мест :", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Назад', callback_data=f'pension_{(await state.get_data()).get("pension")[:30]}')))
    await BookingState.waiting_for_number_of_people.set()

@dp.message_handler(state=BookingState.waiting_for_number_of_people)
async def number_of_people(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите корректное количество людей:")
        return
    number_of_people = int(message.text)
    await state.update_data(number_of_people=number_of_people)
    await ask_amenities(message)

async def ask_amenities(message: types.Message):
    keyboard = create_amenities_keyboard([])
    await message.answer("Выберите удобства (можно выбрать несколько):", reply_markup=keyboard)
    await BookingState.waiting_for_amenities.set()

@dp.callback_query_handler(lambda query: query.data.startswith('amenity_'), state=BookingState.waiting_for_amenities)
async def select_amenity(query: types.CallbackQuery, state: FSMContext):
    amenity = query.data.split('_')[1]
    data = await state.get_data()
    selected_amenities = data.get('selected_amenities', [])
    if amenity not in selected_amenities:
        selected_amenities.append(amenity)
        logging.info(f"Услуга '{amenity}' выбрана")
    else:
        selected_amenities.remove(amenity)
        logging.info(f"Услуга '{amenity}' отменена")
    await state.update_data(selected_amenities=selected_amenities)
    keyboard = create_amenities_keyboard(selected_amenities)
    await query.message.edit_reply_markup(reply_markup=keyboard)
    await query.answer(f"Удобство {amenity} выбрано")

@dp.callback_query_handler(lambda query: query.data == 'done_selecting_amenities', state=BookingState.waiting_for_amenities)
async def done_selecting_amenities(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected_amenities = data.get('selected_amenities', [])
    await state.update_data(selected_amenities=selected_amenities)
    logging.info(f"Выбраны следующие удобства: {', '.join(selected_amenities)}")
    await query.message.edit_text(f"Вы выбрали следующие удобства: {', '.join(selected_amenities)}")
    await ask_distance_to_beach(query.message)

async def ask_distance_to_beach(message: types.Message):
    await message.answer("Укажите расстояние до пляжа (в метрах):", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Назад', callback_data='back')))
    await BookingState.waiting_for_distance_to_beach.set()

@dp.message_handler(state=BookingState.waiting_for_distance_to_beach)
async def distance_to_beach(message: types.Message, state: FSMContext):
    distance_text = message.text.strip()
    # Удаляем все не числовые символы
    distance_text = ''.join(filter(str.isdigit, distance_text))
    if not distance_text.isdigit():
        await message.answer("Пожалуйста, введите корректное расстояние до пляжа (в метрах):")
        return
    distance_to_beach = int(distance_text)
    await state.update_data(distance_to_beach=distance_to_beach)
    await ask_phone_number(message)

async def ask_phone_number(message: types.Message):
    await message.answer("Введите ваш номер телефона (начинается с +996):", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Назад', callback_data='back')))
    await BookingState.waiting_for_phone_number.set()

@dp.message_handler(state=BookingState.waiting_for_phone_number)
async def phone_number(message: types.Message, state: FSMContext):
    phone_number = message.text.strip()
    if not phone_number.startswith("+996") or not phone_number[4:].isdigit():
        await message.answer("Пожалуйста, введите корректный номер телефона (начинается с +996):")
        return
    await state.update_data(phone_number=phone_number)
    await ask_price(message, state)

async def ask_price(message: types.Message, state: FSMContext):
    await message.answer("Укажите цену (в сомах):", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Назад', callback_data='back')))
    await BookingState.waiting_for_price.set()

@dp.message_handler(state=BookingState.waiting_for_price)
async def price(message: types.Message, state: FSMContext):
    price_text = message.text.strip()
    # Удаляем все не числовые символы
    price_text = ''.join(filter(str.isdigit, price_text))
    if not price_text.isdigit():
        await message.answer("Пожалуйста, введите корректную цену (в сомах):")
        return
    price = int(price_text)
    await state.update_data(price=price)
    await ask_photos(message, state)

async def ask_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo_message_id = data.get('photo_message_id')
    if photo_message_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=photo_message_id)

    msg = await message.answer(
        "Загрузите от 5 до 10 фотографий:", 
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Завершить загрузку', callback_data='done_uploading_photos')
        )
    )
    await state.update_data(photo_message_id=msg.message_id)
    await BookingState.waiting_for_photos.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=BookingState.waiting_for_photos)
async def handle_photos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos', [])
    photo_id = message.photo[-1].file_id
    photos.append(photo_id)
    await state.update_data(photos=photos)

    # Edit the existing message with the new photo count
    photo_message_id = data.get('photo_message_id')
    if photo_message_id:
        await bot.edit_message_text(
            f"Вы загрузили {len(photos)} фотографий. Вы можете загрузить еще {10 - len(photos)} фотографий.",
            chat_id=message.chat.id,
            message_id=photo_message_id,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton('Завершить загрузку', callback_data='done_uploading_photos')
            )
        )

@dp.callback_query_handler(lambda query: query.data == 'done_uploading_photos', state=BookingState.waiting_for_photos)
async def done_uploading_photos(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photos = data.get('photos', [])

    if len(photos) < 5:
        await query.answer("Пожалуйста, загрузите минимум 5 фотографий.")
    else:
        await state.update_data(photos=photos)
        await state.update_data(user_id=query.from_user.id)  # Добавляем user_id в данные состояния
        await ask_for_invitation(query.message, state)

async def ask_for_invitation(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data['user_id']
    await message.answer(
        f"Загрузите одного пользователя через ссылку ниже и нажмите 'Разместить отель', когда он присоединится:\n\n"
        f"Для бота: [https://t.me/WeartherallBot?start={user_id}](https://t.me/WeartherallBot?start={user_id})",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton('Назад', callback_data='back'),
            types.InlineKeyboardButton('Разместить отель', callback_data='check_invitation')
        ),
        parse_mode=types.ParseMode.MARKDOWN
    )
    await BookingState.waiting_for_invitation.set()

@dp.callback_query_handler(lambda query: query.data == 'check_invitation', state=BookingState.waiting_for_invitation)
async def check_invitation(query: types.CallbackQuery, state: FSMContext):
    user_id = query.from_user.id
    referrer_id = await sync_to_async(UserBusness.objects.filter(user_id=user_id).values_list('referrer_id', flat=True).first)()
    invited_user_exists = await sync_to_async(UserBusness.objects.filter(referrer_id=user_id).exists)()
    logging.info(f"Проверка статуса приглашения для user ID: {user_id}, invited_user_exists: {invited_user_exists}")

    if invited_user_exists:
        await save_booking(query.message, state)
    else:
        await query.message.answer("Пожалуйста, пригласите одного пользователя через реферальную ссылку, прежде чем размещать отель.")
        logging.info("Пользователю нужно пригласить хотя бы одного человека, чтобы продолжить.")

async def save_booking(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.chat.id
    region_name = data['district']  # Предполагаем, что 'district' эквивалентен 'region'
    city = data.get('city', 'Не указано')
    checkout_date = data.get('checkout_date', '1970-01-01')
    comment = data.get('comment', 'Нет комментариев')
    number_of_people = data['number_of_people']
    selected_amenities = data.get('selected_amenities', [])
    distance_to_beach = data.get('distance_to_beach', 0)
    phone_number = data.get('phone_number', '')
    price = data.get('price', 0)
    photos = data.get('photos', [])

    logging.info(f"Сохранение данных отеля: {data}")

    # Убедитесь, что запись в таблице User существует
    user, created = await sync_to_async(User.objects.get_or_create)(id=user_id)

    # Создание записи в базе данных
    booking = await sync_to_async(Booking.objects.create)(
        user=user,
        region=region_name,
        city=city,
        checkout_date=checkout_date,
        comment=comment,
        number_of_people=number_of_people,
        amenities=selected_amenities,
        distance_to_beach=distance_to_beach,
        phone_number=phone_number,
        price=price,
        photos=",".join(photos)  # Сохранение фотографий как строки с разделением через запятую
    )

    # Подтверждающее сообщение об успешном сохранении
    await message.answer(
        "Ваш отель успешно сохранен.",
        reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Разместить еще', callback_data='business_start'))
    )
    await state.finish()


@dp.callback_query_handler(lambda query: query.data == 'profile')
async def profile(query: types.CallbackQuery):
    user_id = query.from_user.id
    username = query.from_user.username

    profile_text = f"""
    Ваш профиль:
    ID: {user_id}
    Username: {username}
    """

    keyboard = types.InlineKeyboardMarkup()
    if username.startswith('client_'):
        keyboard.add(types.InlineKeyboardButton('Поиск отеля', callback_data='search'))
        profile_text += "\n\nВы клиент и не можете размещать объявления отелей."
    else:
        keyboard.add(types.InlineKeyboardButton('Мои объявления', callback_data='my_ads'))

    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='back'))

    await query.message.edit_text(profile_text, reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data == 'back', state='*')
async def back_to_start(query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.edit_text("Вы вернулись назад.", reply_markup=types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Клиент', callback_data='client_start'),
        types.InlineKeyboardButton('Бизнес', callback_data='business_start')
    ))

@dp.callback_query_handler(lambda query: query.data == 'search')
async def search(query: types.CallbackQuery):
    await query.message.edit_text("Поиск активирован! 🔍")

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member_handler(message: types.Message):
    new_members = message.new_chat_members
    inviter_id = message.from_user.id

    for member in new_members:
        referrer_id = inviter_id
        logging.info(f"ID пригласившего: {referrer_id}")
        referrer_user = await sync_to_async(UserBusness.objects.get)(user_id=referrer_id)

        new_user, created = await sync_to_async(UserBusness.objects.get_or_create)(
            user_id=member.id,
            defaults={'referrer_id': referrer_id, 'referral_status': 1}
        )
        
        if not created:
            new_user.referrer_id = referrer_id
            new_user.referral_status = 1
            await sync_to_async(new_user.save)()

        logging.info(f"Создан новый пользователь с ID: {new_user.user_id}, приглашен: {referrer_id}, создан: {created}")

        await sync_to_async(Invitation.objects.create)(user=new_user, invited_by=referrer_user)

        await bot.send_message(referrer_user.user_id, f"Пользователь {new_user.user_id} зарегистрировался по вашей реферальной ссылке.")
        logging.info(f"Приглашение сохранено и пригласивший уведомлен для user ID: {new_user.user_id}")

@dp.callback_query_handler(lambda query: query.data == 'my_ads')
async def my_ads(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('Назад', callback_data='client_start')
    )
    await query.message.edit_text("У вас нет объявлений", reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data == 'my_ads_busness')
async def my_ads_busness(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Объявления', callback_data='сontinue'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data='client_start'))
    await query.message.edit_text("У вас нет объявлений", reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data.startswith('region_'))
async def region(query: types.CallbackQuery, state: FSMContext):
    current_text = 'Теперь вам нужно выбрать ваш город!'
    current_markup = city_keyboard()
    await query.message.edit_text(current_text, reply_markup=current_markup)
    await BookingState.waiting_for_city.set()

@dp.callback_query_handler(state=BookingState.waiting_for_city)
async def city(query: types.CallbackQuery, state: FSMContext):
    city = query.data.split('_')[1]
    valid_cities = ['cholponata', 'balykchy', 'karakol', 'tup', 'jetiogyz']

    logging.debug(f"Выбранный город: {city}")

    if city not in valid_cities:
        current_text = 'Пожалуйста, выберите город из предложенных вариантов.'
        current_markup = city_keyboard()
        await query.message.edit_text(current_text, reply_markup=current_markup)
        return

    await state.update_data(city=city)
    await query.message.edit_text('Введите дату заезда (в формате ГГГГ.ММ.ДД):', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Назад', callback_data='back')))
    await BookingState.waiting_for_date.set()

@dp.message_handler(state=BookingState.waiting_for_date)
async def checkout_date(message: types.Message, state: FSMContext):
    date_pattern = re.compile(r'\d{4}\.\d{2}\.\d{2}')
    if not date_pattern.match(message.text):
        await message.answer('Неверный формат даты. Пожалуйста, введите дату в формате ГГГГ.ММ.ДД:', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Назад', callback_data='back')))
        return
    await state.update_data(checkout_date=message.text)
    await message.answer('Добавьте комментарий:', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Назад', callback_data='back')))
    await BookingState.waiting_for_comment.set()

@dp.message_handler(state=BookingState.waiting_for_comment)
async def add_comment(message: types.Message, state: FSMContext):
    comment = message.text
    async with state.proxy() as data:
        data['comment'] = comment
    await message.answer('Вы забронировали!', reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Перейти к началу', callback_data='client_start')))
    await state.finish()

executor.start_polling(dp, skip_updates=True)