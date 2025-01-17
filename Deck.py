from BJ import BJ
BlackJack = BJ()

class Deck:
    def __init__(self, decks=4, shufflecard_percentage=0.75):
        self.cards = {}
        self.decks = decks
        self.shufflecard_percentage = shufflecard_percentage
        self.shufflecard = self.shufflecard_percentage*self.decks*52

        for suit in BlackJack.Suits:
            for name in BlackJack.CardNames.keys():
                self.cards[f"{suit}{name}"] = 4*self.decks
