import BKEL_CODE
import bayes
import random_bot
import copy
import time
import xlsxwriter
from xlsxwriter import Workbook
#Hàm mã hóa bảng nhằm mục đích hashing qua số để dễ lưu trữ và tìm kiếm nhanh hơn
def encode(table):
    # 1 --> 2
    # 0 --> 1
    # -1 --> 0
    result=0
    for i in range(5):
        for j in range(5):
            result+=(table[i][j]+1)* (3**(i*5+j))
    return result
def decode(hash):
    table = [[0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0],
             [0,0,0,0,0]]
    for i in range(5):
        for j in range(5):
            table[i][j] = hash%3 - 1
            hash /= 3
    return table
def print_board(board):
    for i in range(5):

        for j in range(5):
            if(board[i][j] >= 0 ):
                print(" ",end="")
                print(board[i][j],end=" ")
            else: print(board[i][j],end=" ")
        print()
def check_vay(board,player,eval):
    Visited = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for i in range(5):
        for j in range(5):
            if(Visited[i][j] == False and board[i][j] != 0):
                eval = BKEL_CODE.check_component(board,Visited,(i,j),eval)
    return eval
def GET_BOARD(move,board):
    start = move[0]
    end = move[1]
    new_board = BKEL_CODE.copy.deepcopy(board)
    eval = BKEL_CODE.Eval_Function(board)
    new_board[end[0]][end[1]] = board[start[0]][start[1]]
    new_board[start[0]][start[1]] = 0
    eval = BKEL_CODE.ganh(new_board,end,eval)
    eval = check_vay(new_board,board[start[0]][start[1]],eval)
    return new_board
def play():
    cnt = 0
    prev_board = None
    board = BKEL_CODE.start_board
    time_first = 50
    time_second = 50
    cnt = 0
    for i in range(50):

        print("Người thứ nhất chơi ",i,sep=" ")
        start = time.time()
        move_first_player = random_bot.random_bot(prev_board,board,1,0,0)
        end = time.time()
        dis = end - start
        time_first -= dis
        if(move_first_player == None or time_first < 0):
            print("Kết quả là người thứ hai thắng")
            return
        prev_board = board
        board = GET_BOARD(move_first_player,board)
        print(move_first_player)
        print_board(board)
        #----------------------------------------------------#
        print("Người thứ hai chơi ",i,sep=" ")
        start = time.time()
        ok,move_second_player = bayes.move(prev_board,board,-1,0,0)
        if(ok == True): cnt += 1
        end = time.time()
        dis = end - start
        time_second -= dis
        if(move_second_player == None or time_second < 0):
            print("Kết quả là người thứ nhất thắng")
            return
        prev_board = board
        board = GET_BOARD(move_second_player,board)
        print(move_second_player)
        print_board(board)
    eval = BKEL_CODE.Eval_Function(board)
    if(eval == 0):
        print("Kết quả của trò chơi là hòa")
        print(cnt)
    elif(eval > 0):
        print("Kết quả là người  1 thắng")
        print(cnt)
    else:
        print("Kết quả là người -1 thắng")
        print(cnt)
def create_one_game(Data:dict):
    list1 = []
    list2 = []
    prev_board = None
    board = BKEL_CODE.start_board
    # print("player 1")
    # print(start_board)
    # print(0)
    # print("-----------------------")
    for i in range(50):
        #print("Luot thu ",i,sep=" ")
        move_first_player = BKEL_CODE.move(prev_board,board,1,0,0)
        if(move_first_player == None): break
        prev_board = board
        board = GET_BOARD(move_first_player,board)
        temp = encode(board)
        list1.append(temp)
        # print("player 2")
        # print(move_first_player)
        # print_board(board)
        # eval = Eval_Function(board)
        # print(eval)
        # print("-----------------------")
        move_second_player = BKEL_CODE.move(prev_board,board,-1,0,0)
        if(move_second_player == None): break
        prev_board = board
        board = GET_BOARD(move_second_player,board)
        temp = encode(board)
        list2.append(temp)
        # print("player 1")
        # print(move_second_player)
        # print_board(board)
        # eval = Eval_Function(board)
        # print(eval)
        # print("-----------------------")
    eval = BKEL_CODE.Eval_Function(board)
    if(eval > 0):
        for x in list1:
            if(x not in Data):
                Data[x] = [0,0,0]
            Data[x][0] += 1
        for x in list2:
            if (x not in Data):
                Data[x] = [0,0,0]
            Data[x][1] += 1
    elif(eval < 0):
        for x in list1:
            if(x not in Data):
                Data[x] = [0,0,0]
            Data[x][1] += 1
        for x in list2:
            if (x not in Data):
                Data[x] = [0,0,0]
            Data[x][0] += 1
    else:
        for x in list1:
            if(x not in Data):
                Data[x] = [0,0,0]
            Data[x][2] += 1
        for x in list2:
            if (x not in Data):
                Data[x] = [0,0,0]
            Data[x][2] += 1
def create_data():
    workbook = xlsxwriter.Workbook('data.xlsx')
    worksheet = workbook.add_worksheet('Bayes')
    Data = {}
    number_of_game = 100
    for i in range(number_of_game):
        print("Tao Data Van Thu ",i,sep=" ")
        create_one_game(Data)
    worksheet.write(0,0,"A")
    worksheet.write(0,1,"B")
    worksheet.write(0,2,"C")
    worksheet.write(0,3,"D")
    row = 1
    for x in Data:
        worksheet.write(row,0,x)
        worksheet.write(row,1,Data[x][0])
        worksheet.write(row,2,Data[x][1])
        worksheet.write(row,3,Data[x][2])
        row += 1
    workbook.close()

create_data()
#play()