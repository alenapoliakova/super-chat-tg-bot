import telebot
import logging
import coloredlogs

from parsing_habr import parse_habr
from check_env import BOT_TOKEN, BOT_NAME


logging.basicConfig(
    level=logging.NOTSET,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(filename="../bot.log")],
    datefmt="%Y-%m-%d %H:%M:%S"
)
coloredlogs.install()

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")
logging.info(f"BOT {BOT_NAME} STARTED")


@bot.message_handler(content_types=["new_chat_members"])
def answer_to_a_new_member(message):
    logging.info(f"ADD USER {message.from_user.username}")
    if name := message.from_user.first_name:
        bot.reply_to(message, f"Привет, {name}, добро пожаловать в наш чат!")
    else:
        bot.reply_to(message, f"Привет, добро пожаловать в наш чат!")


@bot.message_handler(content_types=["text"], commands=["random_habr"])
def send_random_article_from_habr(message):
    """Отправить пользователю рандомную статью из топа за день на Хабре"""
    logging.info(f"RECV {message.text} FROM {message.from_user.username}")
    habr_article = parse_habr()
    bot.reply_to(message, f"_{habr_article.title}_\n\nСсылка: [клик]({habr_article.url})")


bot.polling(none_stop=True)
