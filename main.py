import logging
from telegram.ext import Application, CommandHandler
from handlers import *
from config import TOKEN
from telegram.ext import CallbackQueryHandler
from buttons import button

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("rate", rate))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("joke", get_joke))

    application.add_handler(CallbackQueryHandler(button))

    print("Бот працює...")
    application.run_polling()


if __name__ == "__main__":
    main()
