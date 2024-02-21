# 3 state: STAND, LAY_Y, LAY_X

# Root_Coordinate: (x, y)
"""
STAND: |*|

LAY_X: |*|
       | |

LAY_Y: |*|| |
"""
# Movement: Direction -> (To_state, x, y)
'''
STAND Movement: (x, y)
Up    -> (LAY_X, x - 2, y)
Down  -> (LAY_X, x + 1, y)
Right -> (LAY_Y, x, y + 1)
Left  -> (LAY_Y, x, y - 2)
---------------------------------
LAY_Y Movement: (x, y)
Up    -> (LAY_Y, x + 1, y)
Down  -> (LAY_Y, x - 1, y)
Right -> (STAND, x, y + 2)
Left  -> (STAND, x, y - 1)
---------------------------------
LAY_X Movement: (x, y)
Up    -> (LAY_X, x, y - 1)
Down  -> (LAY_X, x, y + 1)
Right -> (STAND, x + 2, y)
Left  -> (STAND, x - 1, y)
'''
import copy


class Block:
    def __init__(self, x: int, y: int, state: str, x1=None, y1=None):
        self.x = x
        self.y = y
        self.state = state
        self.x1 = x1
        self.y1 = y1

    def move_up(self):
        if self.state == "STAND":
            self.x -= 2
            self.state = "LAY_X"
        elif self.state == "LAY_Y":
            self.x -= 1
        else:
            self.x -= 1
            self.state = "STAND"

    def move_down(self):
        if self.state == "STAND":
            self.x += 1
            self.state = "LAY_X"
        elif self.state == "LAY_Y":
            self.x += 1
        else:
            self.x += 2
            self.state = "STAND"

    def move_left(self):
        if self.state == "STAND":
            self.y -= 2
            self.state = "LAY_Y"
        elif self.state == "LAY_Y":
            self.y -= 1
            self.state = "STAND"
        else:
            self.y -= 1

    def move_right(self):
        if self.state == "STAND":
            self.y += 1
            self.state = "LAY_Y"
        elif self.state == "LAY_Y":
            self.y += 2
            self.state = "STAND"
        else:
            self.y += 1

    def change_split(self):
        t = self.x
        self.x = self.x1
        self.x1 = t
        t = self.y
        self.y = self.y1
        self.y1 = t

    def split_move_left(self):
        self.y -= 1

    def split_move_right(self):
        self.y += 1

    def split_move_up(self):
        self.x -= 1

    def split_move_down(self):
        self.x += 1

    def check_merge(self):
        if self.state == "SPLIT":
            if self.x == self.x1 and abs(self.y - self.y1) == 1:
                self.y = min(self.y, self.y1)
                self.x1 = None
                self.y1 = None
                self.state = "LAY_Y"
            elif self.y == self.y1 and abs(self.x - self.x1) == 1:
                self.x = min(self.x, self.x1)
                self.x1 = None
                self.y1 = None
                self.state = "LAY_X"
            else:
                return False
        else:
            return False
