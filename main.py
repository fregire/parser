import requests
from bs4 import BeautifulSoup
import re

HUB_URL = 'https://habr.com'

def article_link_filter(href):
    return href and not re.compile("comments").search(href) and re.compile("articles").search(href
                                                                                            )
def main():
    response = requests.get(HUB_URL)
    html_page = response.text
    soup = BeautifulSoup(html_page, "html.parser")

    article_links = set()
    for link in soup.find_all(href=article_link_filter):
        href = link.get("href")
        absolute_url = '{}{}'.format(HUB_URL, href)
        article_links.add(absolute_url)

    for article_link in article_links:
        response = requests.get(article_link)
        html_page = response.text
        soup = BeautifulSoup(html_page, "html.parser")

        headline = soup.find("h1", attrs={"class": "tm-title tm-title_h1"}).find("span").text
        publish_date = soup.find("span", attrs={"class": "tm-article-datetime-published"}).find("time")["datetime"]
        author_link = soup.find("a", attrs={"class": "tm-user-info__username"})
        author_name = author_link.text.strip()
        author_link = '{}{}'.format(HUB_URL, author_link["href"])
        print("--------")
        print("Заголовок:", headline)
        print("Дата:", publish_date)
        print("Ссылка на пост:", article_link)
        print("Имя автора:", author_name)
        print("Ссылка на пост:", author_link)
        print("--------")



if __name__ == '__main__':
    main()


