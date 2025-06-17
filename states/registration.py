from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    choosing_role = State()
    entering_name = State()
    confirming = State()
