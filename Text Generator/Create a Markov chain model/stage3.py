from nltk.tokenize import regexp_tokenize
from nltk import bigrams
from collections import Counter
import sys


class TxtGenerator:
    def __init__(self, fn):
        self.filename = fn
        with open(self.filename, "r", encoding="utf_8") as file:
            text = file.read()  # type of text is str

        self.corpus_text = regexp_tokenize(text, r"[\S]+")
        self.bgrs = list(bigrams(self.corpus_text))

    def create_markov(self):
        try:
            count_tail = {}
            for head, tail in self.bgrs:
                count_tail.setdefault(head, []).append(tail)

            list_tail = Counter(count_tail[self.index]).most_common()
            return list_tail
        except KeyError:  # if input not in the head then print key error
            print("The requested word is not in the model. Please input another word.")

    def print_markov(self):
        while True:
            try:
                self.index = input()
                if self.index == "exit":
                    sys.exit()
                else:
                    tail_list = self.create_markov()
                    print(f"Head: {self.index}")
                    for tail in tail_list:
                        print(f"Tail: {tail[0]}\tCount: {tail[1]}")

            except ValueError:
                print("Type Error. Please input an integer.")
            except IndexError:
                print("Index Error. Please input an integer that is in the range of the corpus.")
            except TypeError:
                continue


if __name__ == "__main__":
    filename = input()
    generator = TxtGenerator(filename)
    generator.print_markov()
