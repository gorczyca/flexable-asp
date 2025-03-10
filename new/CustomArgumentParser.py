import argparse

class CustomParser(argparse.ArgumentParser): 
    def __init__(self):
        super().__init__()
        self.add_argument("-i", dest="instance", type=str)
        self.add_argument("-a", dest="approach", type=str)
        self.add_argument("-g", dest="goal", type=str)
        self.add_argument("-c", dest="constraints", action="store_true")
        self.add_argument("-x", dest="max_moves", type=int, default=-1)
        self.add_argument("-l", dest="logic_program_path", type=str)
        self.add_argument("-s", dest="subprocess", action="store_true")
        self.add_argument("-o", dest="game_over_check", action="store_true") # check if game over, i.e. whether to perform the 2nd check

