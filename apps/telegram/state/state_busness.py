from aiogram.dispatcher.filters.state import State, StatesGroup

class HotelInfo(StatesGroup):
    waiting_for_hotel_name = State()
    waiting_for_hotel_address = State()
    waiting_for_hotel_phone = State()
    waiting_for_hotel_description = State()
    waiting_for_allocation_type = State()
    waiting_for_places = State()
    waiting_for_facilities = State()
    waiting_for_distance = State()
    waiting_for_price = State()
    waiting_for_photos = State()
    waiting_for_confirmation = State()
