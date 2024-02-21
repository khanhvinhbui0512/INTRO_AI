import copy
import random
import math
import minimax
import machine
def play(cnt):
    game1 = machine.checker(machine.base_table,-1)
    game2 = minimax.checker(minimax.base_table, 1)
    while (True):
        if (cnt % 2 == 0):
            temp = game1.find_move(6)
            if (not isinstance(temp, machine.move)):
                print("Minimax thang")
                break
            else:
                for i in range(8):
                    print(game1.table[i])
                for i in range(len(temp.move)):
                    print(temp.move[i].x, temp.move[i].y, sep=" ")
            game2.process(minimax.move(temp.move))
        else:
            temp = game2.find_move(6)
            if (not isinstance(temp, minimax.move)):
                print("Machine Learning thang")
                break
            else:
                for i in range(8):
                    print(game2.table[i])
                for i in range(len(temp.move)):
                    print(temp.move[i].x, temp.move[i].y, sep=" ")
            game1.process(machine.move(temp.move))
        cnt += 1
print("Nhập số 0 nếu Machine Learning đi trước và 1 nếu Minimax đi trước:")
num = int(input())
while(num !=0 and num  != 1):
    print("Nhập số 0 nếu Machine Learning đi trước và 1 nếu Minimax đi trước:")
    num = int(input())
play(num)

