from utility.func import level_mapping


class User:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    def get_card(self, card_title):
        for card in self.cards:
            if card_title == card.title:
                return card
        return None

    @property
    def score(self):
        return sum([card.score for card in self.cards])

    @property
    def level(self):
        return level_mapping(self.score)