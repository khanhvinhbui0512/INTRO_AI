# INTRO AI ASS 1 - GAME Bloxorz
# Các trường hợp 
# 0: Ô không có nền: 0
# 1: Ô có thể đi lại bình thường: 1
# 2: Ô chỉ có thể xoay ngang: 2
# 3: Công tắc tròn có thể bật tắt: 3
# 4: Công tắc tròn chỉ có thể bật: 4
# 5: Công tắc tròn chỉ có thể tắt: 5
# 6: Công tắc X có thể bật tắt: 6
# 7: Công tắc X chỉ có thể bật: 7
# 8: Công tác để cục phân thân: 8
# 9: Ô đích đến: 9+`    `
import copy

def readfile(file):
    with open(file) as f:
        # Nhận dữ liệu cột, hàng và điểm bắt đầu
        row, col, start_x, start_y, switch = [int(x) for x in next(f).split()]
        map_table = []  # khởi tạo map
        keys = []
        values = []
        # Đọc dữ liệu của map ban đầu
        for i in range(row):
            map_table.append([int(x) for x in next(f).split()])
        for i in range(switch):
            line = [int(x) for x in next(f).split()]
            keys.append((line[0], line[1]))
            value = []
            idx = 2
            while idx < len(line):
                value.append((line[idx], line[idx + 1]))
                idx += 2
            values.append(value)
        switch_dict = dict(zip(keys, values))
        return map_table, start_x, start_y, switch_dict


class Map:

    def __init__(self, _block, _map, _hash=None):
        self.block = _block
        self.map = copy.deepcopy(_map)
        self.hash = _hash
    def is_0(self, block):
        if self.map[block.x][block.y] == 0:
            return True
        elif self.map[block.x + 1][block.y] == 0 and block.state == "LAY_X":
            return True
        elif self.map[block.x][block.y + 1] == 0 and block.state == "LAY_Y":
            return True
        return False

    def is_1(self, block):
        pass

    def is_2(self, block):
        if self.map[block.x][block.y] == 2 and block.state == "STAND":
            return True
        return False

    def is_3(self, block):
        if self.map[block.x][block.y] == 3:
            for point in self.hash[(block.x, block.y)]:
                self.map[point[0]][point[1]] ^= 1
            return True
        elif self.map[block.x + 1][block.y] == 3 and block.state == "LAY_X":
            for point in self.hash[(block.x + 1, block.y)]:
                self.map[point[0]][point[1]] ^= 1
            return True
        elif self.map[block.x][block.y + 1] == 3 and block.state == "LAY_Y":
            for point in self.hash[(block.x, block.y+1)]:
                self.map[point[0]][point[1]] ^= 1
            return True
        return False
    def is_4(self, block):
        if self.map[block.x][block.y] == 4:
            for point in self.hash[(block.x,block.y)]:
                self.map[point[0]][point[1]] = 1
            return True
        elif self.map[block.x + 1][block.y] == 4 and block.state == "LAY_X":
            for point in self.hash[(block.x+1, block.y)]:
                self.map[point[0]][point[1]] = 1
            return True
        elif self.map[block.x][block.y + 1] == 4 and block.state == "LAY_Y":
            for point in self.hash[(block.x, block.y+1)]:
                self.map[point[0]][point[1]] = 1
            return True
        return False

    def is_5(self, block):
        if self.map[block.x][block.y] == 5:
            for point in self.hash[(block.x, block.y)]:
                self.map[point[0]][point[1]] = 0
            return True
        elif self.map[block.x + 1][block.y] == 5 and block.state == "LAY_X":
            for point in self.hash[(block.x + 1, block.y)]:
                self.map[point[0]][point[1]] = 0
            return True
        elif self.map[block.x][block.y + 1] == 5 and block.state == "LAY_Y":
            for point in self.hash[(block.x, block.y + 1)]:
                self.map[point[0]][point[1]] = 0
            return True
        return False

    def is_6(self, block):
        if self.map[block.x][block.y] == 6 and block.state == "STAND":
            for point in self.hash[(block.x, block.y)]:
                self.map[point[0]][point[1]] ^= 1
            return True
        return False

    def is_7(self, block):
        if self.map[block.x][block.y] == 7 and block.state == "STAND":
            for point in self.hash[(block.x, block.y)]:
                self.map[point[0]][point[1]] = 0
            return True
        return False

    def is_8(self, block):
        if self.map[block.x][block.y] == 8 and block.state == "STAND":
            t = copy.deepcopy(self.block)
            self.block.x = self.hash[(t.x,t.y)][0][0]
            self.block.y = self.hash[(t.x,t.y)][0][1]
            self.block.x1 = self.hash[(t.x,t.y)][1][0]
            self.block.y1 = self.hash[(t.x,t.y)][1][1]
            self.block.state = "SPLIT"

    def is_9(self, block):
        if self.map[block.x][block.y] == 9 and block.state == "STAND":
            return True
        else:
            return False

    def is_0_split(self, block):
        if self.map[block.x][block.y] == 0:
            return True
        return False
    def is_1_split(self, block):
        pass
    def is_2_split(self, block):
        pass
    def is_3_split(self, block):
        if self.map[block.x][block.y] == 3:
            for point in self.hash[(block.x, block.y)]:
                    self[point[0]][point[1]] ^= 1
    def is_4_split(self, block):
        if self.map[block.x][block.y] == 4:
            for point in self.hash[(block.x, block.y)]:
                    self[point[0]][point[1]] = 1
    def is_5_split(self, block):
        if self.map[block.x][block.y] == 5:
            for point in self.hash[(block.x, block.y)]:
                    self[point[0]][point[1]] = 0
    def is_6_split(self, block):
        pass
    def is_7_split(self, block):
        pass
    def is_8_split(self, block):
        pass
    def is_9_split(self, block):
        pass
    def check_all(self):
        check = False
        check |= self.is_0(self.block)
        check |= self.is_2(self.block)
        self.is_3(self.block)
        self.is_4(self.block)
        self.is_5(self.block)
        self.is_6(self.block)
        self.is_7(self.block)
        self.is_8(self.block)
        return check
    def check_all_split(self):
        check = self.is_0_split(self.block)
        self.is_3(self.block)
        self.is_4(self.block)
        self.is_5(self.block)
        return check
