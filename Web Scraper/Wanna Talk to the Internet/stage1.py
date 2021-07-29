import requests


class HttpRreq:
    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url)

    def quote_content(self):
        if self.r:
            try:
                print(self.r.json()["content"])
            except KeyError:
                print("Invalid quote resource!")
        else:
            print("Invalid quote resource!")


if __name__ == "__main__":
    print("Input the URL:")
    url_ = input()
    req = HttpRreq(url_)
    req.quote_content()