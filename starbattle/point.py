class point:
    def __init__(self,_x:int,_y: int):
        self.x = _x
        self.y = _y
    def __eq__(self, other):
        if(self.x == other.x and self.y == other.y):
            return True
        return False