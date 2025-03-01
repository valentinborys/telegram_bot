import os
import random
from config import *
import requests
from telegram.ext import CallbackContext
from utils import get_exchange_rate, get_monkey_images, get_news
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

# /start
async def start(update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Курс валют 💸", callback_data='exchange_rate')],
        [InlineKeyboardButton("Новини 🗞", callback_data='news')],
        [InlineKeyboardButton("Бібізян Дімасік 🙈", callback_data='monkey_images')],
        [InlineKeyboardButton("Анекдоти від бібзяна 😂", callback_data='joke')],
        [InlineKeyboardButton("Пісня для бібізян 🐒", callback_data='song')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с клавиатурой
    await update.message.reply_text(
        "Привіт, бібізян!!! Шо там, цікаво шо по курсу грн? 💰\nВибери одну з опцій нижче ⬇️:",
        reply_markup=reply_markup
    )

# /rate
async def rate(update: Update, context: CallbackContext):

    exchange_rate = get_exchange_rate()
    await update.message.reply_text(exchange_rate)

    monkey_images = get_monkey_images()

    if monkey_images:
        image_path = os.path.join("images", random.choice(monkey_images))
        await update.message.reply_photo(photo=open(image_path, "rb"),
                                         caption="Тримай бібізянку та актуальний курс нашої потужної! 🐵")
    else:
        await update.message.reply_text("Сорі, немає доступних картинок бібізянки! 😔")

# /news
async def news(update: Update, context: CallbackContext):
    news_text = get_news()

    if not news_text.strip():
        news_text = "Сорян, бібізянка не нашла новостей 😔"

    await update.message.reply_text(news_text)

# /help
async def help_command(update, context: CallbackContext):
    help_text = (
        "Ось усі доступні команди ⬇️:\n"
        "/start - Привітальне повідомлення\n"
        "/rate - Отримати актуальний курс валют\n"
        "/news - Отримати останні новини\n"
        "/joke - Анекдоти"
    )
    await update.message.reply_text(help_text)


# /joke
async def get_joke(update: Update, context):
    response = requests.get(JOKE_API_URL)

    if response.status_code == 200:
        joke_text = response.text.strip()
    else:
        joke_text = "Не вийшло отримити анекдот 😔"

    await update.message.reply_text(joke_text)


# /song
async def song(update: Update, context: CallbackContext):
    await send_video_link(update)


async def send_video_link(update: Update):
    youtube_video_url = "https://www.youtube.com/watch?v=_aJZMR8vJXU&ab_channel=%D0%9A%D1%83%D1%80%D0%B3%D0%B0%D0%BD-Topic"
    await update.message.reply_text(f"Приємн видео о бібізянах: 🐒\n{youtube_video_url}")



def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Курс валют 💸", callback_data='exchange_rate')],
        [InlineKeyboardButton("Новини 🗞", callback_data='news')],
        [InlineKeyboardButton("Бібізян Дімасік 🙈", callback_data='monkey_images')],
        [InlineKeyboardButton("Анекдоти від бібізяна 😂", callback_data='joke')],
        [InlineKeyboardButton("Пісня для бібізян 🐒", callback_data='song')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard():
    keyboard = [
        [InlineKeyboardButton("Назад ⬅️", callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)