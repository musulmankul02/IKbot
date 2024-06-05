from aiogram.dispatcher.filters.state import State, StatesGroup
# Определение состояний

class BookingState(StatesGroup):
    waiting_for_city = State()
    waiting_for_date = State()
    waiting_for_comment = State()
    waiting_for_number_of_people = State()  # Добавлено новое состояние
    waiting_for_distance_to_beach = State()  # Новое состояние для расстояния до пляжа
    waiting_for_phone_number = State()  # Новое состояние для номера телефона

class ProfileCreationState(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_phone = State()
    waiting_for_age = State()

class EditProfileState(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
    waiting_for_phone = State()
    waiting_for_age = State()