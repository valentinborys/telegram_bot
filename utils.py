from datetime import *
import os
import requests
from bs4 import BeautifulSoup
from telegram import Update

from config import NEWS_URL, HEADERS


def get_exchange_rate():
    url = "https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=5"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        usd = next((item for item in data if item["ccy"] == "USD"), None)
        eur = next((item for item in data if item["ccy"] == "EUR"), None)

        if usd and eur:
            usd_buy = str(float(usd['buy'])).rstrip('0').rstrip('.')
            usd_sale = str(float(usd['sale'])).rstrip('0').rstrip('.')
            eur_buy = str(float(eur['buy'])).rstrip('0').rstrip('.')
            eur_sale = str(float(eur['sale'])).rstrip('0').rstrip('.')

            return (f"💵 1 USD: {usd_buy} / {usd_sale} UAH\n"
                    f"💶 1 EUR: {eur_buy} / {eur_sale} UAH")
        else:
            return "Не вдалося знайти курс валют для USD або EUR"

    except requests.exceptions.RequestException as e:
        return f"Помилка при запиті до API: {e}. Спробуйте пізніше"
    except ValueError:
        return "Помилка при обробці відповіді сервера. Спробуйте пізніше"

def get_monkey_images(image_folder="images"):
    images = [f for f in os.listdir(image_folder) if f.endswith((".jpg", ".jpeg", ".png"))]
    return images

def get_news():
    response = requests.get(NEWS_URL, headers=HEADERS)

    if response.status_code != 200:
        return "Помилка при отриманні новин 😔"

    soup = BeautifulSoup(response.text, 'html.parser')

    headlines = soup.select(".c-card__link")[:4]

    if not headlines:
        return "Не вийшло отримати новини 😔"

    time_now = datetime.now().strftime("%H:%M:%S")
    news_list = [f"🍌{h.text.strip()}\n {h['href']}" for h in headlines]
    return f"Останні новини на {time_now}:\n\n" + "\n\n".join(news_list)
