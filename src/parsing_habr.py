import json
import random
from collections import namedtuple
from time import strftime

import requests
from bs4 import BeautifulSoup


article = namedtuple("arcticle", ["title", "url"])

harb_url = "https://habr.com/ru/top/daily/"
resp = requests.get(harb_url).text
soup = BeautifulSoup(resp, "html.parser")


def parse_habr() -> article:
    today = strftime("%Y-%m-%d")
    file = open("habr_data.json", "r+")

    try:
        data = json.load(file)
    except json.JSONDecodeError:
        data = {}

    if articles_for_today := data.get(today):
        habr_article = article(*random.choice(articles_for_today))
        file.close()
        return habr_article
    else:
        file = open("habr_data.json", "w")  # Чтобы очистить файл
        all_found_articles = []

        for data in soup.find_all("a", {"class": "tm-article-snippet__title-link"}):
            url = f"https://habr.com{data['href']}"
            header = data.text
            all_found_articles.append([u"{}".format(header), url])

        json.dump({today: all_found_articles}, file, indent=2, ensure_ascii=False)

        file.close()
        habr_article = article(*random.choice(all_found_articles))
        return habr_article
