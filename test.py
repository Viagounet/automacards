import unittest
from copy import deepcopy

from structure.card import Card
from structure.user import User
from structure.word import Word


class TestWord(unittest.TestCase):
    def test_word_string(self):
        """
        Test that the string is set correctly.
        """
        string = "test"
        word = Word(string)
        self.assertEqual(word.string, string, "word.string is not set correctly at initialization.")


class TestCard(unittest.TestCase):
    def test_add_word(self):
        """
        Test that a word is added to the card.
        """
        user = User("viagounet")
        word = Word("test")
        other_word = Word("test2")

        card = Card("test", [word], user)
        card.words.append(other_word)
        self.assertEqual(len(card.words), 2, "The word was not added to the card via card.words.append")

    def test_shuffle(self):
        """
        Test that the words are shuffled.
        """
        user = User("viagounet")
        word = Word("test")
        other_word = Word("test2")

        card = Card("test", [word, other_word], user)
        card_copy = deepcopy(card)
        card.shuffle()
        print(card.words, card_copy.words)
        self.assertNotEqual([word.string for word in card.words], [card_copy.string for word in card.words], "The words were not shuffled.")

if __name__ == '__main__':
    unittest.main()
