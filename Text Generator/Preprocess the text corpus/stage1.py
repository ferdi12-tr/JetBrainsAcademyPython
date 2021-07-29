from nltk.tokenize import regexp_tokenize
from nltk import FreqDist
import sys


class TxtGenerator:
    def __init__(self, fn):
        self.filename = fn
        with open(self.filename, "r", encoding="utf_8") as file:
            text = file.read()  # type of self.text is str

        self.corpus_text = regexp_tokenize(text, r"[\S]+")
        self.count_token()

    def count_token(self):
        num_unique = FreqDist(self.corpus_text).B()  # for the number of unique sample values
        num_total = FreqDist(self.corpus_text).N()  # for the number of total tokens
        print(f"Corpus statistics\nAll tokens: {num_total}\nUnique tokens: {num_unique}")

    def print_token(self):
        while True:
            try:
                index = input()
                print(self.corpus_text[int(index)])

            except ValueError:
                if index == "exit":
                    sys.exit()
                else:
                    print("Type Error. Please input an integer.")

            except IndexError:
                print("Index Error. Please input an integer that is in the range of the corpus.")


if __name__ == "__main__":
    filename = input()
    generator = TxtGenerator(filename)
    generator.print_token()