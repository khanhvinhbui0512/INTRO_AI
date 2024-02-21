import pygame, sys
import numpy as np
from point import point
from GUI import  GUI

class game:
    def __init__(self,filename: str):
        self.size_board = 0
        self.star = 0
        self.table = []
        self.read(filename)
        self.GUI = GUI(self.table,self.star)
    def read(self,filename:str):
        with open(filename) as test_file:
            line = next(test_file)
            n,m = list(map(int, line.split()))
            table = []
            for i in range(n):
                line = next(test_file)
                row = line.split(' ')
                temp = []
                for j in range(len(row)): temp.append(int(row[j]))
                table.append(temp)
            self.size_board = n
            self.star = m
            self.table = table
    def play(self):
        self.GUI.play()


print("Choose one level from 1 to 20")
level = int(input())
while level > 20 or level < 1:
    print("Level doesn't exit. Please choose agian one level from 1 to 12")
    level = int(input())
filename = "testcase/text" + str(level) + ".txt"
game = game(filename)
game.play()
