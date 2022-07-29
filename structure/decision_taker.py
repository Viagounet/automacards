import spacy
from gensim.models import KeyedVectors

from structure.word import Word
from utility.func import lev_dist


class DecisionMaker:
    def __init__(self, limit, wv_file):
        self.wv = KeyedVectors.load_word2vec_format(wv_file, limit=limit)
        self.model = spacy.load("es_core_news_sm")

    def add_words_to(self, card):
        card_words = []
        for word in card.words:
            if word.string in self.wv:
                card_words.append(word.string)
        most_similar = self.wv.most_similar_cosmul(positive=card_words, topn=100)
        similar_words = [self.lemmatize(value[0]) for value in most_similar]
        similar_words_self_filtered = self.self_min_lev_threshold(similar_words, 2)
        similar_words_filtered = self.min_lev_threshold(similar_words_self_filtered, card_words, 2)[:5]

        for word in similar_words_filtered:
            # card += Word(word)
            card.words.append(Word(word))

    def lemmatize(self, word):
        doc = self.model(word)
        if doc[0].pos_ == "VERB":
            return word
        else:
            return doc[0].lemma_

    @staticmethod
    def min_lev_threshold(words_list, words_list_, threshold):
        kept_words = []
        for word in words_list:
            keep = True
            for word_ in words_list_:
                if lev_dist(word, word_) < threshold:
                    keep = False
                    break
            if keep:
                kept_words.append(word)
        return kept_words

    @staticmethod
    def self_min_lev_threshold(words_list, threshold):
        kept_words = []
        words_list = words_list[::-1]
        deleted_keys = []
        for i, word in enumerate(words_list):
            keep = True
            for word_ in filter(lambda x: x != word, words_list):
                if lev_dist(word, word_) < threshold and word not in deleted_keys:
                    keep = False
                    deleted_keys.append(word_)
                    break
            if keep:
                kept_words.append(word)
        return kept_words[::-1]
