class BJ():
    def __init__(self) -> None:
        
        self.Suits = {
        "♠": "spade",
        "♥": "heart",
        "♦": "diamond",
        "♣": "club"
        }
    
        self.CardNames = {
        "A": "ace",
        "2": "two",
        "3": "three",
        "4": "four",
        "5": "five",
        "6": "six",
        "7": "seven",
        "8": "eight",
        "9": "nine",
        "T": "ten",
        "J": "jack",
        "Q": "queen",
        "K": "king"
        }
    
        self.CardValues = {
        "A": 11,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 10,
        "Q": 10,
        "K": 10
        }

        self.Tens = ["T", "J", "Q", "K"]

    def get_hand_type(self, hand):
        if hand[0] == "S":
            return "Soft"
        elif hand[0] == "D":
            return "Pair"
        else:
            return "Hard"