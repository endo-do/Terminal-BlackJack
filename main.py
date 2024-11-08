# Project ToDo list: https://www.notion.so/ToDo-cc089fa4b8964a79b1546003c8274dce?pm=c
# pyinstaller --onefile --distpath . main.py

# Imports
import random
import os
import pandas as pd
import msvcrt
import threading
import time
import yaml
from playsound import playsound # https://stackoverflow.com/questions/69245722/error-259-on-python-playsound-unable-to-sound

# General  Functions

# Get user Input including some special inputs
def get_input():

    first_byte = msvcrt.getch()

    if first_byte in {b'\x00', b'\xe0'}:

        second_byte = msvcrt.getch()
        
        arrow_keys = {
            b'H': 'up',
            b'P': 'down',
            b'K': 'left',
            b'M': 'right'
        }
        
        key_name = arrow_keys.get(second_byte, None)
        
        if key_name:
            return key_name
        else:
            return None
    
    elif first_byte == b'\r':
        return "enter"
    
    elif first_byte == b' ':
        return "space"
    
    elif first_byte == b'\x1b':
        return "esc"

    else:

        try:
            char = first_byte.decode('utf-8')
            return char        

        except UnicodeDecodeError:
            return None

# Resets all values of specified keys in specified dict to 0
def clean_dict(dictionary, keys, reset=0):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            clean_dict(value, keys, reset)  # Pass 'reset' to the recursive call
        elif key in keys:
            dictionary[key] = reset

# Returns the strings as stroken through
def strike(text):
    return ''.join([u'\u0336{}'.format(c) for c in text])

# Clears Terminal
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Pauses terminal for 1 second or until key press 
def confirm(delay=1):
    print(f"Press any key or wait {delay} sec to continue")
    startTime = time.time()
    inp = None
    while True:
        if msvcrt.kbhit():
            inp = msvcrt.getch()
            break
        elif time.time() - startTime > delay:
            break

# Converts time in seconds to a more human-readable format
def convert_time(time):
    if time > 60:
        time /= 60
        if time > 60:
            if time > 24:
                return f"{round(time / 1440, 2)} d"
            else:
                return f"{round(time / 60, 2)} h"
        else:
            return f"{round(time)} m"
    else:
        return f"{time} s"
# UI class to store all strings used to make to UI in the console
class UI():
    
    def __init__(self) -> None:
        
        self.Arrows = {"up":"↑", "down": "↓", "left":"←", "right":"→"}
        
        self.InfoStandart = "|                   ¦                      ¦                   |"
        self.InfoDrillrulesRandom = "|  Basic Strategy   ¦     Random Hands     ¦    [e] - quit     |"
        self.InfoDrillrulesHard = "|  Basic Strategy   ¦    Only Hard Hands   ¦    [e] - quit     |"
        self.InfoDrillrulesSoft = "|  Basic Strategy   ¦    Only Soft Hands   ¦    [e] - quit     |"
        self.InfoDrillrulesPair = "|  Basic Strategy   ¦    Only Pair Hands   ¦    [e] - quit     |"
        self.InfoBasicstrategy = "|   Basic Strategy  ¦                      ¦                   |"
        self.InfoBasicstrategyDrillsets = "|   Basic Strategy  ¦      Drill Sets      ¦                   |"
        self.InfoBasicstrategyCharts = "|   Basic Strategy  ¦        Charts        ¦                   |"
        self.InfoBasicstrategyChartsAllhands = "|   Basic Strategy  ¦       All Hands      ¦     [e] - quit    |"
        self.InfoBasicstrategyChartsHardhands = "|   Basic Strategy  ¦      Hard Hands      ¦     [e] - quit    |"
        self.InfoBasicstrategyChartsSofthands = "|   Basic Strategy  ¦      Soft Hands      ¦     [e] - quit    |"
        self.InfoBasicstrategyChartsPairhands = "|   Basic Strategy  ¦      Pair Hands      ¦     [e] - quit    |"
        self.InfoBasicstrategyStatistics = "|   Basic Strategy  ¦      Statistics      ¦                   |"
        self.InfoBasicstrategyStatisticsGeneral = "|   Basic Strategy  ¦  General Statistics  ¦    [e] - quit     |"
        self.InfoBasicstrategyStatisticsHand = "|   Basic Strategy  ¦     Hand Statistics   ¦    [e] - quit     |"
        self.InfoBasicstrategyStatisticsHard = "|   Basic Strategy  ¦ Hard Hand Statistics ¦    [e] - quit     |"
        self.InfoBasicstrategyStatisticsSoft = "|   Basic Strategy  ¦ Soft Hand Statistics ¦    [e] - quit     |"
        self.InfoBasicstrategyStatisticsPair = "|   Basic Strategy  ¦ Pair Hand Statistics ¦    [e] - quit     |"
        self.InfoBasicstrategyStatisticsErrors = "|   Basic Strategy  ¦      Last Errors     ¦    [e] - quit     |"
        self.InfoFreeplay = "|     Free Play     ¦                      ¦                   |"
        self.InfoFreeplayTraining = "|     Free Play     ¦      Training        ¦                   |"
        self.InfoFreeplayFreeplay = "|     Free Play     ¦      Free Play       ¦                   |"
        self.InfoMenu =   "|                   ¦      Main Menu       ¦                   |"
        self.InfoSettings = "|       Settings       ¦                    ¦                   |"
        self.Barrier = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        self.Title = r"""
          ____  _            _        _            _    
         |  _ \| |          | |      | |          | |   
         | |_) | | __ _  ___| | __   | | __ _  ___| | __
         |  _ <| |/ _` |/ __| |/ /   | |/ _` |/ __| |/ /
         | |_) | | (_| | (__|   < |__| | (_| | (__|   < 
         |____/|_|\__,_|\___|_|\_\____/ \__,_|\___|_|\_\ 
              """
        
    def title(self):
        print(self.Title)

    def info(self, info):
        print(self.Barrier)
        print(info)
        print(self.Barrier)

# BJ class to store everything about BlackJack
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

# Card class to handle everything about Cards
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


# Path class to store all relevant paths
class Path():
    def __init__(self) -> None:

        # paths in UserData\BasicStrategy
        self.Errors = r"UserData\\BasicStrategy\\Errors.txt"
        self.General = r"UserData\\BasicStrategy\\General.yml"
        self.Hands =  r"UserData\\BasicStrategy\\Hands.yml"

        # paths in GameData
        self.Settings = r"GameData\\Settings.yml"
        
        # paths in GameData\\BasicStrategy
        self.BasicStrategyTheory = r"GameData\\BasicStrategy\\BasicStrategyTheory.csv"
        self.AllHandsChart = r"GameData\\BasicStrategy\\AllHandsChart.csv"
        self.HardHandsChart = r"GameData\\BasicStrategy\\HardHandsChart.csv"
        self.SoftHandsChart = r"GameData\\BasicStrategy\\SoftHandsChart.csv"
        self.PairHandsChart = r"GameData\\BasicStrategy\\PairHandsChart.csv"

    def initiate(self):
        print("Getting current folder path")
        dir = os.path.dirname(os.path.abspath(__file__))
        print("Updating all relevant paths")
        for path in [self.Errors, self.General, self.Hands, self.BasicStrategyTheory, self.AllHandsChart, self.HardHandsChart, self.SoftHandsChart, self.PairHandsChart]:
            path = f"{dir}\\{path}"

# Table class to display charts
class Table:
    def __init__(
        self,
        content,
        space_left=1,
        space_right=1,
        space_left_table=0,
        orientation="left",
        min_width=None,
        max_width=None,
        same_sized_cols=False,
        empty_cells=["", "#empty"],
        empty_lists=[[], [""], ["#empty"]],
        replace_empty="",
        col_header=False,
        row_header=False
    ):
        
        self.content = content
        self.space_left = space_left 
        self.space_right = space_right 
        self.orientation = orientation 
        self.min_width = min_width 
        self.max_width = max_width
        self.same_sized_cols = same_sized_cols
        self.empty_cells = empty_cells 
        self.empty_lists = empty_lists 
        self.replace_empty = replace_empty 
        self.col_header = col_header
        self.row_header = row_header
        self.space_left_table = space_left_table
    
    def display(self):

        self.rows = len(self.content)
        self.columns = 0
        for row in self.content:
            if len(row) > self.columns: 
                self.columns = len(row)
        
        self.max_chars = []
        for cell in range(self.columns): 
            self.max_chars.append(0)
        for row in self.content: 
            active_column = 0
            for cell in row:
                if len(str(cell)) > self.max_chars[active_column]: 
                    self.max_chars[active_column] = len(str(cell))
                active_column += 1

        if self.min_width != None:
            for index, i in enumerate(self.max_chars):
                if self.min_width > int(i):
                    self.max_chars[index] = self.min_width
        
        if self.max_width != None:
            for index, i in enumerate(self.max_chars):
                if self.max_width < int(i):
                    self.max_chars[index] = self.max_width

        if self.same_sized_cols:
            self.max_chars = [max(self.max_chars) for i in self.max_chars]
        
        self.header = {"col":[], "row":[]}

        column_index = 0  
        print(self.space_left_table * " ", end="")
        print("╔", end="")
        for column in self.max_chars:
            print("═" * self.space_left, end="")  
            print("═" * column, end="")  
            print("═" * self.space_right, end="")  
            
            if column_index == len(self.max_chars) - 1:  
                print("╗")
            
            else:
            
                if self.col_header and column_index == 0:
                    print("╦", end="")
            
                else:
                    print("╤", end="")  
            
            column_index += 1  
        row_index = 0
        
        for row in range(self.rows): 
            print(self.space_left_table * " ", end="")
            print("║", end="") 
            column_index = 0

            for column in range(self.columns):

                spacebar_counter = self.max_chars[column] - len(str(self.content[row][column])) 
                text = str(self.content[row][column])

                if len(text) > self.max_chars[column_index]:

                    if self.max_chars[column_index] == 2:
                        text = ".."
                    elif int(self.max_chars[column_index]) == 3:
                        text = [i for i in text]
                        text = text[0]
                        text += ("..")
                    
                    elif int(self.max_chars[column_index]) >= 3:
                        text = [i for i in text]
                        text = text[:int(self.max_chars[column_index])-2]
                        text.append("..")
                        textstr = ""
                        for i in text:
                            textstr += i
                        text = textstr
                    spacebar_counter = 0
                
                if self.orientation == "left": 
                    content = text + str(spacebar_counter * " ")  
                
                elif self.orientation == "right":
                    content = str(spacebar_counter * " ") + text 

                print(" " * self.space_left, end="")
                print(content, end="")
                print(" " * self.space_right, end="")
                
                if column_index == self.columns - 1: 
                    print("║") 
                else:
                    if self.col_header and column_index == 0:
                        line = "║"
                    else:
                        line = "│" 
                    print(line, end="")
                column_index += 1  
            
            if row_index == 0 and "row" in self.header: 
                left_border = self.space_left_table * " " + "╠"
                connection = "═"
                right_border = "╣"
                cross_connection = "╪"

            elif row_index == self.rows - 1:
                left_border = self.space_left_table * " " + "╚"
                connection = "═"
                right_border = "╝"
                cross_connection = "╧"

            else:
                left_border = self.space_left_table * " " + "╟"
                connection = "─"
                right_border = "╢"
                cross_connection = "┼"

            print(left_border, end="") 
            column_index = 0
        
            for column in self.max_chars: 
                print(connection * self.space_left, end="")
                print(column * connection, end="") 
                print(connection * self.space_right, end="") 
                
                if column_index == len(self.max_chars) - 1: 
                    print(right_border)
                
                else:
                
                    if self.col_header and column_index == 0:
                
                        if row_index == self.rows - 1:
                            print("╩", end="")
                
                        elif self.row_header and row_index == 0:
                            print("╬", end="")
                
                        else:
                            print("╫", end="")
                
                    else:
                        print(cross_connection, end="") 

                column_index += 1

            row_index += 1

# Game class
class Game():
    
    def __init__(self) -> None:
    
        # get all information that is stored in other classes
        self.ui = UI()
        self.bj = BJ()
        self.path = Path()

        # user settings
        self.SettingSound = True
        self.SettingKeybinds = {"H":["w"], "S":["s"], "D":["d"], "P":["a"]}
        self.SettingSkip21 = True
        self.SettingEvenRandomness = True
        self.SettingDecks = 4
        
        # bools
        self.running = False
        self.drillBool = False

        # data related
        self.BJTheory = None
        self.PossiblePlayerHands = ["21", "20", "19", "18", "17", "16", "15", "14", "13", "12", "11", "10", "9", "8", "7", "6", "5", "S21", "S20", "S19", "S18", "S17", "S16", "S15", "S14", "S13", "SD12", "D20", "D18", "D16", "D14", "D12", "D10", "D8", "D6", "D4"]
        self.PossibleDealerHands = ["-", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]

        # drill related
        self.drill_type = None
        self.drillrulesInfo = [self.ui.InfoDrillrulesRandom, self.ui.InfoDrillrulesHard, self.ui.InfoDrillrulesSoft, self.ui.InfoDrillrulesPair]
        self.drillrules_names = ["random", "hard", "soft", "pair"]

        # freeplay related
        self.deck = []
        self.shuffleCard = None
        
        # blackjack related
        self.dealerHandPrintout = None
        self.playerHandPrintout = None
        self.dealerHand = None
        self.playerHand = None

        # statistics
        self.statisticsInfo = [self.ui.InfoBasicstrategyStatisticsGeneral, self.ui.InfoBasicstrategyStatisticsHand, self.ui.InfoBasicstrategyStatisticsHard, self.ui.InfoBasicstrategyStatisticsSoft, self.ui.InfoBasicstrategyStatisticsPair, self.ui.InfoBasicstrategyStatisticsErrors]
        self.stats = {"BasicStrategy":["general", "all", "hard", "soft", "pair", "errors"]}
        self.handsPlayed = 0
        self.handsPlayedCorrectly = 0
        self.accuracy = "100.0 %"
        self.lastMistake = "No last mistake"

    # Main game function
    def main(self):
        print("Hello World")
        self.initiate()
        while self.running:
            self.menu()
    
    # Funtion that handles playing sound
    def play_sound(self, name):
        if self.SettingSound:
            threading.Thread(target=lambda: playsound(f"Audio/{name}.mp3")).start()
    
    # Function to reset a specific stat file
    def reset_stats(self):
        with open(self.path.Hands, "r+") as f:
            data = yaml.safe_load(f)
            clean_dict(data, ["played", "played_correctly", "played_incorrectly"])
            f.seek(0)
            yaml.safe_dump(data, f)
            f.truncate()
    
        with open(self.path.General, "r+") as f:
            data = yaml.safe_load(f)
            for i in data["GeneralStatistics"]:
                if i != "Last50Hands" and i != "Last50HardHands" and i != "Last50SoftHands" and i != "Last50PairHands" and i != "Last50RandomHands":
                    data["GeneralStatistics"][i] = 0
                else:
                    data["GeneralStatistics"][i] = []
            f.seek(0)
            yaml.safe_dump(data, f)
            f.truncate()

        with open(self.path.Errors, "w") as f:
            pass

    # Function that deletes old data if to much data is saved to prevent long loading times
    def stat_overflow_check(self):
        with open(self.path.Errors, "r") as f:
            lines = f.readlines()
        if len(lines) > 100:
            print("Deleting old data in error file")
            cutLines = lines[-100:]
            with open(self.path.Errors, "w") as f:
                f.writelines(cutLines)
    
    # Function that displays statistics contained in a specific file
    def display_stats(self, file):
        if file ==  "errors":
            with open(self.path.Errors, "r") as f:
                lines = f.readlines()
                data = [i.strip() for i in lines]
            output = []
            if len(data) <= 25:
                for index, i in enumerate(data):
                    output.insert(0, f"{len(data) - index}.{"  " if len(data) - index < 10 else " "} {i}")
            else:
                for index, i in enumerate(data[-25:]):
                    output.append(f"{25 - index}.{"  " if 25 - index < 10 else " "} {i}")
            
            output.insert(0, "")
            output.insert(0, "Last 25 Errors:")


        elif file == "general":
            with open(self.path.General) as f:
                data = yaml.safe_load(f)
            output = ["General Statistics:", ""]
            output.append(f"Total Hands Played: {data["GeneralStatistics"]["HandsPlayed"]}")
            output.append(f"   - Correct Hands: {data["GeneralStatistics"]["HandsPlayedCorrectly"]}")
            try:
                output.append(f"   - All Time Accuracy: {round(data["GeneralStatistics"]["HandsPlayedCorrectly"] / data["GeneralStatistics"]["HandsPlayed"] * 100)} %")
            except ZeroDivisionError:
                output.append(f"   - All Time Accuracy: 100 %")
            try:
                output.append(f"       - Last 50 Hands: {round(data["GeneralStatistics"]["Last50Hands"].count(1) / len(data["GeneralStatistics"]["Last50Hands"]) * 100)} %")
            except ZeroDivisionError:
                output.append(f"       - Last 50 Hands: 100 %")
            output.append("")
            output.append(f"Total Hard Hands Played: {data["GeneralStatistics"]["HardHandsPlayed"]}")
            output.append(f"   - Correct Hands: {data["GeneralStatistics"]["HardHandsPlayedCorrectly"]}")
            try:
                output.append(f"   - All Time Accuracy: {round(data["GeneralStatistics"]["HardHandsPlayedCorrectly"] / data["GeneralStatistics"]["HardHandsPlayed"] * 100)} %")
            except ZeroDivisionError:
                output.append(f"   - All Time Accuracy: 100 %")
            try:
                output.append(f"       - Last 50 Hands: {round(data["GeneralStatistics"]["Last50HardHands"].count(1) / len(data["GeneralStatistics"]["Last50HardHands"]) * 100)} %")
            except ZeroDivisionError:
                output.append(f"       - Last 50 Hands: 100 %")
            output.append("")
            output.append(f"Total Soft Hands Played: {data["GeneralStatistics"]["SoftHandsPlayed"]}")
            output.append(f"   - Correct Hands: {data["GeneralStatistics"]["SoftHandsPlayedCorrectly"]}")
            try:
                output.append(f"   - All Time Accuracy: {round(data["GeneralStatistics"]["SoftHandsPlayedCorrectly"] / data["GeneralStatistics"]["SoftHandsPlayed"] * 100)} %")
            except ZeroDivisionError:
                output.append(f"   - All Time Accuracy: 100 %")
            try:
                output.append(f"       - Last 50 Hands: {round(data["GeneralStatistics"]["Last50SoftHands"].count(1) / len(data["GeneralStatistics"]["Last50SoftHands"]) * 100)} %")
            except ZeroDivisionError:
                output.append(f"       - Last 50 Hands: 100 %")
            output.append("")
            output.append(f"Total Pair Hands Played: {data["GeneralStatistics"]["PairHandsPlayed"]}")
            output.append(f"   - Correct Hands: {data["GeneralStatistics"]["PairHandsPlayedCorrectly"]}")
            try:
                output.append(f"   - All Time Accuracy: {round(data["GeneralStatistics"]["PairHandsPlayedCorrectly"] / data["GeneralStatistics"]["PairHandsPlayed"] * 100)} %")
            except ZeroDivisionError:
                output.append(f"   - All Time Accuracy: 100 %")
            try:
                output.append(f"       - Last 50 Hands: {round(data["GeneralStatistics"]["Last50PairHands"].count(1) / len(data["GeneralStatistics"]["Last50PairHands"]) * 100)} %")
            except ZeroDivisionError:
                output.append(f"       - Last 50 Hands: 100 %")
            time = data["GeneralStatistics"]["TimePlayed"]
            timeHard = data["GeneralStatistics"]["TimePlayedHard"]
            timeSoft = data["GeneralStatistics"]["TimePlayedSoft"]
            timeRandom = data["GeneralStatistics"]["TimePlayedRandom"]
            timePair = data["GeneralStatistics"]["TimePlayedPair"]
            infos = ["Total Time: ","   - Random Hands: ", "   - Hard Hands only: ", "   - Soft Hands only: ", "   - Pair Hands only: "]
            times = [time, timeRandom, timeHard, timeSoft, timePair]
            output.append("")
            for index, i in enumerate(times):
                output.append(infos[index] + convert_time(i))

        elif file == "hard" or file == "soft" or file == "pair" or file == "all":
            with open(self.path.General) as f:
                dataGeneral = yaml.safe_load(f)
            with open(self.path.Hands) as f:
                dataHands = yaml.safe_load(f)
            prefix = file.capitalize()
            if prefix == "All":
                prefix = ""
            output = [f"{prefix + " " if prefix != "" else ""}Hands Statistics:", ""]
            output.append(f"Hands Played: {dataGeneral["GeneralStatistics"][f"{prefix}HandsPlayed"]}")
            output.append(f"   - Correct Hands: {dataGeneral["GeneralStatistics"][f"{prefix}HandsPlayedCorrectly"]}")
            try:
                output.append(f"   - All Time Accuracy: {round(dataGeneral["GeneralStatistics"][f"{prefix}HandsPlayedCorrectly"] / dataGeneral["GeneralStatistics"][f"{prefix}HandsPlayed"] * 100, 2)} %")
            except ZeroDivisionError:
                output.append(f"   - All Time Accuracy: 100 %")
            try:
                output.append(f"       - Last 50 Hands: {round(dataGeneral["GeneralStatistics"][f"Last50{prefix}Hands"].count(1) / len(dataGeneral["GeneralStatistics"][f"Last50{prefix}Hands"]) * 100)} %")
            except ZeroDivisionError:
                output.append(f"       - Last 50 Hands: 100 %")
            output.append("")
            output.append("")
            output.append("Top 15 Misplayed Hands:")
            output.append("")
            Top15Errors = []
            for DealerHand in dataHands["DealerHand"]:
                for PlayerHand in dataHands["DealerHand"][DealerHand]["PlayerHand"]:
                    card = False
                    if file == "all":
                        card = True
                    if file == "hard" and PlayerHand[0] not in ["S", "D"]:
                        card = True
                    elif file == "soft" and PlayerHand[0] == "S":
                        card = True
                    elif file == "pair" and PlayerHand[0] == "D":
                        card = True
                    if card:
                        if dataHands["DealerHand"][DealerHand]["PlayerHand"][PlayerHand]["played"] > 0:
                            acc = round(dataHands["DealerHand"][DealerHand]["PlayerHand"][PlayerHand]["played_correctly"] / dataHands["DealerHand"][DealerHand]["PlayerHand"][PlayerHand]["played"] * 100, 2)
                        else:
                            acc = 100
                        if acc < 100:
                            Top15Errors.append([acc, PlayerHand, DealerHand, self.BJTheory.iloc[self.PossiblePlayerHands.index(PlayerHand), self.PossibleDealerHands.index(DealerHand)]])
                            Top15Errors = sorted(Top15Errors, key=lambda x: x[0])
                            if len(Top15Errors) > 15:
                                Top15Errors.pop()
            output.append(f"0.  Player vs Dealer | Accuracy | Correct")
            output.append(f"-----------------------------------------")
            for index, i in enumerate(Top15Errors):
                output.append(f"{index+1}.{" " if index >= 9 else "  "}{i[1]}{(6 - len(i[1])) * " "} vs {i[2]}{(6 - len(i[2])) * " "} | {'%.2f' % i[0]} %   | {i[3]}")
                        
            

        for i in output:
            print(i)

    # Function that resets the players and the dealers hand
    def reset_hands(self):

        self.dealerHandPrintout = ["", "", "", ""]
        self.playerHandPrintout = ["", "", "", ""]
        self.dealerHand = {"cards": "", "value": 0, "hand": ""}
        self.playerHand = {"cards": "", "value": 0, "hand": ""}

    # Function that loads all Game Data
    def loadGameData(self):
        
        self.load_settings()
        self.BJTheory = pd.read_csv(self.path.BasicStrategyTheory)

    # Function that loads and update the settings previously saved by the user
    def load_settings(self):
        with open(self.path.Settings) as f:
            self.settings = yaml.safe_load(f)
            self.SettingSound = self.settings["GeneralSettings"]["sound"]
            for action in self.settings["Keybinds"]:
                self.SettingKeybinds[action] = self.settings["Keybinds"][action]


    # Function that handles everything before the game can be played
    def initiate(self):
        self.path.initiate()
        print("Checking for data overflow")
        self.stat_overflow_check()
        print("Loading game relevant data")
        self.loadGameData()
        print("Starting game")
        self.running = True
        self.play_sound("intro")
    
    def drill(self):
        
        self.reset_hands()
        clear()

        startTime = time.time()

        with open(self.path.Hands) as file:
            self.handsData = yaml.safe_load(file)
        
        with open(self.path.General) as file:
            self.generalData = yaml.safe_load(file)

        Card1 = Card(self, list(self.bj.Suits.keys())[random.randint(0, 3)], list(self.bj.CardNames.keys())[random.randint(0, 12)])
        Card2 = Card(self, "?", "?")
        Card3 = Card(self, list(self.bj.Suits.keys())[random.randint(0, 3)], list(self.bj.CardNames.keys())[random.randint(0, 12)])
        Card4 = Card(self, list(self.bj.Suits.keys())[random.randint(0, 3)], list(self.bj.CardNames.keys())[random.randint(0, 12)])

        if self.SettingEvenRandomness:            
            for i in (Card1, Card3, Card4):
                if i.name in self.bj.Tens and random.randint(1, 4) != 1:
                    i.name = list(self.bj.CardNames.keys())[random.randint(0, 9)]
                if i.name == "T":
                    i.name = self.bj.Tens[random.randint(0, 3)]

        if self.drill_type == "soft":

            if Card3.name != "A" and Card4.name != "A":

                if random.randint(0, 1) == 1:
                    Card3.name = "A"
                else:
                    Card4.name = "A"
        
            elif Card3.name == "A" and Card4.name == "A":
                if self.SettingSkip21:
                    Card3.name = list(self.bj.CardNames.keys())[random.randint(1, 8)]
                
                else:
                    Card3.name = list(self.bj.CardNames.keys())[random.randint(1, 12)]
                
                    if self.SettingEvenRandomness:            
                        if Card3.name in self.bj.Tens and random.randint(1, 4) != 1:
                            Card3.name = list(self.bj.CardNames.keys())[random.randint(0, 9)]
                        if Card3.name == "T":
                            Card3.name = self.bj.Tens[random.randint(0, 3)]

        if self.drill_type == "pair":
            Card3.name = Card4.name
        
        if self.drill_type == "hard":
            while Card4.name == "A" or Card3.name == "A":
                Card3 = Card(self, list(self.bj.Suits.keys())[random.randint(0, 3)], list(self.bj.CardNames.keys())[random.randint(0, 12)])
                Card4 = Card(self, list(self.bj.Suits.keys())[random.randint(0, 3)], list(self.bj.CardNames.keys())[random.randint(0, 12)])

            while Card3.name == Card4.name:
                Card3 = Card(self, list(self.bj.Suits.keys())[random.randint(0, 3)], list(self.bj.CardNames.keys())[random.randint(0, 12)])
                Card4 = Card(self, list(self.bj.Suits.keys())[random.randint(0, 3)], list(self.bj.CardNames.keys())[random.randint(0, 12)])
                
                if self.SettingEvenRandomness:
                    for i in (Card1, Card3, Card4):
                        if i.name in self.bj.Tens and random.randint(1, 4) != 1:
                            i.name = list(self.bj.CardNames.keys())[random.randint(1, 9)]
                        if i.name == "T":
                            i.name = self.bj.Tens[random.randint(0, 3)]


        self.dealerHand["cards"] += Card1.name
        self.dealerHand["value"] += self.bj.CardValues[Card1.name]

        for card in (Card3, Card4):
            self.playerHand["cards"] += card.name
            self.playerHand["value"] += self.bj.CardValues[card.name]
        
        for hand in [self.playerHand]:
            if hand["cards"] == "AA":
                hand["hand"] = "SD12"
            else:
                if "A" in hand["cards"]:
                    hand["hand"] = f"S{hand["value"]}"
                elif hand["cards"][0] == hand["cards"][1]:
                    hand["hand"] = f"D{hand["value"]}"
                else:
                    hand["hand"] = f"{hand["value"]}"
        
        self.dealerHand["hand"] = str(self.dealerHand["value"])

        for card in (Card1, Card2):
            for index, i in enumerate(card.get_printout()):
                self.dealerHandPrintout[index] += f" {i}"

        for card in (Card3, Card4):
            for index, i in enumerate(card.get_printout()):
                self.playerHandPrintout[index] += f" {i}"

        if self.playerHand["value"] == 21 and self.SettingSkip21:
            pass

        else:
            self.ui.title()
            self.ui.info(self.drillrulesInfo[self.drillrules_names.index(self.drill_type)])
            print()
            
            output = ["", "", "", "", ""]
            
            output[0] += f"   Player has {self.playerHand["hand"]}"
            output[0] += " " * (4 - len(self.playerHand["hand"]))
            for index, i in enumerate(self.playerHandPrintout):
                output[index + 1] += "   " + i + "   "

            for index, i in enumerate(output):
                output[index] += "  |  "
            
            output[0] += f"   Dealer has {self.dealerHand["hand"]}"
            output[0] += " " * (4 - len(self.dealerHand["hand"]))
            for index, i in enumerate(self.dealerHandPrintout):
                output[index + 1] += "   " + i + "   "

            for index, i in enumerate(output):
                output[index] += "  |  "

            output[1] += f"Hands Played: {self.handsPlayed}"
            output[3] += f"Accuracy: {self.accuracy}"

            playerturn = True
            while playerturn:

                clear()

                self.ui.title()
                self.ui.info(self.drillrulesInfo[self.drillrules_names.index(self.drill_type)])
                print()

                for i in output:
                    print(i)
                print()
                print()
                Keys = []
                for i in ["H", "S", "D", "P"]:
                    Keys.append([j if j not in self.ui.Arrows.keys() else self.ui.Arrows[j] for j in self.SettingKeybinds[i]])
                for index, i in enumerate(Keys):
                    string = "["
                    for j in i:
                        if j == i[-1]:
                            string += f"{j}"
                        else:
                            string += f"{j}, "
                    string += "]"
                    Keys[index] = string
                print(f"{Keys[0]} - Hit | {Keys[1]} - Stand  | {Keys[2]} - Double | {Keys[3]} - Split")
                print()
                correctAction = self.BJTheory.iloc[self.PossiblePlayerHands.index(self.playerHand["hand"]), self.PossibleDealerHands.index(self.dealerHand["hand"])]
                action = get_input()
                if action == "e":
                    self.input = "e"
                    playerturn = False
                    self.play_sound("select")
                    self.drillBool = False
                    endTime = time.time()
                    self.generalData["GeneralStatistics"]["TimePlayed"] += round(endTime - startTime)
                    self.generalData["GeneralStatistics"][f"TimePlayed{self.drill_type.capitalize()}"] += round(endTime - startTime)
                    with open(self.path.General, "w") as file:
                            yaml.safe_dump(self.generalData, file)

                else:
                    self.handsPlayed += 1
                    self.generalData["GeneralStatistics"]["HandsPlayed"] += 1
                    self.generalData["GeneralStatistics"][f"{self.bj.get_hand_type(self.playerHand["hand"])}HandsPlayed"] += 1
                    self.handsData["DealerHand"][self.dealerHand["hand"]]["PlayerHand"][self.playerHand["hand"]]["played"] += 1
                    validActions = []
                    for i in list(self.SettingKeybinds.values()):
                        validActions.extend(i)
                    
                    if action in validActions:
                        playerturn = False
                        for key, keybinds in self.SettingKeybinds.items():
                            if action in keybinds:
                                action = key

                        if action == correctAction:
                            print(f"Correct, {correctAction} was the best action")
                            self.play_sound("right")
                            self.handsPlayedCorrectly += 1
                            self.handsData["DealerHand"][self.dealerHand["hand"]]["PlayerHand"][self.playerHand["hand"]]["played_correctly"] += 1
                            self.generalData["GeneralStatistics"]["HandsPlayedCorrectly"] += 1
                            self.generalData["GeneralStatistics"][f"{self.bj.get_hand_type(self.playerHand["hand"])}HandsPlayedCorrectly"] += 1
                            self.generalData["GeneralStatistics"]["Last50Hands"].append(1)
                            self.generalData["GeneralStatistics"][f"Last50{self.bj.get_hand_type(self.playerHand["hand"])}Hands"].append(1)
                        else:
                            print(f"Wrong, {correctAction} would have been correct")
                            self.play_sound("incorrect")
                            self.lastMistake = f"{self.playerHand["hand"]}{(4 - len(self.playerHand["hand"])) * " "} VS {self.dealerHand["hand"]}{(2 - len(self.dealerHand["hand"])) * " "} | {action} instead of {correctAction}"
                            with open(self.path.Errors,  "a") as f:
                                f.write(f"{self.lastMistake}\n")
                            self.handsData["DealerHand"][self.dealerHand["hand"]]["PlayerHand"][self.playerHand["hand"]]["played_incorrectly"] += 1
                            self.generalData["GeneralStatistics"]["Last50Hands"].append(0)
                            self.generalData["GeneralStatistics"][f"Last50{self.bj.get_hand_type(self.playerHand["hand"])}Hands"].append(0)
                        self.accuracy = f"{round((self.handsPlayedCorrectly / self.handsPlayed) * 100, 2)} %"
                        with open(self.path.Hands, "w") as file:
                            yaml.safe_dump(self.handsData, file)
                        for drill_type in ["", "Hard", "Soft", "Pair"]:
                            if len(self.generalData["GeneralStatistics"][f"Last50{self.bj.get_hand_type(self.playerHand["hand"])}Hands"]) > 50:
                                self.generalData["GeneralStatistics"][f"Last50{self.bj.get_hand_type(self.playerHand["hand"])}Hands"] = self.generalData["GeneralStatistics"][f"Last50{self.bj.get_hand_type(self.playerHand["hand"])}Hands"][-50:]
                        with open(self.path.General, "w") as file:
                            yaml.safe_dump(self.generalData, file)
                        print()
                        confirm(delay=1)
                    else:
                        pass
    
    def menu(self):

        clear()

        self.ui.title()
        self.ui.info(self.ui.InfoMenu)
        print()

        print(f"[1] - Basic Strategy\n[2] - {"Card Counting Drill"}\n[3] - {"Free Play"}\n[4] - {"Simulation"}\n[5] - Settings\n\n[q] - quit game")
        print()
        self.input = get_input()
        if self.input == "1":
            self.play_sound("select")
            self.input = None
            while self.input not in ["1", "2", "3", "e"]:
                clear()
                self.ui.title()
                self.ui.info(self.ui.InfoBasicstrategy)
                print()

                print("[1] - Basic Strategy Drill\n[2] - Basic Strategy Charts\n[3] - Statistics\n\n[e] - back to Main Menu")
                print()
                self.input = get_input()
            
            if self.input == "1":
                self.play_sound("select")
                self.input = None
                while self.input not in ["1", "2", "3", "4", "e"]:
                    clear()
                    self.ui.title()
                    self.ui.info(self.ui.InfoBasicstrategyDrillsets)
                    print()

                    print(f"[1] - Random Hands (Even Randomness is {"on" if self.SettingEvenRandomness else "off"})\n[2] - Hard Hands only\n[3] - Soft Hands only\n[4] - Pair Hands only\n\n[e] - back to Main Menu")
                    print()
                    self.input = get_input()

                    if self.input in ("1", "2", "3", "4", "5"):
                        self.play_sound("select")
                        self.drill_type = self.drillrules_names[int(self.input) - 1]
                        self.drillBool = True
                        while self.drillBool:
                            self.drill()

                    elif self.input == "e":
                        self.play_sound("select")

            if self.input == "2":
                self.play_sound("select")
                self.input = None
                while self.input not in ["1", "2", "3", "4", "5", "e"]:
                    clear()
                    self.ui.title()
                    self.ui.info(self.ui.InfoBasicstrategyCharts)
                    print()

                    print("[1] - All Hands\n[2] - Hard Hands\n[3] - Soft Hands\n[4] - Pair Hands\n\n[e] - back to Main Menu")
                    print()
                    self.input = get_input()
                    
                    if self.input == "1" or self.input == "2" or self.input == "3" or self.input == "4":
                        clear()
                        self.play_sound("select")
                        self.ui.title()
                        info = ""
                        chart = None
                        if self.input == "1":
                            info = self.ui.InfoBasicstrategyChartsAllhands
                            chart = pd.read_csv(self.path.AllHandsChart)
                        elif self.input == "2":
                            info = self.ui.InfoBasicstrategyChartsHardhands
                            chart = pd.read_csv(self.path.HardHandsChart)
                        elif self.input == "3":
                            info = self.ui.InfoBasicstrategyChartsSofthands
                            chart = pd.read_csv(self.path.SoftHandsChart)
                        elif self.input == "4":
                            info = self.ui.InfoBasicstrategyChartsPairhands
                            chart = pd.read_csv(self.path.PairHandsChart)
                        self.ui.info(info)
                        print()
                        headers = chart.columns.tolist()
                        chart = chart.values.tolist()
                        chart.insert(0, headers)
                        Chart = Table(chart, space_left_table=8, col_header=True, row_header=True)
                        Chart.display()
                        print()
                        self.input = None
                        while self.input != "e":
                            self.input = get_input()
                        self.play_sound("select")
                    
            if self.input == "3":
                self.play_sound("select")
                self.input = None
                while self.input not in ["1", "2", "3", "4", "5", "6", "e"]:
                    clear()
                    self.ui.title()
                    self.ui.info(self.ui.InfoBasicstrategyStatistics)
                    print()

                    print("[1] - General\n[2] - All Hands\n[3] - Hard Hands\n[4] - Soft Hands\n[5] - Pair Hands\n[6] - Last Errors\n\n[e] - back to Main Menu")
                    print()
                    self.input = get_input()
                    if self.input in ("1", "2", "3", "4", "5", "6"):
                        self.play_sound("select")
                        clear()
                        self.ui.title()
                        self.ui.info(self.statisticsInfo[int(self.input) - 1])
                        print()
                        self.display_stats(self.stats["BasicStrategy"][int(self.input) - 1])
                        print()
                        self.input = None
                        while self.input != "e":
                            self.input = get_input()
                        
                        if self.input == "e":
                            self.play_sound("select")

                    elif self.input == "e":
                                self.play_sound("select")

            elif self.input == "e":
                        self.play_sound("select")
                        pass

        if self.input == "5":
            self.play_sound("select")
            self.input = None
            while self.input != "e":
                clear()
                self.ui.title()
                self.ui.info(self.ui.InfoSettings)
                print()
                print(f"[1] - Clear All Statistics\n[2] - Toggle Sound {"off" if self.SettingSound else "on"}\n[3] - Turn {"off" if self.SettingSkip21 else "on"} Automaticly Skippings 21's in Drills\n\n[e] - quit")
                print()
                self.input = get_input()
                
                if self.input == "1":
                    self.play_sound("select")
                    self.reset_stats()
                    print("All Statistics have been cleared")
                    print()
                    confirm()
                
                elif self.input == "2":
                    self.play_sound("select")
                    if self.SettingSound:
                        self.SettingSound = False
                    else:
                        self.SettingSound = True
                    self.settings["GeneralSettings"]["sound"] = self.SettingSound
                    with open(self.path.Settings, "w") as f:
                        yaml.safe_dump(self.settings, f)
                    print(f"Sound has been turned {"on" if self.SettingSound else "off"}")
                    print()
                    confirm(delay=3)

                elif self.input == "3":
                    self.play_sound("select")
                    if self.SettingSkip21:
                        self.SettingSkip21 = False
                    else:
                        self.SettingSkip21 = True
                    self.settings["GeneralSettings"]["skip21"] = self.SettingSkip21
                    with open(self.path.Settings, "w") as f:
                        yaml.safe_dump(self.settings, f)
                    print(f"Skipping 21's in Drills has been turned {"on" if self.SettingSound else "off"}")
                    print()
                    confirm(delay=3)
                
                if self.input == "e":
                    self.play_sound("select")

        if self.input == "q":
            self.play_sound("outro")
            clear()
            self.ui.title()
            time.sleep(1)
            clear()
            self.running = False

BlackJackTable = Game()
BlackJackTable.main()