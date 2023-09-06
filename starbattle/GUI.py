import pygame, sys
import numpy as np
from point import point
from main import starbattle
# pygame.init()

pygame.init()
RED = (255,0,0)
YELLOW = (255, 255, 0)
font = pygame.font.Font("freesansbold.ttf",40)
winning_text = font.render("You win!", True, RED)
reset_text = font.render("Reset", True, YELLOW)
solution_text = font.render("Solution", True, YELLOW)
class GUI:
    def __init__(self, _table: list[list[int]], _star: int):
        self.limit_dis = 1
        self.table = _table
        self.star = _star
        self.LINE_WIDTH = 1
        self.BIG_LINE_WIDTH = 5 * self.LINE_WIDTH
        self.WIN_LINE_WIDTH = 15
        self.SQUARE_SIZE = 60
        self.CIRCLE_RADIUS = 20
        self.CIRCLE_WIDTH = 10
        self.CROSS_WIDTH = 15
        self.SPACE = 25
        self.BOARD_ROWS = len(self.table)
        self.BOARD_COLS = len(self.table)
        self.WIDTH = self.BOARD_COLS * self.SQUARE_SIZE
        self.HEIGHT = self.BOARD_ROWS * self.SQUARE_SIZE
        self.RED = (255, 0, 0)
        self.BG_COLOR = (255, 255, 255)
        self.LINE_COLOR = (0, 0, 0)
        self.CIRCLE_COLOR = (239, 231, 200)
        self.CROSS_COLOR = (66, 66, 66)
        self.board = np.zeros((self.BOARD_ROWS, self.BOARD_COLS))
        pygame.init()
        pygame.display.set_caption('STAR BATTLE')
        screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT + 150))
        screen.fill(self.BG_COLOR)
        self.screen = screen
        self.solve = starbattle(len(self.table),self.star,self.table)
    def draw_lines(self):
        pygame.draw.line(self.screen, self.LINE_COLOR, (0 * self.SQUARE_SIZE, 0 * self.SQUARE_SIZE),
                         (self.BOARD_COLS * self.SQUARE_SIZE, 0 * self.SQUARE_SIZE), self.BIG_LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (0 * self.SQUARE_SIZE, 0 * self.SQUARE_SIZE),
                         (0 * self.SQUARE_SIZE, self.BOARD_ROWS * self.SQUARE_SIZE), self.BIG_LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (0 * self.SQUARE_SIZE, self.BOARD_ROWS * self.SQUARE_SIZE),
                         (self.BOARD_COLS * self.SQUARE_SIZE, len(self.table) * self.SQUARE_SIZE), self.BIG_LINE_WIDTH)
        pygame.draw.line(self.screen, self.LINE_COLOR, (self.BOARD_COLS * self.SQUARE_SIZE, 0 * self.SQUARE_SIZE),
                         (self.BOARD_ROWS * self.SQUARE_SIZE, self.BOARD_ROWS * self.SQUARE_SIZE), self.BIG_LINE_WIDTH)
        for i in range(len(self.table)):
            for j in range(len(self.table)):
                if (self.table[i][j] != self.table[i - 1][j]):
                    pygame.draw.line(self.screen, self.LINE_COLOR, (j * self.SQUARE_SIZE, i * self.SQUARE_SIZE),
                                     ((j + 1) * self.SQUARE_SIZE, i * self.SQUARE_SIZE), self.BIG_LINE_WIDTH)
                if (self.table[i][j] != self.table[i][j - 1]):
                    pygame.draw.line(self.screen, self.LINE_COLOR, (j * self.SQUARE_SIZE, i * self.SQUARE_SIZE),
                                     (j * self.SQUARE_SIZE, (i + 1) * self.SQUARE_SIZE), self.BIG_LINE_WIDTH)
        for i in range(1, self.BOARD_COLS):
            pygame.draw.line(self.screen, self.LINE_COLOR, (0 * self.SQUARE_SIZE, i * self.SQUARE_SIZE),
                             (self.BOARD_COLS * self.SQUARE_SIZE, i * self.SQUARE_SIZE), self.LINE_WIDTH)
            # vertical line
        for i in range(1, self.BOARD_ROWS):
            pygame.draw.line(self.screen, self.LINE_COLOR, (i * self.SQUARE_SIZE, 0 * self.SQUARE_SIZE),
                             (i * self.SQUARE_SIZE, self.BOARD_ROWS * self.SQUARE_SIZE), self.LINE_WIDTH)

    def mark_square(self, row, col):
        self.board[row][col] = 1 - self.board[row][col]

    def restart(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_lines()
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                self.board[row][col] = 0
        self.draw_button()

    def get_list_star(self):
        list_star = []
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if (self.board[row][col] == 1):
                    list_star.append(point(row, col))
        return list_star

    def distance(self, p1: point, p2: point):
        return max(abs(p1.x - p2.x), abs(p1.y - p2.y))

    def check_legal(self):
        list_star = self.get_list_star()
        cnt_row = np.zeros(len(self.table), dtype=int)
        cnt_col = np.zeros(len(self.table), dtype=int)
        check = True
        for i in range(len(list_star)):
            cnt_row[list_star[i].x] += 1
            cnt_col[list_star[i].y] += 1
        for i in range(len(self.table)):
            if (cnt_row[i] > self.star or cnt_col[i] > self.star):
                check = False
        for i in range(len(list_star)):
            for j in range(i + 1, len(list_star)):
                if (self.distance(list_star[i], list_star[j]) <= self.limit_dis):
                    check = False
        return check

    def check_win(self):
        list_star = self.get_list_star()
        if (self.check_legal() == True and len(list_star) == self.star * len(self.table)):
            return True
        return False

    def draw_figures(self):
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if (self.board[row][col] != 0):
                    pygame.draw.line(self.screen, self.CROSS_COLOR,
                                     (col * self.SQUARE_SIZE + self.SPACE,
                                      row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE),
                                     (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE,
                                      row * self.SQUARE_SIZE + self.SPACE), self.CROSS_WIDTH)
                    pygame.draw.line(self.screen, self.CROSS_COLOR,
                                     (col * self.SQUARE_SIZE + self.SPACE, row * self.SQUARE_SIZE + self.SPACE),
                                     (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE,
                                      row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE), self.CROSS_WIDTH)
                else:
                    pygame.draw.line(self.screen, self.BG_COLOR,
                                     (col * self.SQUARE_SIZE + self.SPACE,
                                      row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE),
                                     (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE,
                                      row * self.SQUARE_SIZE + self.SPACE), self.CROSS_WIDTH)
                    pygame.draw.line(self.screen, self.BG_COLOR,
                                     (col * self.SQUARE_SIZE + self.SPACE, row * self.SQUARE_SIZE + self.SPACE),
                                     (col * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE,
                                      row * self.SQUARE_SIZE + self.SQUARE_SIZE - self.SPACE),
                                     self.CROSS_WIDTH)

    def draw_win(self):
        self.screen.blit(winning_text, (self.WIDTH / 2 - 1*self.SQUARE_SIZE,self.HEIGHT+30))
    def draw_button(self):
        pygame.draw.rect(self.screen, (0,0,0), (0, self.HEIGHT+80, 130, 60))
        self.screen.blit(reset_text, (10, self.HEIGHT+90))
        pygame.draw.rect(self.screen, (0,0,0), (self.WIDTH-80*2.2, self.HEIGHT+80, 180, 60))
        self.screen.blit(solution_text, (self.WIDTH-80*2.2+10, self.HEIGHT+90))
    def play(self):
        self.draw_lines()
        self.draw_button()
        game_over = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                        mouseX = event.pos[0]
                        mouseY = event.pos[1]
                        clicked_row = int(mouseY // self.SQUARE_SIZE)
                        clicked_col = int(mouseX // self.SQUARE_SIZE)
                        if(clicked_col < self.BOARD_COLS and clicked_row < self.BOARD_ROWS and not game_over):
                            self.mark_square(clicked_row, clicked_col)
                        if(0 < mouseX < 130 and self.WIDTH-self.SQUARE_SIZE*2.2 < mouseY <self.HEIGHT+140):
                            self.restart()
                            game_over = False
                        if(self.WIDTH-self.SQUARE_SIZE*2.2 < mouseX < self.WIDTH-self.SQUARE_SIZE*2.2
                                + 180 and self.HEIGHT+80< mouseY < self.HEIGHT + 140 and not game_over):
                            game_over = True
                            self.restart()
                            
                            solution,cnt = self.solve.DFS()
                            print(solution)
                            for i in range(len(solution)):
                                self.mark_square(solution[i].x, solution[i].y)
                        if self.check_win() == True and not game_over:
                            game_over = True
                            self.draw_win()
                        self.draw_figures()
                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_r:
                    #         self.restart()
                    #         game_over = False
                pygame.display.update()


# temp = GUI(table, 1)
# temp.play()