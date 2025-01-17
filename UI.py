""" UI Class for handling the UI in the console"""


import os
import time
import msvcrt

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

    
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')


    def confirm(delay=1):
        """
        Pauses terminal for 1 second or until key press
        :return: None
        """

        print(f"Press any key or wait {delay} sec to continue")
        startTime = time.time()
        inp = None
        while True:
            if msvcrt.kbhit():
                inp = msvcrt.getch()
                break
            elif time.time() - startTime > delay:
                break


    def get_input():
        """ 
        Gets user input including some special inputs
        :return: key if recognized else None
        """
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
            
    def table(self,
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
        row_header=False):
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