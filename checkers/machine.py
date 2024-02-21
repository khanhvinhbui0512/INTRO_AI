import copy
import random
import math
import minimax
INFINITY =1000
NUMPAWN = 12
dx = [1,1,-1,-1]
dy = [1,-1,1,-1]

base_table = [
    [ 0, 1, 0, 1, 0, 1, 0, 1],
    [ 1, 0, 1, 0, 1, 0, 1, 0],
    [ 0, 1, 0, 1, 0, 1, 0, 1],
    [ 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0],
    [-1, 0,-1, 0,-1, 0,-1, 0],
    [ 0,-1, 0,-1, 0,-1, 0,-1],
    [-1, 0,-1, 0,-1, 0,-1, 0],
]
def getSign(number):
    if number > 0:
        return 1
    if number < 0:
        return - 1
    return 0
class Parameter:
    list_weight = [0.9999855327759305, 0.9999870380628723, 0.9999872071179255, 0.9999875447066681, 0.9999854983419103, 0.999986014999549, 0.999987130569303, 0.9999887602519039, 0.9999857547620185, 0.999986549217341, 0.9999884626120673, 0.999988474372385, 0.9999856077541064, 0.9999867696237362, 0.999987297800645, 0.9999858231454885, 0.99998551701236, 0.999986840976078, 0.9999863381847546, 0.9999867560401745, 0.9999860019103499, 0.9999869165223925, 0.9999868961867008, 0.9999860866534597, 0.9999860967943781, 0.9999870169249638, 0.9999862607631436, 0.9999863238820369, 0.9999861530934044, 0.9999877405102778, 0.9999888247641078, 0.9999885058178156]
    player = 1
    learning_rate = 0.1
class Properties:
    empty = 0
    white = 1
    black = -1
    king = 2
    win = True
    lose = False
class point:
    def __init__(self,_x:int,_y:int):
        self.x = _x
        self.y = _y
class move:
    def __init__(self,_move: list[point]):
        self.move = _move
class state:
    def __init__(self,table:list[list[int]]):
        self.table = table
def activate_function(num):
    return 1/(1+math.exp(-num))
def count(table:list[list[int]]):
    cntWhite = 0
    cntBlack = 0
    for i in range(len(table)):
        for j in range(len(table)):
            if (table[i][j] < 0): cntBlack += 1
            if (table[i][j] > 0): cntWhite += 1
    return cntWhite,cntBlack
def take_value(table:list[list[int]]):
    list_val = []
    for i in range(len(table)):
        for j in range(len(table)):
            if((i+j)%2 == 1): list_val.append(activate_function(table[i][j]))
    return list_val
class checker:
    def __init__(self,_table:list[list[int]],_player:int):
        self.size = len(_table)
        self.table = copy.deepcopy(_table)
        self.player = _player
    def random_bot(self):
        allMoves = self.get_all_move(state(self.table),self.player)
        if(len(allMoves) == 0):
            return False
        move = allMoves[random.randint(0,len(allMoves)-1)]
        self.process(move)
        return move
    def legal_pos(self, row:int, col:int):
        if (0 <= row < self.size and 0 <= col < self.size):
            return True
        return False
    def get_eat_move(self,node:state,pos:point,maximizingPlayer):
        ans = []
        for i in range(4):
            jumpPosR = pos.x + 2*dx[i]
            jumpPosC = pos.y + 2*dy[i]
            if(node.table[pos.x][pos.y] == Properties.white):
                if(i >= 2): continue
            if(node.table[pos.x][pos.y] == Properties.black):
                if(i <= 1): continue
            eatR = pos.x + dx[i]
            eatC = pos.y + dy[i]
            if(self.legal_pos(jumpPosR,jumpPosC) and (node.table[jumpPosR][jumpPosC] == 0)
                    and (node.table[eatR][eatC]*maximizingPlayer < 0)):
                jump_node = copy.deepcopy(node)
                jump_pos = point(jumpPosR,jumpPosC)
                if(self.is_end_border(jump_pos)):
                    jump_node.table[jumpPosR][jumpPosC] = Properties.king*getSign(maximizingPlayer)
                else:
                    jump_node.table[jumpPosR][jumpPosC] = node.table[pos.x][pos.y] #use previous state
                jump_node.table[eatR][eatC] = 0
                jump_node.table[pos.x][pos.y] = 0
                list_eat = self.get_eat_move(jump_node,jump_pos,maximizingPlayer)
                if(list_eat == []): ans.append([jump_pos])
                else:
                    for element in list_eat:
                        for i in range(len(element)):
                            ans.append([jump_pos] + element[0:i+1])
        return ans
    def get_all_move(self,node:state,maximizingPlayer):
        all_move = []
        for row in range(self.size):
            for col in range(self.size):
                if(getSign(node.table[row][col]) == getSign(maximizingPlayer)):
                    for i in range(4):
                        posR = row + dx[i]
                        posC = col + dy[i]
                        if (node.table[row][col] == Properties.white):
                            if (i >= 2): continue
                        if (node.table[row][col] == Properties.black):
                            if (i <= 1): continue
                        if (self.legal_pos(posR, posC) and (node.table[posR][posC] == 0)):
                            all_move.append(move([point(row, col), point(posR, posC)]))
                    list_eat = self.get_eat_move(node,point(row,col),maximizingPlayer)
                    for element in list_eat:
                        for i in range(len(element)):
                            all_move.append(move([point(row,col)] + element[0:i+1]))
        return all_move

    def heuristic(self,node:state,maximizingPlayer:int):
        cntWhite,cntBlack = count(node.table)
        if(cntWhite == 0): return -INFINITY
        if(cntBlack == 0): return INFINITY
        list_val = take_value(node.table)
        eval = 0
        for i in range(32):
            eval += Parameter.list_weight[i]*list_val[i]
        output = activate_function(eval+Parameter.player*activate_function(maximizingPlayer))
        return 2*output- 1
    def minimax(self,node:state,depth:int, alpha:float,beta:float, maximizingPlayer):
        if(depth == 0):
            return self.heuristic(node,maximizingPlayer), move([])
        else:
            final_move = move([])
            all_move = self.get_all_move(node,maximizingPlayer)
            if len(all_move) > 0: final_move= all_move[0]
            if maximizingPlayer == 1:
                maxEval = -INFINITY
                for i in range(len(all_move)):
                    jump_node = copy.deepcopy(node)
                    self.process_move(all_move[i],jump_node)
                    eval, temp = self.minimax(jump_node,depth-1,alpha,beta,-maximizingPlayer)
                    if(eval > maxEval):
                        maxEval = eval
                        final_move = all_move[i]
                        alpha = max(alpha, maxEval)
                    if(beta <= alpha): break
                return maxEval, final_move
            else:
                minEval = INFINITY
                for i in range(len(all_move)):
                    jump_node = copy.deepcopy(node)
                    self.process_move(all_move[i],jump_node)
                    eval, temp = self.minimax(jump_node,depth-1,alpha,beta,-maximizingPlayer)
                    if(eval < minEval):
                        minEval = eval
                        final_move = all_move[i]
                        beta = min(beta, minEval)
                    if(beta <= alpha): break
                return minEval, final_move
    def is_end_border(self,pos:point):
        if (pos.x == 0 or pos.x == self.size - 1):
            return True
        return False

    def update_pawn_cut(self, start:point, des:point,node:state):
        node.table[start.x][start.y] = Properties.empty
        x_cut_pos = int((start.x + des.x) / 2)
        y_cut_pos = int((start.y + des.y) / 2)
        node.table[x_cut_pos][y_cut_pos] = Properties.empty
        return self.is_end_border(des)

    def update_not_pawn_cut(self, lstPos:move,node:state):
        firstItem = lstPos.move[0]
        secondItem = lstPos.move[1]
        dis = abs(firstItem.x - secondItem.x) + abs(firstItem.y - secondItem.y)
        if (dis == 2):
            prevState = node.table[firstItem.x][firstItem.y]
            node.table[firstItem.x][firstItem.y] = Properties.empty
            if (self.is_end_border(secondItem) == True):
                node.table[secondItem.x][secondItem.y] = Properties.king * getSign(prevState)
            else:
                node.table[secondItem.x][secondItem.y] = prevState
            return True
        return False

    def process_move(self, lstPos:move,node:state):
        if (len(lstPos.move) == 2 and self.update_not_pawn_cut(lstPos,node) == True): pass
        else:
            firstMove = lstPos.move[0]
            finalMove = lstPos.move[-1]
            prevState = node.table[firstMove.x][firstMove.y]
            wasReachEndBorder = False
            for i in range(len(lstPos.move) - 1):
                wasReachEndBorder += self.update_pawn_cut(lstPos.move[i], lstPos.move[i + 1],node)
            if (wasReachEndBorder == True):
                node.table[finalMove.x][finalMove.y] = Properties.king * getSign(prevState)
            else:
                node.table[finalMove.x][finalMove.y] = prevState
        return None
    def process(self,lstPos:move):
        self.process_move(lstPos,state(self.table))
    def count(self):
        cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                if(self.table[i][j] != 0): cnt += 1
        return cnt
    def find_move(self,level:int):
        if(self.count() <= 6):
            eval, lstPos = self.minimax(state(self.table), level*1.5, -INFINITY, INFINITY, self.player)
        else:
            eval,lstPos = self.minimax(state(self.table),level,-INFINITY,INFINITY,self.player)
        if len(lstPos.move) == 0 or type(lstPos) is bool:
            return Properties.lose
        self.process(lstPos)
        return lstPos

def SGD(list_board,target):
    for i in range(len(list_board)):
        list_eval= take_value(list_board[i][0])
        player = activate_function(list_board[i][1])
        eval = 0
        for i in range(32):
            eval += Parameter.list_weight[i]*list_eval[i]
        output = activate_function(eval+Parameter.player*player)
        sigma = []
        delta = []
        sigmaOut = output * (1 - output) * (target - output)
        for i in range(32):
            sigma.append(list_eval[i]*(1-list_eval[i])*Parameter.list_weight[i]*sigmaOut)
            delta.append(Parameter.learning_rate*sigma[i]*output)
            Parameter.list_weight[i] += delta[i]
        sigmaPlayer = player * (1 - player) * Parameter.player * sigmaOut
        deltaPlayer = Parameter.learning_rate*sigmaPlayer*output
        Parameter.player += deltaPlayer
    print(Parameter.list_weight)

def train():
    cnt = 0
    game1 = checker(base_table,-1)
    game2 = checker(base_table,1)
    list_board = []
    while(True):
        print(cnt,end=" ")
        if(cnt == 120 or list_board.count([game1.table,1]) == 3):
            cntWhite, cntBlack = count(game1.table)
            if(cntWhite  > cntBlack):
                print("\n 2- thang")
                SGD(list_board, 1)
            elif(cntWhite  < cntBlack):
                print("\n 1- thang")
                SGD(list_board,0)
            else:
                print("\n Hoa")
                SGD(list_board,0.5)
            break
        if (cnt % 2 == 0):
            list_board.append([copy.deepcopy(game1.table),-1])
            temp = game1.find_move(7)
            if (not isinstance(temp,move)):
                print("\n 2 thang")
                SGD(list_board, 1)
                break
            game2.process(temp)
        else:
            list_board.append([copy.deepcopy(game2.table),1])
            temp = game2.find_move(7)
            if (not isinstance(temp,move)):
                print("\n 1 thang")
                SGD(list_board, 0)
                break
            game1.process(temp)
        cnt += 1
def play_with_random():
    cnt = 0
    game1 = checker(base_table, -1)
    game2 = checker(base_table,  1)
    while (True):
        print(cnt, end=" ")
        if (cnt % 2 == 0):
            temp = game1.random_bot()
            if (not isinstance(temp, move)):
                print("\n 2 thang")
                break
            else:
                for i in range(8):
                    print(game1.table[i])
                for i in range(len(temp.move)):
                    print(temp.move[i].x, temp.move[i].y, sep=" ")
            game2.process(temp)
        else:
            temp = game2.find_move(4)
            if (not isinstance(temp, move)):
                print("\n 1 thang")
                break
            else:
                for i in range(8):
                    print(game2.table[i])
                for i in range(len(temp.move)):
                    print(temp.move[i].x, temp.move[i].y, sep=" ")
            game1.process(temp)
        cnt += 1
# play_with_random()