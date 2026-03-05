import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    exit("Ошибка: Вы забыли указать BOT_TOKEN в файле .env!")
