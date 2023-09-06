'''
dx = [1,0,0,-1,-1,-1,1,1]
dy = [0,1,-1,0,-1,1,-1,1]
#Code tạo bảng available_move
for i in range(5):
    for j in range(5):
        if((i+j)%2 == 0):
            for k in range(8):
                if(0 <= i + dx[k] and i + dx[k] <= 4 and 0<= j + dy[k]  and j + dy[k] <=4):
                    available_move[i][j].append((i + dx[k],j + dy[k]))
        else:
            for k in range(4):
                if(0 <= i + dx[k] and i + dx[k] <= 4 and 0<= j + dy[k]  and j + dy[k] <=4):
                    available_move[i][j].append((i + dx[k],j + dy[k]))
print(available_move)
'''
import secrets
import copy
from time import time
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

def ganh(board, pos, eval : int):
    #Lưu vị trí quân cờ di chuyển tới sau khi move
    pos_x = pos[0]
    pos_y = pos[1]
    #Nếu vị trí ở ngoài biên thì không gánh được
    if(pos_x == 0 or pos_y == 0 or pos_x == 4 or pos_y == 4): return eval
    elif((pos_x+pos_y)%2 == 1):
        #Trường hợp gánh năm dọc
        if(board[pos_x][pos_y] == -board[pos_x + 1][pos_y] and board[pos_x][pos_y] == -board[pos_x - 1][pos_y]):
            eval += 4*board[pos_x][pos_y]
            board[pos_x + 1][pos_y] = copy.deepcopy(board[pos_x][pos_y])
            board[pos_x - 1][pos_y] = copy.deepcopy(board[pos_x][pos_y])
         #Trường hợp gánh năm ngang
        if(board[pos_x][pos_y] == -board[pos_x][pos_y + 1] and board[pos_x][pos_y] == -board[pos_x][pos_y - 1]):
            eval += 4*board[pos_x][pos_y]
            board[pos_x][pos_y+1] = copy.deepcopy(board[pos_x][pos_y])
            board[pos_x][pos_y-1] = copy.deepcopy(board[pos_x][pos_y])
    else:
         #Trường hợp gánh năm dọc
        if(board[pos_x][pos_y] == -board[pos_x + 1][pos_y] and board[pos_x][pos_y] == -board[pos_x - 1][pos_y]):
            eval += 4*board[pos_x][pos_y]
            board[pos_x + 1][pos_y] = copy.deepcopy(board[pos_x][pos_y])
            board[pos_x - 1][pos_y] = copy.deepcopy(board[pos_x][pos_y])
        #Trường hợp gánh năm ngang
        if(board[pos_x][pos_y] == -board[pos_x][pos_y + 1] and board[pos_x][pos_y] == -board[pos_x][pos_y - 1]):
            eval += 4*board[pos_x][pos_y]
            board[pos_x][pos_y+1] = copy.deepcopy(board[pos_x][pos_y])
            board[pos_x][pos_y-1] = copy.deepcopy(board[pos_x][pos_y])
        #Trường hợp gánh dấu sắc
        if(board[pos_x][pos_y] == -board[pos_x + 1][pos_y + 1] and board[pos_x][pos_y] == -board[pos_x - 1][pos_y - 1]):
            eval += 4*board[pos_x][pos_y]
            board[pos_x + 1][pos_y + 1] = copy.deepcopy(board[pos_x][pos_y])
            board[pos_x - 1][pos_y - 1] = copy.deepcopy(board[pos_x][pos_y])
        #Trường hợp gánh dấu huyền
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
# def minimax(board,start_x,start_y,eval,player,depth,parent):
#     if(eval*player == -16 or depth == 0): return eval,(start_x,start_y)
#     res = -20*player
#     pos = (0,0)
#     if(player == 1):
#         for index in available_move[start_x][start_y]:
#             if board[index[0]][index[1]] == 0:
#                 new_board, calc = Move_To(board, (start_x, start_y), index, eval)
#                 tmp_res, tmp_pos = minimax(new_board, index[0], index[1], calc, -player, depth - 1, res)
#                 if (tmp_res > res):
#                     res = tmp_res
#                     pos = (index[0], index[1])
#                 if (res > parent):
#                     return res, pos
#
#     else:
#         for index in available_move[start_x][start_y]:
#             if board[index[0]][index[1]] == 0:
#                 new_board, calc = Move_To(board, (start_x, start_y), index, eval)
#                 tmp_res, tmp_pos = minimax(new_board, index[0], index[1], calc, -player, depth - 1, res)
#                 if (tmp_res < res):
#                     res = tmp_res
#                     pos = (index[0], index[1])
#                 if (res < parent):
#                     return res, pos
#     return res, pos

def minimax(prev_board,board,eval,player,depth,eval_parent):
    if(depth == 0): return eval,((0,0),(0,1))
    res = -20*player
    pos = ((0,0),(0,0))
    if prev_board != None:
        pre_move = ((0,0),(0,0))
        cnt = 0
        for i in range(5):
            for j in range(5):
                if(prev_board[i][j] != board[i][j]):
                    cnt += 1
                    if(prev_board[i][j] == 0):
                        pre_move[1] = (i,j)
                    if(pre_move[i][j] == -player):
                        pre_move[0] = (i,j) 
        if(cnt == 2):
            ok = False
            for index in available_move[pre_move[0][0]][pre_move[0][1]]:
                if(board[index[0]][index[1]] == player):
                    new_board = copy.deepcopy(board)
                    new_board[index[0]][index[1]] = 0
                    new_board[pre_move[0][0]][pre_move[0][1]] = player
                    temp_eval = ganh(new_board,pre_move[0],eval)
                    if(temp_eval > eval):
                        ok = True
                        temp_eval = ganh(new_board,pre_move[0],eval)
                        tmp_res, tmp_pos = minimax(board,new_board,temp_eval,-player,depth-1,20*player)
                        if(player*tmp_res > player * res):
                            res = tmp_res
                            pos = (index,pre_move[0])
            if(ok == True):
                return res, pos
    
    temp = [[(res,pos),(res,pos),(res,pos),(res,pos),(res,pos)],
            [(res,pos),(res,pos),(res,pos),(res,pos),(res,pos)],
            [(res,pos),(res,pos),(res,pos),(res,pos),(res,pos)],
            [(res,pos),(res,pos),(res,pos),(res,pos),(res,pos)],
            [(res,pos),(res,pos),(res,pos),(res,pos),(res,pos)]]
    if (player == 1):
        for i in range(5):
            for j in range(5):
                if (board[i][j] == player):
                    for index in available_move[i][j]:
                        if board[index[0]][index[1]] == 0:
                            new_board, calc = Move_To(board, (i,j), index, eval)
                            tmp_res, tmp_pos = minimax(new_board, calc, -player, depth - 1,res)
                            if(tmp_res > temp[i][j][0]):
                                temp[i][j] = (tmp_res,((i,j),index))
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
                            new_board, calc = Move_To(board, (i,j), index, eval)
                            tmp_res, tmp_pos = minimax(new_board, calc, -player, depth - 1,res)
                            if(tmp_res < temp[i][j][0]):
                                temp[i][j] = (tmp_res, ((i, j), index))
                            if (tmp_res < res):
                                res = tmp_res
                            if (res < eval_parent):
                                return res, pos
    ans = []
    for i in range(5):
        for j in range(5):
            if(temp[i][j][0] == res):
                ans.append(temp[i][j][1])
    return res,ans[secrets.randbelow(len(ans))]
#cnt = 0
remain_time_x = 50
remain_time_o = 50
def move(prev_board, board, player, remain_time_x, remain_time_o):
    eval = Eval_Function(board)
    res,move = minimax(prev_board,board,eval,player,3,20*player)
    return move
def print_board(board):
    for i in range(5):

        for j in range(5):
            if(board[i][j] >= 0 ):
                print(" ",end="")
                print(board[i][j],end=" ")
            else: print(board[i][j],end=" ")
        print()
