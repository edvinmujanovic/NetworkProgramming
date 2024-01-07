from enum import Enum
import random

class Suit(Enum):
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4

class Card:
    def __init__(self, suit, value):
        assert suit in Suit and 1 <= value <= 13
        self._suit = suit
        self._value = value


    def getValue(self):
        return self._value

    def getSuit(self):
        return self._suit

    def __str__(self):
        suits = {Suit.HEARTS: "Hearts", Suit.DIAMONDS: "Diamonds", Suit.CLUBS: "Clubs", Suit.SPADES: "Spades"}
        values = {1: "Ace", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King"}
        return f"{values[self._value]} of {suits[self._suit]}"

class CardDeck:
    def __init__(self):
        self.myCards = []
        self.reset()

    def shuffle(self):
        random.shuffle(self.myCards)

    def getCard(self):
        if self.size() > 0:
            card = self.myCards.pop()
            return card
        else:
            return None

    def size(self):
        return len(self.myCards)

    def reset(self):
        self.myCards = [Card(suit, value) for suit in Suit for value in range(1, 14)]


deck = CardDeck()
deck.shuffle()
while deck.size() > 0:
    card = deck.getCard()
    print(f"Card {card} has value {card.getValue()}")
