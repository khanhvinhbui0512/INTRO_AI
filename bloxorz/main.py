from bloxorz.Map import readfile, Map
from bloxorz.Block import Block
from bloxorz.BFS import BFS
from bloxorz.Genetic import genetic
from time import time
import os, psutil
from bloxorz.Map import readfile
from bloxorz.BFS import BFS
from bloxorz.Map import Map
from bloxorz.Block import Block


def execute():
    process = psutil.Process(os.getpid())
    map_no = input("Select map to play: ")
    algorithm_no = int(input("Choose algorithm:\n"
                             "* 1 is Breadth First Search\n"
                             "* 2 is Genetic Search\n"
                             "Type your selection: "))
    map_table, start_x, start_y, switch_dict = readfile("map/map%d.txt" % int(map_no))
    time_start = time()
    if algorithm_no == 1:
        block = Block(start_x, start_y, "STAND")
        game = Map(block, map_table, switch_dict)
        ok, path = BFS(game)
        path.reverse()
        if ok == "YES":
            for x in path:
                for y in x:
                    print(y)
        else:
            print("THERE IS NO SUCCESS ROAD\n")
    elif algorithm_no == 2:
        map_info = {
            "map_table": map_table,
            "start_x": start_x,
            "start_y": start_y,
            "switch_dict": switch_dict
        }
        if map_no in ["8", "9", "10", "15", "16"]:
            print("Not available!")
        else:
            genetic(map_no, map_info)
    elapsed_time = time() - time_start
    print("Elapsed time:", end=" ")
    print(round(elapsed_time, 4))
    print("Memory:", end=" ")
    print(round(process.memory_info().rss / (1024 * 1024), 2))  


execute()
