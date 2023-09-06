from copy import deepcopy
from random import random, choice, choices, randint, randrange
from bloxorz import Block
from bloxorz import Map


# Relevant population_configuration for each map
class Population_Configuration:
    def __init__(self, num_moves: int, size: int, mutation_rate: float, best_rate: float, evaluation: list):
        self.num_moves = deepcopy(num_moves)
        self.size = deepcopy(size)
        self.mutation_rate = deepcopy(mutation_rate)
        self.best_rate = best_rate
        self.evaluation = deepcopy(evaluation)
        self.evaluation.append(num_moves)


POPULATION_CONFIGURATIONS = {
    "1": Population_Configuration(7, 1000, 0.1, 0.1, [0, -1]),
    "2": Population_Configuration(25, 5000, 0.5, 0.3, [0, -1]),
    "3": Population_Configuration(30, 10000, 0.5, 0.3, [0, 0]),
    "4": Population_Configuration(35, 50000, 0.5, 0.5, [0, 0]),
    "5": Population_Configuration(55, 100000, 0.01, 0.1, [0, -1]),
}


# ================================================================
# CONSTANTS
MOVE = ["up", "down", "left", "right"]
MAP_NO = ""
MAP_INFO = {}  # with the following keys: map_table, start_x, start_y, switch_dict
CONFIG = Population_Configuration(0, 0, 0, 0, [0, 0])
# ================================================================


def create_single_solution():
    return choices(MOVE, k=CONFIG.num_moves)


def calc_fitness(list_moves: []) -> list[int, int, int]:
    target = tuple
    penalty = 0
    bad_moves = 0
    for i, x in enumerate(MAP_INFO["map_table"]):
        if 9 in x:
            target = (i, x.index(9))
    block = Block.Block(MAP_INFO["start_x"], MAP_INFO["start_y"], "STAND")
    map_object = Map.Map(block, MAP_INFO["map_table"], MAP_INFO["switch_dict"])
    for i, move in enumerate(list_moves):
        current_distance = abs(target[0] - block.x) + abs(target[1] - block.y)
        # Basic movement
        if move == "up":
            block.move_up()
        elif move == "down":
            block.move_down()
        elif move == "left":
            block.move_left()
        elif move == "right":
            block.move_right()
        after_distance = abs(target[0] - block.x) + abs(target[1] - block.y)
        if after_distance < current_distance:
            bad_moves += 1
        # ------------------------
        # Check for penalty move
        if block.x < 0 or block.y < 0:
            penalty += 1
        elif block.x >= len(MAP_INFO["map_table"]) or block.y >= len(MAP_INFO["map_table"][0]):
            penalty += 1
        elif map_object.is_0(block) or map_object.is_2(block):
            penalty += 1
        # ------------------------
        # Check for switches
        elif map_object.is_3(block):
            pass
        elif map_object.is_4(block):
            pass
        elif map_object.is_5(block):
            pass
        elif map_object.is_6(block):
            pass
        elif map_object.is_7(block):
            pass
        # ------------------------
        # Check if reach target
        elif map_object.is_9(block) and penalty == 0:
            del list_moves[i + 1:]
            return [0, -1, bad_moves]
        # ------------------------
    return [penalty, abs(target[0] - block.x) + abs(target[1] - block.y), bad_moves]


def mutate(list_moves):
    if random() < CONFIG.mutation_rate:
        place = randint(0, CONFIG.num_moves - 1)
        new_moves = [x for x in MOVE if x != list_moves[place]]
        list_moves[place] = choice(new_moves)
    return list_moves


def crossover(parent1: [], parent2: []):
    cut_point = randrange(0, CONFIG.num_moves - 2)
    if random() >= 0.5:
        off_spring = parent1[:cut_point] + parent2[cut_point:]
    else:
        off_spring = parent2[:cut_point] + parent1[cut_point:]
    return off_spring


# An individual will contain a solution and the fitness score for that solution
class Individual:
    def __init__(self, list_moves):
        self.list_moves = list_moves
        self.fitness = calc_fitness(self.list_moves)


# Create a population
def create_population():
    population = []
    while len(population) < CONFIG.size:
        list_moves = create_single_solution()
        if list_moves not in population:
            population.append(Individual(list_moves))
    return population


def genetic(map_no, map_info):
    global MAP_NO, MAP_INFO, CONFIG
    MAP_NO = map_no
    MAP_INFO = map_info
    CONFIG = POPULATION_CONFIGURATIONS[MAP_NO]
    population = create_population()
    index = 0
    while 1:
        population.sort(key=lambda x: (x.fitness, len(x.list_moves)))
        print("Generation: " + str(index) + " - " + "Best fitness: " + str(population[0].fitness))
        if population[0].fitness <= CONFIG.evaluation:
            solution = population[0].list_moves
            break
        else:
            best_individuals = int(CONFIG.best_rate * CONFIG.size)
            new_generation = population[:best_individuals]
            new_rest_population = CONFIG.size - best_individuals
            for i in range(new_rest_population):
                parent1_list_moves = new_generation[randint(0, best_individuals - 1)].list_moves
                parent2_list_moves = new_generation[randint(0, best_individuals - 1)].list_moves
                off_spring_list_moves = crossover(parent1_list_moves, parent2_list_moves)
                mutate(off_spring_list_moves)
                off_spring = Individual(off_spring_list_moves)
                new_generation.append(off_spring)
            population = new_generation
        index += 1
    for index, move in enumerate(solution, start=1):
        print(index, move)
    return solution
