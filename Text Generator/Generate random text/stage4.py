from nltk.tokenize import regexp_tokenize
from nltk import bigrams
from collections import Counter
import random
import sys


class TxtGenerator:
    def __init__(self, fn):
        self.filename = fn
        with open(self.filename, "r", encoding="utf_8") as file:
            text = file.read()  # type of text is str

        self.corpus_text = regexp_tokenize(text, r"[\S]+")
        self.bgrs = list(bigrams(self.corpus_text))

        self.count_tail = {}
        for head, tail in self.bgrs:
            self.count_tail.setdefault(head, []).append(tail)

    def create_markov(self, ini):
        self.init = ini
        list_tail = Counter(self.count_tail[self.init]).most_common()
        return list_tail

    def generate_text(self):
        for _ in range(0,10):
            init = random.choice(self.corpus_text)
            sentence = [init]
            for _ in range(0,9):
                population = []
                weight = []
                tail_list = self.create_markov(init)
                for key, value in tail_list:
                    population.append(key)
                    weight.append(value)
                predict = random.choices(population, weight)
                sentence.append(predict[0])
                init = predict[0]
            print(" ".join(sentence))

if __name__ == "__main__":
    filename = input()
    generator = TxtGenerator(filename)
    generator.generate_text()