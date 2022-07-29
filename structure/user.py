from glob import glob
from os.path import basename

from structure.card import CardFromFile, Card
from structure.decision_taker import DecisionMaker
from utility.func import level_mapping


class User:
    def __init__(self, name):
        """
        Class defining a user and its properties.
        :param name: str
        """
        self.name = name
        self.cards = []
        self.dm = DecisionMaker(25000, "embeddings/embeddings-l-model.vec")
        for path in glob(f"data/{name}/cards/*.json"):
            self.cards.append(CardFromFile(self, basename(path).replace(".json", "")))

    def add_new_card(self, title, words):
        """ Add a new card to the user.
        :param title: str
        :param words: list of Words
        :return: Card
        """

        card = Card(title, words, self)
        card.save()  # Save the card in the user's folder
        self.cards.append(card)

    def get_card(self, card_title):
        """
        Get a card from the user by its title.
        :param card_title: Card object
        :return: Card object
        """
        for card in self.cards:
            if card_title == card.title:
                return card
        return None

    @property
    def score(self):
        """
        Get the user's score.
        :return: int
        """
        return sum([card.score for card in self.cards])

    @property
    def level(self):
        """
        Get the user's level.
        :return: int
        """
        return level_mapping(self.score)
