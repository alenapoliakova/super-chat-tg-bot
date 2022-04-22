import telebot
import requests
import logging
import coloredlogs
from bs4 import BeautifulSoup

from parsing_habr import parse_habr
from check_env import BOT_TOKEN, BOT_NAME


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(filename="../bot.log")],
    datefmt="%Y-%m-%d %H:%M:%S"
)
coloredlogs.install()


url = "https://habr.com/ru/top/daily/"
resp = requests.get(url).text
soup = BeautifulSoup(resp, "html.parser")

bot = telebot.TeleBot(BOT_TOKEN)
logging.info(f"BOT {BOT_NAME} STARTED")


@bot.message_handler(content_types=["new_chat_members"])
def answer_to_a_new_member(message):
    bot.reply_to(message, f"Привет, {message.from_user.first_name}, добро пожаловать в наш чат!\n\n")


@bot.message_handler(commands=["/random_habr"])
def send_random_article_from_habr(message):
    """Отправить пользователю рандомную статью из топа за день на Хабре"""
    habr_article = parse_habr()
    bot.reply_to(message.chat.id, f"<b>Статья</b> {habr_article.title}\n\n"
                                  f"Ссылка на статью: <a href='{habr_article.url}'>Клик</a>")


bot.polling(none_stop=True)
