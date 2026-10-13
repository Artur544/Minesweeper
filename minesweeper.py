import pyxel
import random

class Block:
    def __init__(self, x, y, is_bomb, area_bombs = None):
        self.x = x
        self.y = y
        self.is_bomb = is_bomb
        self.area_bombs = area_bombs
        self.IMG, self.W, self.H = 0, 8, 8
        self.clicked, self.marked = False, False

    def draw(self):
        # pyxel.rect(self.x, self.y, 8, 8, 12)
        # pyxel.rect(self.x + 1, self.y + 1, 6, 6, 10)
        # self.u = ((pyxel.frame_count//4) % 23) * 8
        if self.marked:
            self.u = 88; self.v = 8
        elif not self.clicked:
            self.u = 80; self.v = 0
        elif self.is_bomb:
            self.u = 72; self.v = 8
        else:
            self.u = self.area_bombs * 8; self.v = 8
        pyxel.blt(self.x, self.y, self.IMG, self.u, self.v, self.W, self.H)

class Minesweeper:
    def __init__(self, dif, style, debug):
        self.bombs = 12 * (2 ** dif)
        self.L, self.C = 20, 15
        self.GAP = 2
        self.style = style
        self.map = []
        self.debug = debug

        for l in range(self.L):
            self.map.append([])
            for c in range(self.C):
                self.map[l].append(Block(self.GAP + (8*c), self.GAP + (8*l), False, 0))

    def get_area_pos(self, l, c):
        if l - 1 < 0: min_l = 0; max_l = 3
        elif l + 2 > 19: min_l = 17; max_l = 20
        else: min_l = l - 1; max_l = l + 2
        if c - 1 < 0: min_c = 0; max_c = 3
        elif c + 2 > 14: min_c = 12; max_c = 15
        else: min_c = c - 1; max_c = c + 2
        area = []
        for line in range(min_l, max_l):
            for colum in range(min_c, max_c):
                area.append(line * self.C + colum)
        return area
    
    def init_bombs(self, l, c):
        area_ck = self.get_area_pos(l, c)
        available_map = [i for i in range(self.L * self.C) if i not in area_ck]
        print(area_ck)
        
        if not self.debug:
            self.bombs_pos = random.sample(available_map, self.bombs)
        else:
            self.bombs_pos = [28, 267, 118, 102, 15, 263, 265, 240, 235, 284, 290, 281, 298, 260, 196, 229, 71, 257, 53, 89, 268, 26, 246, 97, 100, 137, 108, 191, 149, 295, 210, 294, 92, 282, 166, 143, 231, 72, 104, 286, 39, 23, 167, 19, 255, 181, 6, 180, 76, 34, 202, 128, 289, 261, 120, 114, 212, 228, 224, 259, 199, 1, 262, 213, 269, 42, 226, 121, 88, 74, 206, 117, 57, 73, 190, 237, 139, 239, 43, 153, 245, 193, 223, 270, 214, 3, 4, 200, 292, 13, 227, 7, 148, 138, 63, 90]
        print(f"\n\nBombas Array: {self.bombs_pos}\n\n")
        pos = 0
        for l in range(self.L):
            for c in range(self.C):
                if pos in self.bombs_pos:
                    self.map[l][c] = Block(self.GAP + (8*c), self.GAP + (8*l), True)
                elif pos not in area_ck:
                    self.map[l][c] = Block(self.GAP + (8*c), self.GAP + (8*l), False)
                pos += 1
        pos = 0
        for l in range(self.L):
            for c in range(self.C):
                if not self.map[l][c].is_bomb:
                    self.map[l][c] = Block(self.GAP + (8*c), self.GAP + (8*l), False, self.count_bombs(l, c))

    def count_bombs(self, bl, bc):
        count = 0
        min_bl = 0 if bl - 1 < 0 else bl - 1
        min_bc = 0 if bc - 1 < 0 else bc - 1
        max_bl = 20 if bl + 2 > 19 else bl + 2
        max_bc = 15 if bc + 2 > 14 else bc + 2
        for l in range(min_bl, max_bl):
            for c in range(min_bc, max_bc):
                if self.map[l][c].is_bomb:
                    count += 1
        return count