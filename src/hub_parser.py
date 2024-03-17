import datetime

import re
from bs4 import BeautifulSoup
from src.schemas.article import BaseArticle
import aiohttp

from src.utils import get_page


class HubParser:
    def __init__(self, hub: str):
        self.hub = hub

    async def parse(self) -> list[BaseArticle]:
        async with aiohttp.ClientSession(self.hub) as session:
            async with session.get('/') as response:
                html_page = await response.text()
                soup = BeautifulSoup(html_page, "html.parser")

            article_links = set()
            for link in soup.find_all(href=self.__article_link_filter):
                href = link.get("href")
                article_links.add(href)

            result = []

            for article_link in article_links:
                print("--------")
                await self.__process_article_page(article_link=article_link, url_session=session)
                print("--------")

        return result

    def __article_link_filter(self, href):
        return href and not re.compile("comments").search(href) and re.compile(r"(articles\/)\d+").search(href)

    def __is_absolute_link(self, link: str):
        return "http" in link or "https" in link

    async def __process_article_page(
        self,
        article_link: str,
        url_session: aiohttp.ClientSession,
    ) -> BaseArticle:
        absolute_article_link = article_link

        if self.__is_absolute_link(article_link):
            html_page = await get_page(url=article_link)
        else:
            async with url_session.get(article_link) as response:
                html_page = await response.text()
                absolute_article_link = str(response.url)

        soup = BeautifulSoup(html_page, "html.parser")

        headline = soup.find("h1", attrs={"class": "tm-title tm-title_h1"}).find("span").text
        publish_date = soup.find("span", attrs={"class": "tm-article-datetime-published"}).find("time")["datetime"]
        author_link = soup.find("a", attrs={"class": "tm-user-info__username"})
        content = soup.find("div", attrs={"class": "article-formatted-body"}).find("div").get_text()

        author_name = author_link.text.strip()
        author_link = '{}{}'.format(self.hub, author_link["href"])

        result = BaseArticle(
            headline=headline,
            publish_date=datetime.datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%S.%fZ"),
            link=absolute_article_link,
            author=author_name,
            author_link=author_link,
            content=content,
            hub=self.hub
        )

        self.__log_article(article=result)

        return result

    def __log_article(self, article: BaseArticle):
        print("Заголовок:", article.headline)
        print("Дата:", article.publish_date)
        print("Ссылка на пост:", article.link)
        print("Имя автора:", article.author)
        print("Ссылка на автора:", article.author_link)
