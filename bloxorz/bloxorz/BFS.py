import copy
def IS_VISITED(curr, Visited):
    if (curr.block.state == "SPLIT"):
        for item in Visited:
            if item.block.x == curr.block.x and item.block.y == curr.block.y and \
                    item.block.x1 == curr.block.x1 and item.block.y1 == curr.block.y1 and \
                    curr.map == item.map:
                return True
    else:
        for item in Visited:
            if item.block.x == curr.block.x and item.block.y == curr.block.y and \
                    item.block.state == curr.block.state and curr.map == item.map:
                return True
    return False


def BFS(game: map):
    queue = []
    queue.append([game, None])
    Count = 0
    Visited = []
    PARENT = {game: None}
    ans = game
    while len(queue) > 0:
        temp = queue[0]
        queue.pop(0)
        curr = temp[0]
        curr.block.check_merge()
        if (curr.block.state == "SPLIT"):
            if (curr.check_all_split() == True):
                continue
        else:
            if (curr.check_all() == True):
                continue
        if (IS_VISITED(curr, Visited) == False):
            Visited.append(curr)
        else:
            continue
        PARENT[curr] = temp[1]
        if (curr.is_9(curr.block)):
            ans = curr
            break
        if(curr.block.state != "SPLIT"):
            Count += 4
            t1 = copy.deepcopy(curr)
            t1.block.move_up()
            queue.append([t1, [curr, "U"]])
            t2 = copy.deepcopy(curr)
            t2.block.move_down()
            queue.append([t2, [curr, "D"]])
            t3 = copy.deepcopy(curr)
            t3.block.move_left()
            queue.append([t3, [curr, "L"]])
            t4 = copy.deepcopy(curr)
            t4.block.move_right()
            queue.append([t4, [curr, "R"]])
        else:
            Count += 8
            t1 = copy.deepcopy(curr)
            t1.block.split_move_up()
            queue.append([t1, [curr, "U"]])
            t2 = copy.deepcopy(curr)
            t2.block.split_move_down()
            queue.append([t2, [curr, "D"]])
            t3 = copy.deepcopy(curr)
            t3.block.split_move_left()
            queue.append([t3, [curr, "L"]])
            t4 = copy.deepcopy(curr)
            t4.block.split_move_right()
            queue.append([t4, [curr, "R"]])
            t=copy.deepcopy(curr)
            t.block.change_split()
            queue.append([t, [curr, "C"]])
    SUCCESS_PATH = []
    if (ans == game):
        return "NO", []
    while PARENT[ans] != None:
        SUCCESS_PATH.append(PARENT[ans][1])
        ans = PARENT[ans][0]
    return "YES",SUCCESS_PATH
