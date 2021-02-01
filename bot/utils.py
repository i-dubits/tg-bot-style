
from aiogram.dispatcher.filters.state import State, StatesGroup

class Nst(StatesGroup):
    waiting_for_content_image = State()
    waiting_for_style_image = State()
    waiting_for_result = State()

class Cycle(StatesGroup):
    waiting_for_content_image = State()
    waiting_for_result = State()





