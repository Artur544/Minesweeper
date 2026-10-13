import pyxel
from minesweeper import Minesweeper
from info import Info

class Table:
    def __init__(self, dif, style, debug = False):
        self.mine = Minesweeper(dif, style, debug)
        self.info = Info(self.mine.bombs, dif, style)
        self.GAP = self.mine.GAP
        self.marks, self.frame = 0, 0
        self.defeat, self.first_ck = False, False
        self.arr_draw = []

    def collide(self, block):
        return (pyxel.mouse_x - block.x >= 0 and pyxel.mouse_x - block.x < block.W) and (pyxel.mouse_y - block.y >= 0 and pyxel.mouse_y - block.y < block.H)

    def get_area(self, bl, bc):
        min_bl = 0 if bl - 1 < 0 else bl - 1
        min_bc = 0 if bc - 1 < 0 else bc - 1
        max_bl = 20 if bl + 2 > 19 else bl + 2
        max_bc = 15 if bc + 2 > 14 else bc + 2
        return [[min_bl, max_bl], [min_bc, max_bc]]

    def show_empty(self, bl, bc, array_b):
        area = self.get_area(bl, bc)
        for l in range(area[0][0], area[0][1]):
            for c in range(area[1][0], area[1][1]):
                if not self.mine.map[l][c].marked:
                    if not self.mine.map[l][c].area_bombs:
                        if not self.mine.map[l][c].clicked: 
                            array_b.append([l, c])
                    self.mine.map[l][c].clicked = True
        if array_b:
            return [array_b[0][0], array_b[0][1], array_b[1:]]

    def show_unmarked(self, bl, bc):
        area = self.get_area(bl, bc); b_marked = 0
        for l in range(area[0][0], area[0][1]):
            for c in range(area[1][0], area[1][1]):
                if self.mine.map[l][c].marked: b_marked += 1 
        if self.mine.map[bl][bc].area_bombs == b_marked:
            for l in range(area[0][0], area[0][1]):
                for c in range(area[1][0], area[1][1]):
                    if not self.mine.map[l][c].marked:
                        if not (self.mine.map[l][c].area_bombs or self.mine.map[l][c].is_bomb):
                            if not self.arr_draw: self.arr_draw = self.show_empty(l, c, [])
                        else: self.mine.map[l][c].clicked = True