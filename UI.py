from aiogram import types

# подать заявку клава
applyKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard = True)
apply_button = types.KeyboardButton(text="Подать заявку")
applyKeyboard.add(apply_button)

# клава с "Далее"
nextKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
next_button = types.KeyboardButton(text="Далее")
nextKeyboard.add(next_button)

# клава с ошибкой и подать заявку
errorKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
error_button = types.KeyboardButton(text="Подать заявку")
errorKeyboard.add(error_button)

# клава админа
adminKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
admin_button = types.KeyboardButton(text="Заявки на регистрацию")
admin_button2 = types.KeyboardButton(text="Бан")
adminKeyboard.add(admin_button, admin_button2)

#клава main
mainKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
main_button = types.KeyboardButton(text="Правила")
main_button2 = types.KeyboardButton(text="Реф.Ссылка")
mainKeyboard.add(main_button, main_button2)




