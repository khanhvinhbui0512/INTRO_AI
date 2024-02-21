'''
Quy định màu trong input:
Rỗng            = 0
Đỏ              = 1
Vàng            = 2
Xanh dương đậm  = 3
Xanh lá nhạt    = 4
Cam             = 5
Hồng            = 6
Xám             = 7
'''

import numpy as np
import pygame
import sys
from solver import WaterSort


def encode_number_to_color(x):
    switcher = {
        0: (255, 255, 255),
        1: (255, 0, 0),
        2: (255, 255, 0),
        3: (0, 0, 255),
        4: (0, 255, 0),
        5: (255, 165, 0),
        6: (255, 192, 203),
        7: (169, 169, 169)
    }
    return switcher.get(x)


def create_color_in_pipe(arr, pipe_surface, idx_pipe_1, idx_pipe_2):
    # pipes = [[]]
    for i in range(arr.shape[1]):
        pipe_surface.append(pygame.Surface((70, 60 * arr_row + 10)))
        pipe_surface[i].fill((255, 255, 255))
        for j in range(arr.shape[0]):
            # pipes[j][i] = (5 , 5 + 50*j, 50, 50)
            pipe_surface[i].get_rect(center=(50, 50))
            pygame.draw.rect(pipe_surface[i], encode_number_to_color(arr[j][i]), (10, 10 + 60 * j, 50, 50))
        if i == idx_pipe_1 or i == idx_pipe_2:  # Cho bình được chọn cao hơn
            if arr.shape[1] <= 4:
                screen.blit(pipe_surface[i], (45 * (4 - arr.shape[1] + 1) + 90 * i, 90 - 30))
            elif i < 4:
                screen.blit(pipe_surface[i], (45 + 90 * i, 90 - 30))
            elif i >= 4:
                screen.blit(pipe_surface[i], (45 * (8 - arr.shape[1] + 1) + 90 * (i - 4), 90 + 60 * arr_row + 60 - 30))
        else:  # Những bình không được chọn thì không cao lên
            if arr.shape[1] <= 4:
                screen.blit(pipe_surface[i], (45 * (4 - arr.shape[1] + 1) + 90 * i, 90))
            elif i < 4:
                screen.blit(pipe_surface[i], (45 + 90 * i, 90))
            elif i >= 4:
                screen.blit(pipe_surface[i], (45 * (8 - arr.shape[1] + 1) + 90 * (i - 4), 90 + 60 * arr_row + 60))
    # return pipes


def change_color(arr, idx1, idx2):
    # idx lớn hơn index trong arr 1 đơn vị
    t = -1
    z = -1
    for i in range(arr.shape[0]):
        if arr[i][idx1] == 0:
            continue
        else:
            t = i
            break
    for i in range(arr.shape[0]):
        if i == arr.shape[0] - 1: z = i
        if arr[i][idx2] == 0:
            continue
        else:
            z = i - 1
            break
    while True:
        if t == arr.shape[0] or z == -1:
            break
        elif z == arr.shape[0] - 1 and arr[z][idx2] == 0:
            arr[t][idx1], arr[z][idx2] = arr[z][idx2], arr[t][idx1]
        elif arr[t][idx1] == arr[z + 1][idx2]:
            arr[t][idx1], arr[z][idx2] = arr[z][idx2], arr[t][idx1]
        else:
            break
        t += 1
        z -= 1


# Check xem đã thắng hay chưa
def check_win(arr):
    for j in range(arr.shape[1]):
        for i in range(arr.shape[0] - 1):
            if arr[i][j] != arr[i + 1][j]: return False
    return True


pygame.init()
TILE_COLOR = (199, 208, 207)
# 0 màu trắng
WHITE = (255, 255, 255)
# 1 màu đỏ
RED = (255, 0, 0)
# 2 màu vàng
YELLOW = (255, 255, 0)
# 3 màu xanh dương
BLUE = (0, 0, 255)
# 4 màu xanh lá
GREEN = (0, 255, 0)
# 5 màu cam
ORANGE = (255, 165, 0)
# 6 màu hồng
PINK = (255, 192, 203)
# 7 màu xám
GREY = (169, 169, 169)

# Setup font
font = pygame.font.Font("freesansbold.ttf", 64)

# Tạo các text để render trong game
manual_text = font.render("Manual", True, YELLOW)
DFS_text = font.render("DFS", True, YELLOW)
A_STAR_text = font.render("A *", True, YELLOW)
winning_text = font.render("You win!", True, YELLOW)
back_text = font.render("Back", True, YELLOW)


# Vẽ menu
def draw_menu():
    screen = pygame.display.set_mode((432, 768))
    pygame.draw.rect(screen, WHITE, (80, 130, 280, 90))
    screen.blit(manual_text, (100, 150))
    pygame.draw.rect(screen, WHITE, (80, 260, 280, 90))
    screen.blit(DFS_text, (150, 280))
    pygame.draw.rect(screen, WHITE, (80, 390, 280, 90))
    screen.blit(A_STAR_text, (180, 410))


running = True  # Biến chỉ ra chương trình có đang chạy không
reset_map = False
winning = False
playing = 0
# -1: Sau khi kết thúc ván chơi
# 0: Menu
# 1: Đang chơi game Manual
# 2: DFS
# 3: A*

# Tạo các biến cần có cho game
screen = pygame.display.set_mode((432, 768))
pygame.display.set_caption("Watersort")
clock = pygame.time.Clock()

# Read file input testcase
arr = []
level_no = int(input("Choose a level from 1 to 10: "))
# Choose from 1 to 10
with open("testcase/testcase" + str(level_no) + ".txt") as file:
    while line := file.readline().rstrip():
        li = list(map(int, line.split(' ')))
        arr.append(li)

# Solve the testcase with DFS here (playing == 2)
np_arr = np.copy(arr)
resultAStar = WaterSort(np_arr).solveAStar()
resultDFS = WaterSort(np_arr).solveDFS()

list_step = []
for steps in resultDFS:
    curr_step = np.array(list(steps))
    list_step.append(curr_step)

arr = np_arr  # Input
arr_3 = np.array(list_step)  # Solution DFS

# Mỗi ô màu có kích thước 60*60 => Pipe sẽ có kích thước 62*(62*arr_row)
arr_row = arr.shape[0]
arr_col = arr.shape[1]
# Tạo ra một mảng 2 chiều là surface của các bình
pipe_surface = []
pipe_list = [[]]
# Tạo ra biến dành để chơi Manual
int_times = 0
idx_1 = 9
idx_2 = 9
i = 0  # biến index đầu tiên của mảng 3 chiều
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if playing == 1:
            screen = pygame.display.set_mode((432, 768))
            create_color_in_pipe(np_arr, pipe_surface, idx_1, idx_2)
            if winning: winning = False
            if event.type == pygame.KEYDOWN:
                int_times += 1
                if event.key == pygame.K_BACKSPACE:
                    playing = 0
                if event.key == pygame.K_1:
                    if int_times == 1:
                        idx_1 = 0
                    elif int_times == 2:
                        idx_2 = 0
                        change_color(np_arr, idx_1, idx_2)
                elif event.key == pygame.K_2:
                    if int_times == 1:
                        idx_1 = 1
                    elif int_times == 2:
                        idx_2 = 1
                        change_color(np_arr, idx_1, idx_2)
                elif event.key == pygame.K_3:
                    if int_times == 1:
                        idx_1 = 2
                    elif int_times == 2:
                        idx_2 = 2
                        change_color(np_arr, idx_1, idx_2)
                elif event.key == pygame.K_4:
                    if int_times == 1:
                        idx_1 = 3
                    elif int_times == 2:
                        idx_2 = 3
                        change_color(np_arr, idx_1, idx_2)
                elif event.key == pygame.K_5:
                    if int_times == 1:
                        idx_1 = 4
                    elif int_times == 2:
                        idx_2 = 4
                        change_color(np_arr, idx_1, idx_2)
                elif event.key == pygame.K_6:
                    if int_times == 1:
                        idx_1 = 5
                    elif int_times == 2:
                        idx_2 = 5
                        change_color(np_arr, idx_1, idx_2)
                elif event.key == pygame.K_7:
                    if int_times == 1:
                        idx_1 = 6
                    elif int_times == 2:
                        idx_2 = 6
                        change_color(np_arr, idx_1, idx_2)
                elif event.key == pygame.K_8:
                    if int_times == 1:
                        idx_1 = 7
                    elif int_times == 2:
                        idx_2 = 7
                        change_color(np_arr, idx_1, idx_2)
                elif event.key == pygame.K_ESCAPE:
                    idx_1 = 9
                    idx_2 = 9
                    int_times = 0

                if check_win(np_arr):
                    winning = True
                    playing = -1
            pygame.display.update()
        elif playing == 0:
            draw_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                winning = False
                mouse = pygame.mouse.get_pos()
                if 80 <= mouse[0] <= 360 and 130 <= mouse[1] <= 220:
                    playing = 1
                elif 80 <= mouse[0] <= 360 and 260 <= mouse[1] <= 350:  # BFS
                    playing = 2
                elif 80 <= mouse[0] <= 360 and 390 <= mouse[1] <= 480:  # A*
                    playing = 3
            pygame.display.update()  # Update screen
        elif playing == -1:
            if winning:
                screen = pygame.display.set_mode((432, 768))
                pygame.draw.rect(screen, WHITE, (80, 260, 280, 90))
                screen.blit(winning_text, (85, 280))
                pygame.display.update()  # Update screen
        elif playing == 2:
            if i < arr_3.shape[0]:
                screen = pygame.display.set_mode((432, 768))
                create_color_in_pipe(arr_3[i], pipe_surface, 9, 9)
            if i >= arr_3.shape[0]:
                playing = -1
                winning = True
                pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    playing = 0
                if event.key == pygame.K_SPACE:
                    if i < (arr_3.shape[0]):
                        screen = pygame.display.set_mode((432, 768))
                        create_color_in_pipe(arr_3[i], pipe_surface, 9, 9)
                        i += 1
            pygame.display.update()

        elif playing == 3:
            list_step_A = []
            for steps in resultAStar:
                curr_step = np.array(list(steps))
                list_step_A.append(curr_step)

            arr_3 = np.array(list_step_A)

            if i < arr_3.shape[0]:
                screen = pygame.display.set_mode((432, 768))
                create_color_in_pipe(arr_3[i], pipe_surface, 9, 9)
            if i >= arr_3.shape[0]:
                playing = -1
                winning = True
                pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    playing = 0
                if event.key == pygame.K_SPACE:
                    if i < (arr_3.shape[0]):
                        screen = pygame.display.set_mode((432, 768))
                        create_color_in_pipe(arr_3[i], pipe_surface, 9, 9)
                        i += 1
            pygame.display.update()
