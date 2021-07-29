import requests
from bs4 import BeautifulSoup
import string


DMN = "https://www.nature.com"


class HttpRreq:
    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url)

    def news_content(self):
        if self.r:
            soup = BeautifulSoup(self.r.content, "html.parser")
            article = soup.find_all("article", {"class": "u-full-height c-card c-card--flush"})
            for i in article:
                if_news = i.find("span", {"class": "c-meta__type"}).text
                if if_news == "News":

                    title = i.find("a", {"data-track-label": "link"}).text.strip()
                    ttl = title.maketrans(" ", "_", string.punctuation)
                    filename = title.translate(ttl)

                    link = i.find("a").get("href")
                    actual_link = DMN + link
                    new_req = requests.get(actual_link)

                    new_soup = BeautifulSoup(new_req.content, "html.parser")
                    body = new_soup.find("div", {"class": "c-article-body u-clearfix"}).text.strip()

                    with open(f"{filename}.txt", "wb") as file:
                        file.write(body.encode())
        else:
            print(self.r.status_code)


if __name__ == "__main__":
    url_ = "https://www.nature.com/nature/articles"
    req = HttpRreq(url_)
    req.news_content()
