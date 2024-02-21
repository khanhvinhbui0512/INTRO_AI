from BKEL_CODE import *
import xlsxwriter
from xlsxwriter import Workbook
import bayes
import BKEL_CODE
import pandas as pd
import copy

def print_board(board):
    for i in range(5):

        for j in range(5):
            if (board[i][j] >= 0):
                print(" ", end="")
                print(board[i][j], end=" ")
            else:
                print(board[i][j], end=" ")
        print()


def check_vay(board, player, eval):
    Visited = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    for i in range(5):
        for j in range(5):
            if (Visited[i][j] == False and board[i][j] != 0):
                eval = BKEL_CODE.check_component(board, Visited, (i, j), eval)
    return eval


def GET_BOARD(move, board):
    start = move[0]
    end = move[1]
    new_board = copy.deepcopy(board)
    eval = BKEL_CODE.Eval_Function(board)
    new_board[end[0]][end[1]] = board[start[0]][start[1]]
    new_board[start[0]][start[1]] = 0
    eval = BKEL_CODE.ganh(new_board, end, eval)
    eval = check_vay(new_board, board[start[0]][start[1]], eval)
    return new_board


def create_one_game(Data: dict):
    list1 = []
    list2 = []
    prev_board = None
    board = BKEL_CODE.start_board
    # print("player 1")
    # print(start_board)
    # print(0)
    # print("-----------------------")
    for i in range(50):
        # print("Luot thu ",i,sep=" ")
        ok,move_first_player = bayes.move(prev_board, board, 1, 0, 0)
        if (move_first_player == None): break
        prev_board = board
        board = GET_BOARD(move_first_player, board)
        temp = BKEL_CODE.encode(board)
        list1.append(temp)
        # print("player 2")
        # print(move_first_player)
        # print_board(board)
        # eval = Eval_Function(board)
        # print(eval)
        # print("-----------------------")
        move_second_player = BKEL_CODE.move(prev_board, board, -1, 0, 0)
        if (move_second_player == None): break
        prev_board = board
        board = GET_BOARD(move_second_player, board)
        temp = BKEL_CODE.encode(board)
        list2.append(temp)
        # print("player 1")
        # print(move_second_player)
        # print_board(board)
        # eval = Eval_Function(board)
        # print(eval)
        # print("-----------------------")
    eval = BKEL_CODE.Eval_Function(board)
    if (eval > 0):
        for x in list1:
            if (x not in Data):
                Data[x] = [0, 0, 0]
            Data[x][0] += 1
        for x in list2:
            if (x not in Data):
                Data[x] = [0, 0, 0]
            Data[x][1] += 1
    elif (eval < 0):
        for x in list1:
            if (x not in Data):
                Data[x] = [0, 0, 0]
            Data[x][1] += 1
        for x in list2:
            if (x not in Data):
                Data[x] = [0, 0, 0]
            Data[x][0] += 1
    else:
        for x in list1:
            if (x not in Data):
                Data[x] = [0, 0, 0]
            Data[x][2] += 1
        for x in list2:
            if (x not in Data):
                Data[x] = [0, 0, 0]
            Data[x][2] += 1


def train():
    workbook = xlsxwriter.Workbook('data.xlsx')
    worksheet = workbook.add_worksheet('Bayes')
    number_of_turn = 5
    game_per_turn = 2
    for i in range(number_of_turn):
        df = pd.read_excel('data.xlsx', sheet_name='Bayes')
        df = pd.DataFrame(df, columns=['A', 'B', 'C', 'D'])
        Data = {}
        df = df.reset_index()  # make sure indexes pair with number of rows
        for index, row in df.iterrows():
            Data[int(row['A'])] = [int(row['B']), int(row['C']), int(row['D'])]
        for j in range(game_per_turn):
            print("Tao Data Van Thu ", game_per_turn * i + j, sep=" ")
            create_one_game(Data)
        worksheet.write(0, 0, "A")
        worksheet.write(0, 1, "B")
        worksheet.write(0, 2, "C")
        worksheet.write(0, 3, "D")
        row = 1
        for x in Data:
            worksheet.write(row, 0, x)
            worksheet.write(row, 1, Data[x][0])
            worksheet.write(row, 2, Data[x][1])
            worksheet.write(row, 3, Data[x][2])
            row += 1
    workbook.close()

train()