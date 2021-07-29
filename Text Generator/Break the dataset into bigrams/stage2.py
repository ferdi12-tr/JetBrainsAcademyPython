from nltk.tokenize import regexp_tokenize
from nltk import bigrams
import sys


class TxtGenerator:
    def __init__(self, fn):
        self.filename = fn
        with open(self.filename, "r", encoding="utf_8") as file:
            text = file.read()  # type of self.text is str

        self.corpus_text = regexp_tokenize(text, r"[\S]+")
        self.create_bigram()

    def create_bigram(self):
        self.bgrs = list(bigrams(self.corpus_text))
        print(f"Numbers of bigrams: {len(self.bgrs)}")

    def print_bigram(self):
        while True:
            try:
                index = input()
                print(f"Head: {self.bgrs[int(index)][0]}\tTail: {self.bgrs[int(index)][1]}")

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
    generator.print_bigram()