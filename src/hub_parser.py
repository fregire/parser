import datetime

import requests
import re
from bs4 import BeautifulSoup
from src.schemas.article import BaseArticle


class HubParser:
    def __init__(self, hub: str):
        self.hub = hub

    def __article_link_filter(self, href):
        return href and not re.compile("comments").search(href) and re.compile("articles").search(href)

    def parse(self) -> list[BaseArticle]:
        response = requests.get(self.hub)
        html_page = response.text
        soup = BeautifulSoup(html_page, "html.parser")

        article_links = set()
        for link in soup.find_all(href=self.__article_link_filter):
            href = link.get("href")
            absolute_url = '{}{}'.format(self.hub, href)
            article_links.add(absolute_url)

        result = []

        for article_link in article_links:
            response = requests.get(article_link)
            html_page = response.text
            soup = BeautifulSoup(html_page, "html.parser")

            headline = soup.find("h1", attrs={"class": "tm-title tm-title_h1"}).find("span").text
            publish_date = soup.find("span", attrs={"class": "tm-article-datetime-published"}).find("time")["datetime"]
            author_link = soup.find("a", attrs={"class": "tm-user-info__username"})
            content = soup.find("div", attrs={"class": "article-formatted-body"}).find("div").get_text()

            author_name = author_link.text.strip()
            author_link = '{}{}'.format(self.hub, author_link["href"])

            result.append(
                BaseArticle(
                    headline=headline,
                    publish_date=datetime.datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%S.%fZ"),
                    link=article_link,
                    author=author_name,
                    author_link=author_link,
                    content=content,
                    hub=self.hub
                )
            )

            print("--------")
            print("Заголовок:", headline)
            print("Дата:", publish_date)
            print("Ссылка на пост:", article_link)
            print("Имя автора:", author_name)
            print("Ссылка на автора:", author_link)
            print("--------")

        return result

