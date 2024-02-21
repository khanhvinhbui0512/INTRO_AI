import secrets
import time
import copy
import random
start_board =  [[1, 1, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 0, 0, 0, -1],
                [-1, 0, 0, 0, -1],
                [-1, -1, -1, -1, -1]]
available_move = [[[(1, 0), (0, 1), (1, 1)],
                   [(1, 1), (0, 2), (0, 0)],
                   [(1, 2), (0, 3), (0, 1), (1, 1), (1, 3)],
                   [(1, 3), (0, 4), (0, 2)],
                   [(1, 4), (0, 3), (1, 3)]],
                  [[(2, 0), (1, 1), (0, 0)],
                   [(2, 1), (1, 2), (1, 0), (0, 1), (0, 0), (0, 2), (2, 0), (2, 2)],
                   [(2, 2), (1, 3), (1, 1), (0, 2)],
                   [(2, 3), (1, 4), (1, 2), (0, 3), (0, 2), (0, 4), (2, 2), (2, 4)],
                   [(2, 4), (1, 3), (0, 4)]],
                   [[(3, 0), (2, 1), (1, 0), (1, 1), (3, 1)],
                   [(3, 1), (2, 2), (2, 0), (1, 1)],
                   [(3, 2), (2, 3), (2, 1), (1, 2), (1, 1), (1, 3), (3, 1), (3, 3)],
                   [(3, 3), (2, 4), (2, 2), (1, 3)],
                   [(3, 4), (2, 3), (1, 4), (1, 3), (3, 3)]],
                   [[(4, 0), (3, 1), (2, 0)],
                   [(4, 1), (3, 2), (3, 0), (2, 1), (2, 0), (2, 2), (4, 0), (4, 2)],
                   [(4, 2), (3, 3), (3, 1), (2, 2)],
                   [(4, 3), (3, 4), (3, 2), (2, 3), (2, 2), (2, 4), (4, 2), (4, 4)],
                   [(4, 4), (3, 3), (2, 4)]],
                   [[(4, 1), (3, 0), (3, 1)],
                   [(4, 2), (4, 0), (3, 1)],
                   [(4, 3), (4, 1), (3, 2), (3, 1), (3, 3)],
                   [(4, 4), (4, 2), (3, 3)],
                   [(4, 3), (3, 4), (3, 3)]]]


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
#Hàm đánh giá lợi thế
def Eval_Function(board):
    sum = 0
    # Tính tổng của các quân trên bảng nếu tổng âm thì nghiêng về -1 và dương thì nghiêng về 1
    for i in range(5):
        for j  in range(5):
            sum += board[i][j]
    return sum

# Hàm kiểm tra trường gánh với board là bảng chơi, move là vị trí di chuyển và eval là tổng các số trên bảng
def ok_inside(x,y):
    if(0 <= x and x <= 4 and 0 <= y and y <= 4): return True
def ganh(board, pos, eval : int):
    #Lưu vị trí quân cờ di chuyển tới sau khi move
    pos_x = pos[0]
    pos_y = pos[1]
    #Nếu vị trí ở ngoài biên thì không gánh được
    if((pos_x+pos_y)%2 == 1):
        #Trường hợp gánh năm dọc
        if(ok_inside(pos_x+1,pos_y) and ok_inside(pos_x-1,pos_y)):
            if (board[pos_x][pos_y] == -board[pos_x + 1][pos_y] and board[pos_x][pos_y] == -board[pos_x - 1][pos_y]):
                eval += 4 * board[pos_x][pos_y]
                board[pos_x + 1][pos_y] = copy.deepcopy(board[pos_x][pos_y])
                board[pos_x - 1][pos_y] = copy.deepcopy(board[pos_x][pos_y])
         #Trường hợp gánh năm ngang
        if (ok_inside(pos_x, pos_y + 1) and ok_inside(pos_x, pos_y - 1)):
            if(board[pos_x][pos_y] == -board[pos_x][pos_y + 1] and board[pos_x][pos_y] == -board[pos_x][pos_y - 1]):
                eval += 4*board[pos_x][pos_y]
                board[pos_x][pos_y+1] = copy.deepcopy(board[pos_x][pos_y])
                board[pos_x][pos_y-1] = copy.deepcopy(board[pos_x][pos_y])
    else:
         #Trường hợp gánh năm dọc
        if (ok_inside(pos_x + 1, pos_y) and ok_inside(pos_x - 1, pos_y)):
            if(board[pos_x][pos_y] == -board[pos_x + 1][pos_y] and board[pos_x][pos_y] == -board[pos_x - 1][pos_y]):
                eval += 4*board[pos_x][pos_y]
                board[pos_x + 1][pos_y] = copy.deepcopy(board[pos_x][pos_y])
                board[pos_x - 1][pos_y] = copy.deepcopy(board[pos_x][pos_y])
        #Trường hợp gánh năm ngang
        if (ok_inside(pos_x, pos_y + 1) and ok_inside(pos_x, pos_y - 1)):
            if(board[pos_x][pos_y] == -board[pos_x][pos_y + 1] and board[pos_x][pos_y] == -board[pos_x][pos_y - 1]):
                eval += 4*board[pos_x][pos_y]
                board[pos_x][pos_y+1] = copy.deepcopy(board[pos_x][pos_y])
                board[pos_x][pos_y-1] = copy.deepcopy(board[pos_x][pos_y])
        #Trường hợp gánh dấu sắc
        if (ok_inside(pos_x + 1, pos_y + 1) and ok_inside(pos_x - 1, pos_y - 1)):
            if(board[pos_x][pos_y] == -board[pos_x + 1][pos_y + 1] and board[pos_x][pos_y] == -board[pos_x - 1][pos_y - 1]):
                eval += 4*board[pos_x][pos_y]
                board[pos_x + 1][pos_y + 1] = copy.deepcopy(board[pos_x][pos_y])
                board[pos_x - 1][pos_y - 1] = copy.deepcopy(board[pos_x][pos_y])
        #Trường hợp gánh dấu huyền
        if (ok_inside(pos_x - 1, pos_y + 1) and ok_inside(pos_x + 1, pos_y - 1)):
            if(board[pos_x][pos_y] == -board[pos_x - 1][pos_y + 1] and board[pos_x][pos_y] == -board[pos_x + 1][pos_y - 1]):
                eval += 4*board[pos_x][pos_y]
                board[pos_x - 1][pos_y+1] = copy.deepcopy(board[pos_x][pos_y])
                board[pos_x + 1][pos_y-1] = copy.deepcopy(board[pos_x][pos_y])
    return eval


def check_component(board,Visited,pos,eval):
    value = board[pos[0]][pos[1]]
    # Nơi để lưu trữ các ô cùng màu được liên kết với ô có vị trí pos
    component = []
    # Hàng đợi để dùng BFS duyệt qua các ô
    queue = []
    queue.append((pos[0],pos[1]))
    component.append((pos[0],pos[1]))
    Visited[pos[0]][pos[1]] = 1
    #ans = True nếu trong bảng chơi các ô liên kết với ô có vị trí pos sẽ không bị vây
    #ans = False nếu trong bảng chơi các ô liên kết với ô có vị trí pos bị vây
    ans = False
    while(len(queue) > 0):
        # Lấy các giá trị thuộc đầu hàng đợi
        temp = queue[0]
        queue.pop(0)
        for index in available_move[temp[0]][temp[1]]:
            #Không duyệt các giá trị đã đi qua
            if Visited[index[0]][index[1]] != 0: continue
            #Nếu có ô liên kết với ô trống nghĩa là sẽ không bị vây
            if(board[index[0]][index[1]]==0):
                ans = True
            #Nếu có ô tiếp theo cùng màu với ô pos thì sẽ duyệt ô đó tiếp
            elif (board[index[0]][index[1]] == value):
                Visited[index[0]][index[1]] = 1
                queue.append(index)
                component.append(index)
    # Đổi các quân bị vây thành các quân vây nó
    if(ans == False):
        for index in component:
            board[index[0]][index[1]] = -value
        eval -= len(component) * 2 * value
        return eval
    return eval
# Hàm kiểm tra trường vây với board là bảng chơi, move là vị trí di chuyển và eval là tổng các số trên bảng
def vay(board,pos, eval : int):
    #Mảng hai chiều lưu các vị trí đã đi qua
    Visited = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    #Lưu vị trí quân cờ di chuyển tới sau khi move
    pos_x = pos[0]
    pos_y = pos[1]
    for index in available_move[pos_x][pos_y]:
        #Nếu muốn vây được thì nhưng ô kề nó sẽ phải khác màu với nó và chưa được đi qua
        if(board[index[0]][index[1]] == -board[pos_x][pos_y] and Visited[index[0]][index[1]] == 0):
            #Kiểm tra ô kế bên có nằm trong trường hợp hay không. Nếu có thì sẽ thay đổi trong hàm.
            eval = check_component(board,Visited,(index[0],index[1]),eval)
    return eval
def Move_To(board,start,end,eval):
    new_board = copy.deepcopy(board)
    new_board[end[0]][end[1]] = board[start[0]][start[1]]
    new_board[start[0]][start[1]] = 0
    eval = ganh(new_board,end,eval)
    eval = vay(new_board,end,eval)
    return new_board,eval

def minimax(prev_board, board, eval, player, depth, eval_parent):
    if (depth <= 0): return eval, ((0, 0), (0, 0))
    res = -20 * player
    pos = ((0, 0), (0, 0))
    if prev_board != None:
        pos1 = ()
        pos2 = ()
        cnt = 0
        for i in range(5):
            for j in range(5):
                if (prev_board[i][j] != board[i][j]):
                    cnt += 1
                    if (prev_board[i][j] == 0):
                        pos1 = (i,j)
                    if (prev_board[i][j] == -player):
                        pos2 = (i,j)
        pre_move = (pos2,pos1)
        if (cnt == 2):
            ok = False
            for index in available_move[pre_move[0][0]][pre_move[0][1]]:
                if (board[index[0]][index[1]] == player):
                    new_board = copy.deepcopy(board)
                    new_board[index[0]][index[1]] = 0
                    new_board[pre_move[0][0]][pre_move[0][1]] = player
                    temp_eval = ganh(new_board, pre_move[0], eval)
                    if(player == 1):
                        if(temp_eval > eval):
                            ok = True
                            temp_eval = ganh(new_board, pre_move[0], eval)
                            tmp_res, tmp_pos = minimax(board, new_board, temp_eval, -player, depth-0.75,20 * player)
                            if ( tmp_res >  res):
                                res = tmp_res
                                pos = (index, pre_move[0])
                    else:
                        if (temp_eval < eval):
                            ok = True
                            temp_eval = ganh(new_board, pre_move[0], eval)
                            tmp_res, tmp_pos = minimax(board, new_board, temp_eval, -player, depth-0.75,20 * player)
                            if (tmp_res < res):
                                res = tmp_res
                                pos = (index, pre_move[0])
            if (ok == True):
                return res, pos

    temp = [[(res, None), (res, None), (res, None), (res, None), (res, None)],
            [(res, None), (res, None), (res, None), (res, None), (res, None)],
            [(res, None), (res, None), (res, None), (res, None), (res, None)],
            [(res, None), (res, None), (res, None), (res, None), (res, None)],
            [(res, None), (res, None), (res, None), (res, None), (res, None)]]
    if (player == 1):
        for i in range(5):
            for j in range(5):
                if (board[i][j] == player):
                    for index in available_move[i][j]:
                        if board[index[0]][index[1]] == 0:
                            new_board, calc = Move_To(board, (i, j), index, eval)
                            tmp_res, tmp_pos = minimax(board,new_board, calc, -player, depth - 1, res)
                            if (tmp_res > temp[i][j][0]):
                                temp[i][j] = (tmp_res, ((i, j), index))
                            if (tmp_res > res):
                                res = tmp_res
                            if (res > eval_parent):
                                return res, pos
    else:
        for i in range(5):
            for j in range(5):
                if (board[i][j] == player):
                    for index in available_move[i][j]:
                        if board[index[0]][index[1]] == 0:
                            new_board, calc = Move_To(board, (i, j), index, eval)
                            tmp_res, tmp_pos = minimax(board,new_board, calc, -player, depth - 1, res)
                            if (tmp_res < temp[i][j][0]):
                                temp[i][j] = (tmp_res, ((i, j), index))
                            if (tmp_res < res):
                                res = tmp_res
                            if (res < eval_parent):
                                return res, pos
    ans = []
    for i in range(5):
        for j in range(5):
            if (temp[i][j][0] == res):
                ans.append(temp[i][j][1])
    return res, ans[secrets.randbelow(len(ans))]


'''
def move(prev_board, board, player, remain_time_x, remain_time_o):
    eval = Eval_Function(board)
    if(eval == -player*16): return None
    res, move = minimax(prev_board, board, eval, player, 4, 20 * player)
    return move
'''

def list_moves(prev_board, board, player):
    list_move = []
    eval = Eval_Function(board)

    if prev_board != None:
        pos1 = ()
        pos2 = ()
        cnt = 0
        for i in range(5):
            for j in range(5):
                if (prev_board[i][j] != board[i][j]):
                    cnt += 1
                    if (prev_board[i][j] == 0):
                        pos1 = (i, j)
                    if (prev_board[i][j] == -player):
                        pos2 = (i, j)
        pre_move = (pos2, pos1)
        if (cnt == 2):
            ok = False
            for index in available_move[pre_move[0][0]][pre_move[0][1]]:
                if (board[index[0]][index[1]] == player):
                    new_board = copy.deepcopy(board)
                    new_board[index[0]][index[1]] = 0
                    new_board[pre_move[0][0]][pre_move[0][1]] = player
                    temp_eval = ganh(new_board, pre_move[0], eval)
                    if (player == 1):
                        if (temp_eval > eval):
                            ok = True
                            list_move.append((index, pre_move[0]))
                            # move = (index, pre_move[0])

                    else:
                        if (temp_eval < eval):
                            ok = True
                            list_move.append((index, pre_move[0]))
                            # move = (index, pre_move[0])

            if (ok == True):
                # list_move.append(move)
                return True, list_move

    if player == 1:
        for i in range(5):
            for j in range(5):
                if board[i][j] == player:
                    for index in available_move[i][j]:
                        if board[index[0]][index[1]] == 0:
                            move = ((i, j), index)
                            list_move.append(move)
    else:
        for i in range(5):
            for j in range(5):
                if board[i][j] == player:
                    for index in available_move[i][j]:
                        if board[index[0]][index[1]] == 0:
                            move = ((i, j), index)
                            list_move.append(move)

    return False, list_move

import pandas as pd
df = pd.read_excel('data.xlsx', sheet_name='Bayes')
df = pd.DataFrame(df,columns=['A','B','C','D'])
dict = {}
df = df.reset_index()  # make sure indexes pair with number of rows
for index, row in df.iterrows():
    dict[row['A']] = row['B'] / (row['B'] + row['C'] + row['D'])

print('Successfully loaded data')

def move(prev_board, board, player, remain_time_x, remain_time_o):
    is_mo, new_moves = list_moves(prev_board, board, player)
    is_bayes = True
    best_val = 0
    best_move = None
    for move in new_moves:
        new_board = copy.deepcopy(board)
        new_board[move[0][0]][move[0][1]] = 0
        new_board[move[1][0]][move[1][1]] = player
        val = encode(new_board)
        if val in dict.keys():
            val = dict[val]
        else:
            val = 0
        if (val > best_val):
            best_val = val
            best_move = move
        if (val > 0 and val == best_val):
            if (random.random() > 0.5):
                best_move = move

    # print(is_mo)
    # print(new_moves)
    
    if (best_move == None and is_mo == False):
        is_bayes = False
        eval = Eval_Function(board)
        if(eval == -player*16): return None
        res, best_move = minimax(prev_board, board, eval, player, 4, 20 * player)
    elif (best_move == None):
        return 'a', new_moves[secrets.randbelow(len(new_moves))]
    return is_bayes, best_move