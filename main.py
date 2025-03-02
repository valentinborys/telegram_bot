import logging
import os
import telegram
import azure.functions as func
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from handlers import start, rate, news, help_command, get_joke, song
from buttons import button
from config import TOKEN

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_URL = "https://bibizyan.azurewebsites.net/webhook"

application = Application.builder().token(TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("rate", rate))
application.add_handler(CommandHandler("news", news))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("joke", get_joke))
application.add_handler(CommandHandler("song", song))
application.add_handler(CallbackQueryHandler(button))

app = func.FunctionApp()

@app.function_name(name="TelegramWebhook")
@app.route(route="webhook", methods=["POST"])
async def webhook(req: func.HttpRequest) -> func.HttpResponse:
    try:
        update = telegram.Update.de_json(req.get_json(), application.bot)
        await application.update_queue.put(update)
        return func.HttpResponse("OK", status_code=200)
    except Exception as e:
        logger.error(f"Ошибка обработки вебхука: {e}")
        return func.HttpResponse("Ошибка", status_code=500)

async def set_webhook():
    async with Application.builder().token(TOKEN).build() as app:
        await app.bot.set_webhook(url=WEBHOOK_URL)
        print("Webhook установлен!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
