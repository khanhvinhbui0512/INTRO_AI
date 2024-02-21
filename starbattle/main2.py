import time
import itertools
import copy
import psutil
import os
import numpy as np
from queue import PriorityQueue
from point import point
a = 1
b = 7.75
class state:
    def __init__(self,_curr:int,_list_star:list[point] or list[None],_cost):
        self.curr = _curr
        self.list_star = _list_star
        self.cost = _cost
    def __gt__(self,other):
        if(self.cost > other.cost):
            return True
        return False
    def __lt__(self,other):
        if(self.cost < other.cost):
            return True
        return False
class starbattle:
    def __init__(self,size_board:int,star:int,table:list[list[int]]):
        self.size_board = size_board
        self.star= star
        self.table = table
        self.list_shape = self.get_shape()
        self.limit_dis = 1
    def get_shape(self):
        list_shape = []
        for i in range(self.size_board): list_shape.append([])
        for i in range(self.size_board):
            for j in range(self.size_board):
                list_shape[self.table[i][j]].append(point(i, j))
        return list_shape
    def g(self,curr:state):
        ans = 0
        temp = []
        check_row = np.zeros(self.size_board,dtype = int)
        check_col = np.zeros(self.size_board,dtype = int)
        for i in range(curr.curr):
            temp = temp + self.list_shape[i]
        for i in range(len(curr.list_star)):
            check_row[curr.list_star[i].x] = 1
            check_col[curr.list_star[i].y] = 1
        for i in range(self.size_board):
            for j in range(self.size_board):
                if(point(i,j) in temp or check_col[j] == 1 or check_row[i] == 1):
                    ans += 1
        return ans
    def h(self,curr:state):
        return self.size_board*self.star - len(curr.list_star)
    def distance(self,p1:point,p2:point):
        return max(abs(p1.x -p2.x),abs(p1.y-p2.y))
    #KIỂM TRA SỰ HỢP LỆ CỦA TRẠNG THÁI HIỆN TẠI
    def is_legal(self,curr: state):
        cnt_row = np.zeros(self.size_board,dtype = int)
        cnt_col = np.zeros(self.size_board,dtype = int)
        check = True
        for i in range(len(curr.list_star)):
            cnt_row[curr.list_star[i].x] += 1
            cnt_col[curr.list_star[i].y] += 1
        for i in range(self.size_board):
            if(cnt_row[i] > self.star or cnt_col[i] > self.star):
                check = False
        for i in range(len(curr.list_star)):
            for j in range(i+1,len(curr.list_star)):
                if(self.distance(curr.list_star[i],curr.list_star[j]) <= self.limit_dis):
                    check = False
        return check
    def DFS(self):
        stack = []
        stack.append(state(0,[],0))
        cnt = 0
        while(len(stack) != 0):
            top = stack.pop()
            if(self.is_legal(top) == True):
                cnt += 1
                print(top.curr)
                if (top.curr == self.size_board):
                    return top.list_star,cnt
                else:
                    list_op = list(itertools.combinations(range(len(self.list_shape[top.curr])), self.star))
                    for i in range(len(list_op)):
                        list_star = copy.deepcopy(top.list_star)
                        for j in range(len(list_op[i])):
                            list_star = list_star + [self.list_shape[top.curr][list_op[i][j]]]
                        stack.append(state(top.curr+1,list_star,0))
        return stack
    def A_star(self):
        cnt = 0
        tree_state = PriorityQueue()
        tree_state.put(state(0, [], size_board*b))
        while (not tree_state.empty()):
            cnt += 1
            top = tree_state.get()
            print(top.curr)
            if (top.curr == self.size_board):
                return top.list_star,cnt
            else:
                list_op = list(itertools.combinations(range(len(self.list_shape[top.curr])), self.star))
                for i in range(len(list_op)):
                    list_star = copy.deepcopy(top.list_star)
                    for j in range(len(list_op[i])):
                        list_star = list_star + [self.list_shape[top.curr][list_op[i][j]]]
                    temp = state(top.curr + 1, list_star, 0)
                    if (self.is_legal(temp) == True):
                        temp.cost = a*self.g(temp) + b* self.h(temp)
                        tree_state.put(temp)
        return []
    def solve(self):
        # print("Nhập 1 nếu giải bằng DFS và 2 nếu giải bằng A start:")
        # option = int(input())
        # if(option == 1):
        #     solution,cnt = self.DFS()
        # else:
        #     solution,cnt = self.A_star()
        solution, cnt = self.A_star()
        # if(len(solution) == 0):
        #     print("NO SOLUTION")
        # else:
        #     for i in range(len(solution)):
        #         print(solution[i].x + 1, solution[i].y + 1)
        return solution,cnt
# while(b <= 12):
#     total_cnt = 0
#     total_time = 0
#     for k in range(1,13):
#         with open("testcase/text"+str(k)+".txt") as test_file:
#             line = next(test_file)
#             n, m = list(map(int, line.split()))
#             table = []
#             for i in range(n):
#                 line = next(test_file)
#                 row = line.split(' ')
#                 temp = []
#                 for j in range(len(row)): temp.append(int(row[j]))
#                 table.append(temp)
#             size_board = n
#             star = m
#             start = time.time()
#             game = starbattle(size_board,star,table)
#             solution,cnt = game.solve()
#             end = time.time()
#             total_cnt += cnt
#             total_time += end - start
#     print(a,b, total_cnt,total_time)
#     b+=0.125

with open("testcase/text1.txt") as test_file:
    process = psutil.Process(os.getpid())
    line = next(test_file)
    n, m = list(map(int, line.split()))
    table = []
    for i in range(n):
        line = next(test_file)
        row = line.split(' ')
        temp = []
        for j in range(len(row)): temp.append(int(row[j]))
        table.append(temp)
    size_board = n
    star = m
    start = time.time()
    game = starbattle(size_board,star,table)
    solution,cnt = game.solve()
    end = time.time()
    for i in range(len(solution)):
        print(solution[i].x + 1, solution[i].y + 1)
    print(round(end -start,5),cnt,round(process.memory_info().rss / (1024 * 1024), 2))