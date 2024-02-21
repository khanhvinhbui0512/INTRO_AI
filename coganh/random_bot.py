from BKEL_CODE import *
def random_bot(prev_board, board, player, remain_time_x, remain_time_o):
    list_move = []
    eval = Eval_Function(board)
    if(eval == -16*player): return None
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
        if(cnt == 2):
            ok = False
            for index in available_move[pre_move[0][0]][pre_move[0][1]]:
                if(board[index[0]][index[1]] == player):
                    new_board = copy.deepcopy(board)
                    new_board[index[0]][index[1]] = 0
                    new_board[pre_move[0][0]][pre_move[0][1]] = player
                    temp_eval = ganh(new_board,pre_move[0],eval)
                    if(temp_eval*player > eval*player):
                        ok = True
                        list_move.append((index,pre_move[0]))           
            if(ok == True):
                return list_move[secrets.randbelow(len(list_move))]
    for i in range(5):
            for j in range(5):
                if (board[i][j] == player):
                    for index in available_move[i][j]:
                        if board[index[0]][index[1]] == 0:
                            list_move.append(((i,j),index))
    return list_move[secrets.randbelow(len(list_move))]