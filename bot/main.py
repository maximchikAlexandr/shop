import logging

import requests
from aiogram import Bot, Dispatcher, types
from django.conf import settings
from django.contrib.auth.hashers import make_password

from bot.keyboard import bot_keyboard
from bot.utils import get_data_from_api, get_user_by_chat_id

logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
COUNT_OBJS = 5


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Input some message", reply_markup=bot_keyboard)


@dp.message_handler(lambda message: message.text == "Categories")
async def cmd_get_categories(msg: types.Message):
    categories = get_data_from_api("api/catalog/catigories")
    msg_to_answer = ""
    for cat in categories[:COUNT_OBJS]:
        msg_to_answer += (
            f"Category: {cat['name']}\n"
            f"Description: {cat['description']}\n"
            f"-----------------------\n"
        )
    await bot.send_message(msg.chat.id, msg_to_answer)


@dp.message_handler(lambda message: message.text == "Producers")
async def cmd_get_producers(msg: types.Message):
    producers = get_data_from_api("api/catalog/producers")
    msg_to_answer = ""
    for producer in producers[:COUNT_OBJS]:
        msg_to_answer += (
            f"Producer: {producer['name']}\n"
            f"Country: {producer['country']}\n"
            f"-----------------------\n"
        )
    await bot.send_message(msg.chat.id, msg_to_answer)


@dp.message_handler(lambda message: message.text == "Discounts")
async def cmd_get_discounts(msg: types.Message):
    discounts = get_data_from_api("api/catalog/discounts")
    msg_to_answer = ""
    for discount in discounts[:COUNT_OBJS]:
        msg_to_answer += (
            f"Producer: {discount['name']}\n"
            f"Percent: {discount['percent']}\n"
            f"-----------------------\n"
        )
    await bot.send_message(msg.chat.id, msg_to_answer)


@dp.message_handler(lambda message: message.text == "Promocodes")
async def cmd_get_promocodes(msg: types.Message):
    promocodes = get_data_from_api("api/catalog/promocodes")
    msg_to_answer = ""
    for promocode in promocodes[:COUNT_OBJS]:
        msg_to_answer += (
            f"Producer: {promocode['name']}\n"
            f"Percent: {promocode['percent']}\n"
            f"-----------------------\n"
        )
    await bot.send_message(msg.chat.id, msg_to_answer)


@dp.message_handler(lambda message: message.text == "Products")
async def cmd_get_products(msg: types.Message):
    products = get_data_from_api("api/catalog/products")
    msg_to_answer = ""
    for product in products[:COUNT_OBJS]:
        msg_to_answer += (
            f"Product: {product['name']}\n"
            f"Price: {product['price']}\n"
            f"-----------------------\n"
        )
    await bot.send_message(msg.chat.id, msg_to_answer)


@dp.message_handler(lambda message: message.text == "Show Users cart")
async def cmd_get_users_cart(message: types.Message):
    try:
        user = await get_user_by_chat_id(tg_chat_id=message.chat.id)
        if user is not None:
            await bot.send_message(message.chat.id, f"User is exist: {user}")
        else:
            await bot.send_message(message.chat.id, f"User is not exist")
    except Exception as e:
        await bot.send_message(message.chat.id, f"{type(e).__name__} - {e}")


@dp.message_handler(commands=["chatid"])
async def cmd_get_chat_id(message: types.Message):
    await bot.send_message(
        message.chat.id, f"Your telegram chat id:\n{message.chat.id}"
    )


@dp.message_handler()
async def query_telegram(message: types.Message):
    await bot.send_message(message.chat.id, "Understandable, have a nice day")
