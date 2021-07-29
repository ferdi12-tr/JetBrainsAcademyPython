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
        self.build_model(text)

    def build_model(self, text):
        self.text = text
        self.corpus_text = regexp_tokenize(text, r"[\S]+")

        self.list_upperword = []
        for word in self.corpus_text:  # to find words that has capital character at the very beginning
                if word[0].isupper():
                    self.list_upperword.append(word)

        self.bgrs = list(bigrams(self.corpus_text))

        self.create_tail = {}
        for head, tail in self.bgrs:
            self.create_tail.setdefault(head, []).append(tail)

    def create_markov(self, ini):
        self.init = ini
        list_tail = Counter(self.create_tail[self.init]).most_common()
        return list_tail

    def generate_text(self):
        for _ in range(0,10):
            while True:

                init = random.choice(self.list_upperword)  # choose random word amongst list_upper that we create for quick choosing
                if regexp_tokenize(init, "[A-Z].*?[^.?!]$"):  # check if sentence starts with capitalized word or not
                    sentence = [init]

                    population = []
                    weight = []
                    tail_list = self.create_markov(init)
                    for key, value in tail_list:
                        population.append(key)
                        weight.append(value)

                    chc = False  # if our words haven't punctuations, it probably falls into an infinitive loop
                    for pop in population:
                        if regexp_tokenize(pop, "[.?!]$"):
                            chc = True
                    if chc == False:
                        continue

                    while True:
                        predict = random.choices(population, weight)
                        sentence.append(predict[0])
                        if regexp_tokenize(" ".join(sentence), r'[A-Za-z].*?[.?!]$'):
                            if len(sentence) < 5:
                                continue
                            else:
                                print(" ".join(sentence))
                                break
                    break
                else:
                    continue
                    

if __name__ == "__main__":
    filename = input()
    generator = TxtGenerator(filename)
    generator.generate_text()