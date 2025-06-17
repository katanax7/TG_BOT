from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.registration import Registration

from database.db import add_user


router = Router()

roles_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Соискатель")],
        [KeyboardButton(text="Работодатель")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "/start")
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Выбери свою роль:", reply_markup=roles_kb)
    await state.set_state(Registration.choosing_role)

@router.message(Registration.choosing_role)
async def choose_role(message: Message, state: FSMContext):
    role = message.text
    if role not in ["Соискатель", "Работодатель"]:
        await message.answer("Пожалуйста, выбери роль с кнопки.")
        return
    await state.update_data(role=role)
    await message.answer("Введи своё имя:")
    await state.set_state(Registration.entering_name)

@router.message(Registration.entering_name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(
        f"Ты выбрал(а):\nРоль: {data['role']}\nИмя: {data['name']}\n\nПодтверди /confirm или отмени /cancel"
    )
    await state.set_state(Registration.confirming)

@router.message(F.text == "/confirm", Registration.confirming)
async def confirm_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    # тут будет сохранение в БД
    add_user(
        telegram_id=message.from_user.id,
        name=data["name"],
        role=data["role"]
    )

    await message.answer("Регистрация завершена! 🎉", reply_markup=None)
    await state.clear()

@router.message(F.text == "/cancel")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Регистрация отменена.", reply_markup=None)
