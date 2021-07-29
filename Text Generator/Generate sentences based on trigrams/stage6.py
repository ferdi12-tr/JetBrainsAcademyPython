from nltk.tokenize import regexp_tokenize
from nltk.util import trigrams
from collections import Counter
import random


class TxtGenerator:
    def __init__(self, fn):
        self.filename = fn
        with open(self.filename, "r", encoding="utf_8") as file:
            text = file.read()  # type of text is str
        self.build_model(text)

    def build_model(self, text):
        self.text = text
        self.corpus_text = regexp_tokenize(text, r"[\S]+")

        self.trgrm = list(trigrams(self.corpus_text))

        self.create_tail = {}
        self.list_head = []  # for the choosing of head of the chain
        for h_t in self.trgrm:  # h_t refer to head and tail
            head = " ".join(list(h_t[:2]))
            tail = h_t[-1]
            self.create_tail.setdefault(head, []).append(tail)
            if head[0].istitle():  # when choosing first words of sentences
                self.list_head.append(head)

    def create_markov(self, ini):
        self.init = ini
        list_tail = Counter(self.create_tail[self.init]).most_common()
        return list_tail

    def generate_text(self):
        count = 0
        while True:
            init = random.choice(self.list_head)
            # we head must not include punctuation at the end of each word
            if regexp_tokenize(init.split()[0], "[A-Za-z].*?[^.?!]{2}$"):
                sentence = [init]  # create first sentence chain
            else:
                continue

            while True:
                population = []  # store all tails of head
                weight = []  # store repetition of each tail in order to make a good choose
                tail_list = self.create_markov(init)
                for key, value in tail_list:
                    population.append(key)
                    weight.append(value)

                # pseudo-predict, means that choose according to weigh of population
                predict = random.choices(population, weight)
                sentence.append(predict[0])
                sent = " ".join(sentence)  # full sentence
                if regexp_tokenize(sent, r'[A-Za-z].*?[.?!]$'):
                    if len(sent.split()) < 5:  # the sentence must include at least 5 words
                        init = " ".join(sent.split()[-2:])  # the new head must be the last 2 word from sentence
                        continue
                    else:
                        print(" ".join(sentence))
                        count += 1
                        break
                init = " ".join(sent.split()[-2:])  # the new head must be the last 2 word from sentence

            if count == 10:  # check that if we reach 10 pseudo-sentence or not
                break


if __name__ == "__main__":
    filename = input()
    generator = TxtGenerator(filename)
    generator.generate_text()