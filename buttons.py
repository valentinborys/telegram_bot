import os
import random
import requests
from telegram import Update
from telegram.ext import CallbackContext
from config import JOKE_API_URL
from handlers import get_back_keyboard, get_main_keyboard
from utils import get_exchange_rate, get_monkey_images, get_news


async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'back':
        await query.message.delete()

        await query.message.reply_text(
            "Привіт, бібізян!!! Шо там, цікаво шо по курсу грн? 💰\nВибери одну з опцій нижче ⬇️",
            reply_markup=get_main_keyboard()
        )

    elif query.data == 'exchange_rate':
        exchange_rate = get_exchange_rate()

        await query.message.delete()

        monkey_images = get_monkey_images()
        if monkey_images:
            image_path = os.path.join("images", random.choice(monkey_images))
            await query.message.reply_photo(photo=open(image_path, "rb"),
                                            caption=f"{exchange_rate}\n\nТримай бібізянку та актуальний курс нашої потужної! 🐵🐵🐵",
                                            reply_markup=get_back_keyboard())
        else:
            await query.message.reply_text("Сорі, немає доступних картинок бібізянки! 😔", reply_markup=get_back_keyboard())
            await query.message.reply_text(exchange_rate, reply_markup=get_back_keyboard())

    elif query.data == 'news':
        news_text = get_news()
        if not news_text.strip():
            news_text = "Сорян, бібізянка не знайшла новин 😔"

        await query.message.delete()

        await query.message.reply_text(text=news_text, reply_markup=get_back_keyboard())

    elif query.data == 'monkey_images':
        monkey_images = get_monkey_images()

        await query.message.delete()

        if monkey_images:
            image_path = os.path.join("images", random.choice(monkey_images))
            await query.message.reply_photo(photo=open(image_path, "rb"),
                                            caption="Тримай бібізянку! У-АА! Сьогодні він дууже веселий!! 🐵🙊",
                                            reply_markup=get_back_keyboard())
        else:
            await query.message.reply_text("Сорі, немає доступних картинок бібізянки! 😔", reply_markup=get_back_keyboard())

    elif query.data == 'joke':
        response = requests.get(JOKE_API_URL)
        if response.status_code == 200:
            joke_text = response.text.strip()
        else:
            joke_text = "Не удалось получить анекдот 😔"

        await query.message.delete()

        await query.message.reply_text(text=joke_text, reply_markup=get_back_keyboard())
