class Card():
    
    def __init__(self, GameInstance, suit, name) -> None:
    
        GameInstance = GameInstance
        self.suit = suit if suit in GameInstance.bj.Suits.keys() else "?"
        self.name = name if name in GameInstance.bj.CardNames.keys() else "?"
    
    def get_printout(self):
        self.printout = [
            f" ___ ",
            f"|{self.name}  |",
            f"| {self.suit} |",
            f"|__{self.name}|",
        ]

        return self.printout
    
    def print(self):
        for i in self.printout:
            print(i)