import requests
from bs4 import BeautifulSoup
import string
import os

DMN = "https://www.nature.com"


class HttpRreq:
    def __init__(self, n_pages, type_articles):
        self.url = "https://www.nature.com/nature/articles"
        self.n_page = n_pages
        self.type_article = type_articles
        self.construct_url()

    def construct_url(self):
        for num_p in range(1, self.n_page + 1):
            self.payload = {"searchType": "journalSearch", "sort": "PubDate", "page": "{}".format(str(num_p))}
            r = requests.get(self.url, params=self.payload)

            self.current_path = os.path.join(os.getcwd(), "Page_{}".format(str(num_p)))
            if not os.path.exists(self.current_path):
                os.mkdir(self.current_path)
            self.article_content(r)

    def article_content(self, r):
        self.r = r
        if self.r:
            soup = BeautifulSoup(self.r.content, "html.parser")  # soup of "Browse Article" page
            article = soup.find_all("article", {"class": "u-full-height c-card c-card--flush"})  # get the article of "Browse Article" page
            for i in article:
                if_type = i.find("span", {"class": "c-meta__type"}).text
                if if_type == self.type_article:

                    title = i.find("a", {"data-track-label": "link"}).text.strip()  # get title
                    ttl = title.maketrans(" ", "_", string.punctuation)
                    filename = title.translate(ttl)

                    link = i.find("a").get("href")  # get link but this is tail of actual link e.g: "/articles/d41586-021-01948-2"
                    actual_link = DMN + link
                    new_req = requests.get(actual_link)  # new request for the corresponding link

                    new_soup = BeautifulSoup(new_req.content, "html.parser")
                    body = new_soup.find("div", {"class": "article-item__body"}).text.strip()

                    try:
                        doc_name = os.path.join(self.current_path, "{}.txt".format(filename))
                        with open(doc_name, "wb") as file:
                            file.write(body.encode())
                    except OSError:
                        print("OSError occur")

        else:
            print(self.r.status_code)


if __name__ == "__main__":
    n_page = int(input())  # number of pages that we want to search in
    type_article = input()
    req = HttpRreq(n_page, type_article)