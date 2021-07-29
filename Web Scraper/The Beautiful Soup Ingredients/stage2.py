import requests
from bs4 import BeautifulSoup

IMDB_HOST = 'www.imdb.com'


class HttpRreq:
    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url, headers={'Accept-Language': 'en-US,en;q=0.5'})

    def quote_content(self):
        is_valid = IMDB_HOST in self.url
        if is_valid:
            try:
                if self.r:
                    soup = BeautifulSoup(self.r.content, "html.parser")

                    desc = soup.find('span', {"data-testid": "plot-xl", "role": "presentation"})
                    title = soup.find("title")
                    dic = {"title":title.text, "description":desc.text}
                    print(dic)
            except AttributeError:
                print("Invalid movie page!")
        else:
            print("Invalid movie page!")


if __name__ == "__main__":
    print("Input the URL:")
    url_ = input()
    req = HttpRreq(url_)
    req.quote_content()