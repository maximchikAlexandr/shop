from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

bot_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
bot_keyboard.add(
    KeyboardButton("Categories"),
    KeyboardButton("Producers"),
    KeyboardButton("Discounts"),
    KeyboardButton("Promocodes"),
    KeyboardButton("Products"),
    KeyboardButton("Show Users cart")
)
