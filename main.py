from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
import logging


import db
from db import Database
import UI
TOKEN = 'TOKEN'

bot = Bot(token=TOKEN)


api_id = 123456789
api_hash = "API_HASH"

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

bot = Bot(token=TOKEN)

class Form(StatesGroup):
    helloState = State()
    submitErrorState = State()
    applyState = State()
    experienceState = State()
    finalState = State()
    registeredState = State()
    adminPanel = State()

db = Database('userdatabase.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    if db.user_exists(message.from_user.username):
        state = dp.current_state(user=message.from_user.id)
        print("Registered!")
        await state.set_state(Form.registeredState)
    if not db.user_exists(message.from_user.username):
        try:
            await bot.send_message(message.chat.id, "Привет! Добро пожаловать! Для начала, подайте заявку.", reply_markup=UI.applyKeyboard)
            state = dp.current_state(user=message.from_user.id)
            print("Not Registered!")
            await state.set_state(Form.applyState)
        except Exception as e:
            await bot.send_message(message.chat.id, "Ошибка!")
            await start()

@dp.message_handler(lambda message: message.text == "Подать заявку", state=Form.applyState)
async def applyStep(message: types.Message, state: FSMContext):
    try:
        state = dp.current_state(user=message.from_user.id)
        print(state)
        await state.set_state(Form.experienceState)
        await bot.send_message(message.chat.id, "Отлично! Нажмите 'Далее'", reply_markup=UI.nextKeyboard)
    except Exception as e:
        print("Error!")


@dp.message_handler(lambda message: message.text != "Подать заявку", state=Form.applyState)
async def errorStep(message: types.Message, state: FSMContext):
    try:
        print(state)
        await state.set_state(Form.applyState)
        await message.reply("Пожалуйста, используйте кнопку" + " 'подать заявку'", reply_markup=UI.errorKeyboard)
    except Exception as e:
        print("Error!")

@dp.message_handler(state=Form.experienceState)
async def experience(message: types.Message, state: FSMContext):
    try:
        db.add_user(message.from_user.username)
        print(logging.info("mes "), logging.debug("msg"))
        await bot.send_message(message.chat.id, "Пожалуйста, расскажите о своем опыте в нашей сфере работы.")
        state = dp.current_state(user=message.from_user.id)
        print(state)
        await state.set_state(Form.finalState)
        db.set_experience(message.text, message.from_user.username)
    except Exception as e:
        await bot.send_message(message.chat.id, "Ошибка!")
        print(e)

@dp.message_handler(state=Form.finalState)
async def final(message: types.Message, state: FSMContext):
    try:
        if db.get_signup(message.from_user.username) == "notapproved":
            await bot.send_message(message.chat.id, "Ваша заявка на рассмотрении! Ожидайте...")
            print(db.get_signup(message.from_user.username))
        elif db.get_signup(message.from_user.username) == "approved":
            await bot.send_message(message.chat.id, "Поздравляем! Вы были приняты", reply_markup=UI.mainKeyboard)
            state = dp.current_state(user=message.from_user.id)
            print(db.get_signup(message.from_user.username))
            await state.set_state(Form.registeredState)
    except Exception as e:
        await bot.send_message(message.chat.id, "Ошибка!")

@dp.message_handler(state=Form.registeredState)
async def registered(message: types.Message, state: FSMContext):
    if message.text == "/start":
        await bot.send_message(message.chat.id, "Главное меню", reply_markup=UI.mainKeyboard)

    if message.text == "doradoora":
        await bot.send_message(message.chat.id, "@" + message.from_user.username + " попытка зайти в админ-панель...")
        if db.get_admin(message.from_user.username) == "YES":
            state = dp.current_state(user=message.from_user.id)
            print(state)
            await bot.send_message(message.chat.id, "Добро пожаловать в админ панель! Что нужно сделать?",
                                   reply_markup=UI.adminKeyboard)
            await state.set_state(Form.adminPanel)
            print(message.from_user.username, " Зашел в админ панель!")

            # await state.set_state(Form.adminPanel)
        if db.get_admin(message.from_user.username) == "NO":
            await bot.send_message(message.chat.id, "Вы не админ!")

@dp.message_handler(state=Form.adminPanel)
async def admin_panel(message: types.Message, state: FSMContext):
    if message.text == "Заявки на регистрацию":
        print("заявки на руге")
        await bot.send_message(message.chat.id, f"Список заявок: \n {db.get_applications()} ")
    if message.text == "Бан":
        pass
    # show menu

# подтверждение заявок через админ панель
# бан через админ панель
#

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


