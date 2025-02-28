import os
import random
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler
from bs4 import BeautifulSoup


TOKEN = "7886697117:AAEHySBWJww2_R24RLf_dxo33qYdAugbwUk"

IMAGE_FOLDER = "images"


def get_exchange_rate():
    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=5"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        usd = next(item for item in data if item["ccy"] == "USD")
        eur = next(item for item in data if item["ccy"] == "EUR")
        return f"💵 1 USD = {usd['sale']} UAH\n💶 1 EUR = {eur['sale']} UAH"
    else:
        return "Помилка, бібізянчик не сумуй, спробуй трохи пізніше ще раз 😔"


async def start(update: Update, context):
    await update.message.reply_text(
        "Привіт, бібізян! Шо там, цікаво шо там по курсу грн? 💰\nТицяй на /rate, дам актуальний курс (за банан) 🍌🍌🍌."
    )


def get_monkey_images():
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith((".jpg", ".jpeg", ".png"))]
    return images


async def rate(update: Update, context):
    exchange_rate = get_exchange_rate()
    await update.message.reply_text(exchange_rate)

    monkey_images = get_monkey_images()

    if monkey_images:
        image_path = os.path.join(IMAGE_FOLDER, random.choice(monkey_images))

        await update.message.reply_photo(photo=open(image_path, "rb"), caption="Тримай бібізянку та актуальний курс нашої потужної! 🐵")
    else:
        await update.message.reply_text("Сорі, немає доступних картинок бібізянки! 😔")


NEWS_URL = "https://www.epravda.com.ua/news/"


def get_news():
    response = requests.get(NEWS_URL)
    if response.status_code != 200:
        return "Ошибка при получении новостей 😔"

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.select(".article_header a")[:5]  # Берем первые 5 заголовков

    news_list = [f"📰 {h.text.strip()}\nhttps://www.epravda.com.ua{h['href']}" for h in headlines]
    print(news_list)
    return "\n\n".join(news_list)


async def news(update: Update, context):
    news_text = get_news()
    await update.message.reply_text(news_text)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rate", rate))
    app.add_handler(CommandHandler("news", news))

    print("Бот запущений...")
    app.run_polling()


if __name__ == "__main__":
    main()
