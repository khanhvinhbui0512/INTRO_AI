import pygame
import time
from bloxorz.Map import readfile
from bloxorz.Block import Block
from bloxorz.Map import Map
from bloxorz.BFS import BFS
from bloxorz.Genetic import genetic

print("Choose one level from 1 to 12")
level = int(input())
while level > 16 or level < 1:
    print("Level doesn't exit. Please choose agian one level from 1 to 16")
    level = int(input())
link = "map/map" + str(level) + ".txt"

pygame.init() # Khởi tạo py game

# Setup display view cho game
screen_width = 1000
screen_height = 750
display = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Bloxorz")

# Setup font
font = pygame.font.Font("freesansbold.ttf",64)

# Setup một số màu sắc được sử dụng trong game
TILE_COLOR = (199,208,207)
BLACK = (0,0,0)
BLOCK_COLOR = (165, 42, 42)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128,128,128)

# Gọi đối tượng block
block = Block(0,0,"STAND")

# Vẽ block lên màn hình game
def draw_block(state):
    if (state == "STAND"):
        pygame.draw.rect(display, BLOCK_COLOR, (50*block.y+5,50*block.x+5,39,39))
    elif (state == "LAY_X"):
        pygame.draw.rect(display, BLOCK_COLOR, (50*block.y+5,50*block.x+5,39,89))
    elif (state == "LAY_Y"):
        pygame.draw.rect(display, BLOCK_COLOR, (50*block.y+5,50*block.x+5,89,39))
    elif (state == "SPLIT"):
        pygame.draw.rect(display, BLOCK_COLOR, (50*block.y+5,50*block.x+5,39,39))
        pygame.draw.rect(display, BLOCK_COLOR, (50*block.y1+5,50*block.x1+5,39,39))
        pygame.draw.rect(display, YELLOW, (50*block.y-5,50*block.x-5,58,58), 4)

# Đọc các thông tin cần thiết từ 1 file map có sẵn
map, x_init, y_init, switches = readfile(link)
block.x, block.y = x_init, y_init

# Tạo các hình công tắc X,O
x_text = font.render("x", True, GRAY)
o_text = font.render("o", True, GRAY)

# Vẽ bản đồ trò chơi
def draw_map(startX = 0, startY = 0):
    x,y = startX,startY
    for row in map:
        for tile in row:
            if tile != 0:
                if tile == 1:
                    pygame.draw.rect(display, TILE_COLOR, (x,y,50,50))
                if tile == 2:
                    pygame.draw.rect(display, ORANGE, (x,y,50,50))
                if tile == 3 or tile == 4 or tile == 5:
                    pygame.draw.rect(display, TILE_COLOR, (x,y,50,50))
                    display.blit(o_text, (x+5,y-10))
                if tile == 6 or tile == 7:
                    pygame.draw.rect(display, TILE_COLOR, (x,y,50,50))
                    display.blit(x_text, (x+7,y-10))
                if tile == 8:
                    pygame.draw.rect(display, TILE_COLOR, (x,y,50,50))
                    pygame.draw.circle(display, GRAY, (x+22,y+24), 21, 8, False, True, True, False)
                    pygame.draw.circle(display, GRAY, (x+26,y+24), 21, 8, True, False, False, True)
                pygame.draw.line(display,BLACK, (x+50,y), (x+50,y+50), 5)
                pygame.draw.line(display,BLACK, (x,y+50), (x+50,y+50), 5)
            x += 50
        x = startX
        y += 50    

# Vẽ các cầu khi các công tắc được bật/tắt
def bridge(x_switch,y_switch,value):
    bridges = switches[(x_switch,y_switch)]
    for tile in bridges:
        x,y = tile[0],tile[1]
        if value == 3 or value == 6: # Có thể bật/tắt
            map[x][y] = 1 - map[x][y]
        elif value == 4 or value == 7: # Chỉ có thể bật
            map[x][y] = 1
        elif value == 5: # Chỉ có thể tắt
            map[x][y] = 0


# Tạo các text để render trong game
manual_text = font.render("Manual", True, YELLOW)
BFS_text = font.render("BFS", True, YELLOW)
Genetic_text = font.render("Genetic", True, YELLOW)
winning_text = font.render("You win!", True, YELLOW)
losing_text = font.render("You lose!", True, YELLOW)
back_text = font.render("Back", True, YELLOW)

# Vẽ menu
def draw_menu():
    pygame.draw.rect(display, BLACK, (360,130,280,90))
    display.blit(manual_text, (380,150))
    pygame.draw.rect(display, BLACK, (360,260,280,90))
    display.blit(BFS_text, (440,280))
    pygame.draw.rect(display, BLACK, (360,390,280,90))
    display.blit(Genetic_text, (380,405))

running = True # Biến chỉ ra chương trình có đang chạy không
reset_map = False
winning = False
playing = 0
Manual = 0
BFS_al = 1
Genetic_al = 2
mode = -1
algo_runned = False
# -1: Sau khi kết thúc ván chơi
# 0: Menu
# 1: Đang chơi game

# For BFS
def runBFS():
    game = Map(block, map, switches)
    ok, path = BFS(game)
    path.reverse()
    return ok, path

# For Genetic
def runGenetic():
    map_info = {
        "map_table": map,
        "start_x": x_init,
        "start_y": y_init,
        "switch_dict": switches
    }
    list_moves = ""
    if str(level) in ["8", "9", "10", "15", "16"]:
        list_moves = "null"
    else:
        list_moves = genetic(str(level), map_info)
    return list_moves

# Kiểm tra vị trí hiện tại của block sau khi di chuyển
# Từ đó update bản đồ dựa trên trạng thái mới nhất        
def check_move():
    x,y = block.x,block.y
    if map[x][y] == 9 and block.state == "STAND":
        global winning
        winning = True
        return -1
    elif map[x][y] == 8 and block.state == "STAND":
        block.state = "SPLIT"
        mini_blocks = switches[(x,y)]
        block.x, block.y, block.x1, block.y1 = mini_blocks[0][0], mini_blocks[0][1], mini_blocks[1][0], mini_blocks[1][1]
    elif block.state == "STAND":
        if map[x][y] == 0 or map[x][y] == 2: 
            return -1
        elif map[x][y] == 3 or map[x][y] == 4 or map[x][y] == 5 or map[x][y] == 6 or map[x][y] == 7:
            bridge(x,y,map[x][y])
    elif block.state == "LAY_X":
        if map[x][y] == 0 or map[x+1][y] == 0:
            return -1
        if map[x][y] == 3 or map[x][y] == 4 or map[x][y] == 5:
            bridge(x,y,map[x][y])
        elif map[x+1][y] == 3 or map[x+1][y] == 4 or map[x+1][y] == 5:
            bridge(x+1,y,map[x+1][y])              
    elif block.state == "LAY_Y":
        if map[x][y] == 0 or map[x][y+1] == 0:
            return -1
        if map[x][y] == 3 or map[x][y] == 4 or map[x][y] == 5:
            bridge(x,y,map[x][y])
        elif map[x][y+1] == 3 or map[x][y+1] == 4 or map[x][y+1] == 5:
            bridge(x,y+1,map[x][y+1])
    elif block.state == "SPLIT":
        if map[x][y] == 0:
            return -1
        if map[x][y] == 3 or map[x][y] == 4 or map[x][y] == 5:
            bridge(x,y,map[x][y])               
    return 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        display.fill((193,39,1)) # Fill screen
        if playing == 1:
            if winning:
                winning = False
            if mode == Manual:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_LEFT:
                        # print("LEFT")
                        if block.state == "SPLIT":
                            block.split_move_left()
                        else:
                            block.move_left()
                        playing = check_move()
                    if event.key == pygame.K_RIGHT:
                        # print("RIGHT")
                        if block.state == "SPLIT":
                            block.split_move_right()
                        else:
                            block.move_right()
                        playing = check_move()
                    if event.key == pygame.K_UP:
                        # print("UP")
                        if block.state == "SPLIT":
                            block.split_move_up()
                        else:
                            block.move_up()
                        playing = check_move()
                    if event.key == pygame.K_DOWN:
                        # print("DOWN")
                        if block.state == "SPLIT":
                            block.split_move_down()
                        else:
                            block.move_down()
                        playing = check_move()
                    if event.key == pygame.K_SPACE:
                        if block.state == "SPLIT":
                            # print("SWITCH MINI BLOCK")
                            block.change_split()
                    block.check_merge()

            elif mode == BFS_al:
                if algo_runned == False:
                    ok, path = runBFS()
                    algo_runned = True
                if ok == "YES":
                    draw_map()
                    draw_block(block.state)
                    pygame.display.update() # Update screen
                    for x in path:
                        for y in x:
                            time.sleep(1)
                            if y == "L":
                                if block.state == "SPLIT":
                                    block.split_move_left()
                                else:
                                    block.move_left()
                                playing = check_move()
                            if y == "R":
                                if block.state == "SPLIT":
                                    block.split_move_right()
                                else:
                                    block.move_right()
                                playing = check_move()
                            if y == "U":
                                if block.state == "SPLIT":
                                    block.split_move_up()
                                else:
                                    block.move_up()
                                playing = check_move()
                            if y == "D":
                                if block.state == "SPLIT":
                                    block.split_move_down()
                                else:
                                    block.move_down()
                                playing = check_move()
                            if y == "C":
                                if block.state == "SPLIT":
                                    block.change_split()
                            block.check_merge()
                            display.fill((193,39,1)) # Fill screen
                            draw_map()
                            draw_block(block.state)
                            pygame.display.update() # Update screen


                else:
                    pygame.display.quit()
                    pygame.quit()
                    exit()
            elif mode == Genetic_al:
                if algo_runned == False:
                    list_moves = runGenetic()
                    algo_runned = True
                if list_moves == "null":
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                else:
                    draw_map()
                    draw_block(block.state)
                    pygame.display.update() # Update screen
                    for move in list_moves:
                        time.sleep(1)
                        if move == "left":
                            if block.state == "SPLIT":
                                block.split_move_left()
                            else:
                                block.move_left()
                            playing = check_move()
                        if move == "right":
                            if block.state == "SPLIT":
                                block.split_move_right()
                            else:
                                block.move_right()
                            playing = check_move()
                        if move == "up":
                            if block.state == "SPLIT":
                                block.split_move_up()
                            else:
                                block.move_up()
                            playing = check_move()
                        if move == "down":
                            if block.state == "SPLIT":
                                block.split_move_down()
                            else:
                                block.move_down()
                            playing = check_move()
                        if move == "change":
                            if block.state == "SPLIT":
                                block.change_split()
                        block.check_merge()
                        display.fill((193,39,1)) # Fill screen
                        draw_map()
                        draw_block(block.state)
                        pygame.display.update() # Update screen


            display.fill((193,39,1)) # Fill screen        
            draw_map()
            draw_block(block.state)
            pygame.display.update() # Update screen
            reset_map = True
        elif playing == 0:
            if reset_map: # Cập nhật lại map, trạng thái ban đầu của block
                map, x_init, y_init, switches = readfile(link)
                block.x, block.y, block.state = x_init, y_init, "STAND"
                reset_map = False
            draw_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 360 <= mouse[0] <= 640 and 130 <= mouse[1] <= 220:
                    playing = 1
                    mode = Manual
                if 360 <= mouse[0] <= 640 and 260 <= mouse[1] <= 350:
                    playing = 1
                    mode = BFS_al
                if 360 <= mouse[0] <= 640 and 390 <= mouse[1] <= 480:
                    playing = 1
                    mode = Genetic_al

            pygame.display.update() # Update screen
        elif playing == -1:
            mode = -1
            algo_runned = False
            if winning:
                display.blit(winning_text, (380,200))
            else:
                display.blit(losing_text, (370,200))         
            pygame.draw.rect(display, BLACK, (410,480,195,100))
            display.blit(back_text, (430, 500))
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 410 <= mouse[0] <= 605 and 480 <= mouse[1] <= 580:
                    playing = 0

            pygame.display.update() # Update screen