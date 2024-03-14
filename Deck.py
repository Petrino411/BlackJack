from Card import Card
import random


class Deck:
    def __init__(self):
        print("Deck __init")
        suits = ['черви', 'бубны', 'крести', 'пики']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'валет', 'дама', 'король', 'туз']
        self.cards = [Card(suit, value) for suit in suits for value in values]
        self.playing_cards = self.shuffle_cards()
        print("Deck_inited")

    def deal_card(self):
        return self.playing_cards.pop()

    def shuffle_cards(self):
        print("Shuffling")
        cards = self.cards.copy()
        random.shuffle(cards)
        return cards

