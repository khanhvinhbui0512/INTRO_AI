import copy
import random
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
    def heuristic(self,node:state):
        eval = 0
        cntMin = 0
        cntMax = 0
        for i in range(self.size):
            for j in range(self.size):
                eval += node.table[i][j]
                if(node.table[i][j] < 0): cntMin+= 1
                if(node.table[i][j] > 0): cntMax+= 1
        if(cntMin == 0): return INFINITY
        if(cntMax == 0): return -INFINITY
        return eval
    def minimax(self,node:state,depth:int, alpha:float,beta:float, maximizingPlayer):
        if(depth == 0):
            return self.heuristic(node), move([])
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
def play():
    cnt = 0
    game1 = checker(base_table, -1)
    game2 = checker(base_table,  1)
    while (True):
        if (cnt % 2 == 0):
            temp = game1.find_move(7)
            if (not isinstance(temp,move)):
                print("2 thang")
                break
            else:
                for i in range(8):
                    print(game1.table[i])
                for i in range(len(temp.move)):
                    print(temp.move[i].x, temp.move[i].y, sep=" ")
            game2.process(temp)
        else:
            temp = game2.find_move(3)
            if (not isinstance(temp,move)):
                print("1 thang")
                break
            else:
                for i in range(8):
                    print(game2.table[i])
                for i in range(len(temp.move)):
                    print(temp.move[i].x, temp.move[i].y, sep=" ")
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