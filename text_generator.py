from nltk.tokenize import WhitespaceTokenizer
from collections import defaultdict, Counter
import random
import re


class TextGenerator:
    def __init__(self):
        self.tokens = []
        self.trigrams = []
        self.chain_model = {}


def tokenize():
    with open("corpus.txt", encoding="utf-8") as f:
        corpus_data = f.read()
    tokenizer = WhitespaceTokenizer()
    return tokenizer.tokenize(corpus_data)


def trigrams_maker(tokens):
    trigrams = []
    for word in range(len(tokens) - 2):
        trigrams.append([tokens[word] + " " + tokens[word+1], tokens[word+2]])
    trigrams_dict = defaultdict(list)
    for head, tail in trigrams:
        trigrams_dict[head].append(tail)
    a = {key: dict(Counter(value)) for key, value in trigrams_dict.items()}
    return a


def sentence_combiner(trigrams):
    sentences = 40
    while sentences > 0:
        a = generating_sentence(trigrams)
        while a is None:
            a = generating_sentence(trigrams)
        sentences -= 1
        a = ' '.join(a)
        print(a)


def generating_sentence(model):
    counter = 0
    sentence = []
    first = first_word(model)
    sentence.append(first)
    current_head = first
    while len(sentence) < 4:
        next_word = random.choice(list(model[current_head].keys()))
        while not re.match(r"^[a-z].*[\w,]$", next_word):
            next_word = random.choice(list(model[current_head].keys()))
            counter += 1
            if counter == 5:
                return None
        sentence.append(next_word)
        current_head = current_head.split()[1] + " " + next_word
    while len(sentence) < 10:
        next_word = random.choice(list(model[current_head].keys()))
        sentence.append(next_word)
        if next_word.endswith((".", "!", "?")):
            return sentence
        current_head = current_head.split()[1] + " " + next_word
    return None


def first_word(model):
    first = random.choice(list(model.keys()))
    while not re.match(r"^[A-Z].*\w\s.*\w$", first):
        first = random.choice(list(model.keys()))
    return first


def main():
    text_generator = TextGenerator
    text_generator.tokens = tokenize()
    text_generator.trigrams = trigrams_maker(text_generator.tokens)
    trigrams = text_generator.trigrams
    sentence_combiner(trigrams)


if __name__ == "__main__":
    main()
