import os

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
