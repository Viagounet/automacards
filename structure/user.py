class User:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards

    def get_card(self, card_title):
        for card in self.cards:
            if card_title == card.title:
                return card
        return None
