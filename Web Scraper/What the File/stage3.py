import requests


class HttpRreq:
    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url)

    def quote_content(self):

        if self.r:
            page_content = self.r.content
            with open("source.html", "wb") as file:
                file.write(page_content)
            print("Content saved.")
        else:
            print(f"The URL returned {self.r.status_code}")


if __name__ == "__main__":
    print("Input the URL:")
    url_ = input()
    req = HttpRreq(url_)
    req.quote_content()